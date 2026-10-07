#!/usr/bin/env python3
"""Profile lossless secondary compression of GGUF tensor bytes."""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.metadata
import json
import math
import platform
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from collections.abc import Iterable, Iterator
from pathlib import Path
from typing import Any

import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "gguf-py"))

from gguf import GGUFReader  # noqa: E402


LAYER_RE = re.compile(r"(?:blk|layers)\.(\d+).")
EXPERT_ID_RE = re.compile(r"(?:expert|experts)[._](\d+)(?:\.|$)", re.IGNORECASE)
EXPERT_TENSOR_RE = re.compile(r"(?:_exps|_experts|expert)", re.IGNORECASE)


def shannon_entropy(histogram: np.ndarray, total: int) -> float:
    """Return byte entropy in bits per byte from a 256-bin histogram."""
    if total <= 0:
        return 0.0
    probabilities = histogram[histogram > 0].astype(np.float64) / total
    return float(-np.sum(probabilities * np.log2(probabilities)))


def classify_tensor(name: str) -> tuple[str, int | None, int | str | None]:
    """Infer a coarse role, layer index, and explicit/embedded expert ID."""
    layer_match = LAYER_RE.search(name)
    expert_match = EXPERT_ID_RE.search(name)
    layer = int(layer_match.group(1)) if layer_match else None
    expert_id: int | str | None = int(expert_match.group(1)) if expert_match else None
    if expert_id is None and EXPERT_TENSOR_RE.search(name):
        expert_id = "embedded"

    low = name.lower()
    if "attn" in low or "attention" in low:
        role = "attention"
    elif "ffn" in low and EXPERT_TENSOR_RE.search(name):
        role = "expert_weight"
    elif "ffn" in low:
        role = "feed_forward"
    elif "token_embd" in low or "tok_embeddings" in low or "embed_tokens" in low:
        role = "embedding"
    elif "output" in low or "lm_head" in low:
        role = "output"
    elif "norm" in low:
        role = "normalization"
    else:
        role = "other"
    return role, layer, expert_id


def iter_sampled_chunks(data: np.ndarray, sample_limit: int, chunk_size: int) -> Iterator[bytes]:
    """Yield chunks from a byte view, sampling evenly when a limit is set."""
    byte_view = np.asarray(data).view(np.uint8).reshape(-1)
    byte_count = int(byte_view.size)
    if sample_limit < 0:
        raise ValueError("sample_limit must be non-negative")
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")

    if sample_limit == 0 or sample_limit >= byte_count:
        windows = [(0, byte_count)]
    else:
        window_count = max(1, math.ceil(sample_limit / chunk_size))
        window_size = min(chunk_size, max(1, sample_limit // window_count))
        if window_count == 1:
            starts = [max(0, (byte_count - window_size) // 2)]
        else:
            max_start = max(0, byte_count - window_size)
            starts = [int(round(i * max_start / (window_count - 1))) for i in range(window_count)]
        windows = [(start, min(byte_count, start + window_size)) for start in starts]

    for start, end in windows:
        pos = start
        while pos < end:
            next_pos = min(end, pos + chunk_size)
            yield byte_view[pos:next_pos].tobytes()
            pos = next_pos


def codec_compressors(codec: str, level: int | None) -> tuple[Any, Any]:
    if codec == "lz4":
        try:
            import lz4.frame
        except ImportError as exc:
            raise RuntimeError("codec lz4 requires the optional Python package 'lz4'") from exc
        return lz4.frame.compress, lz4.frame.decompress
    if codec == "zstd":
        try:
            import zstandard
        except ImportError as exc:
            raise RuntimeError("codec zstd requires the optional Python package 'zstandard'") from exc
        compressor = zstandard.ZstdCompressor(level=level or 3)
        decompressor = zstandard.ZstdDecompressor()
        return compressor.compress, decompressor.decompress
    raise ValueError(f"unsupported codec: {codec}")


def measure_codec(chunks: Iterable[bytes], codec: str, level: int | None) -> dict[str, Any]:
    compress, decompress = codec_compressors(codec, level)
    input_bytes = 0
    output_bytes = 0
    encode_seconds = 0.0
    decode_seconds = 0.0
    for raw in chunks:
        input_bytes += len(raw)
        started = time.perf_counter()
        packed = compress(raw)
        encode_seconds += time.perf_counter() - started
        output_bytes += len(packed)
        started = time.perf_counter()
        restored = decompress(packed)
        decode_seconds += time.perf_counter() - started
        if restored != raw:
            raise ValueError(f"{codec} produced a non-identical round trip")

    return {
        "codec": codec,
        "level": level if codec == "zstd" else None,
        "input_bytes": input_bytes,
        "compressed_bytes": output_bytes,
        "ratio": (output_bytes / input_bytes) if input_bytes else 1.0,
        "saving_bytes": input_bytes - output_bytes,
        "encode_mib_s": (input_bytes / (1024 * 1024) / encode_seconds) if encode_seconds else None,
        "decode_mib_s": (input_bytes / (1024 * 1024) / decode_seconds) if decode_seconds else None,
        "round_trip": "exact",
    }


def tensor_histogram(chunks: Iterable[bytes]) -> tuple[np.ndarray, int]:
    hist = np.zeros(256, dtype=np.uint64)
    total = 0
    for chunk in chunks:
        view = np.frombuffer(chunk, dtype=np.uint8)
        hist += np.bincount(view, minlength=256).astype(np.uint64)
        total += int(view.size)
    return hist, total


def metadata_value(reader: GGUFReader, key: str) -> Any:
    field = reader.fields.get(key)
    if field is None:
        return None


def tool_metadata(codecs: list[str]) -> dict[str, Any]:
    try:
        commit = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=REPO_ROOT, check=True,
            capture_output=True, text=True,
        ).stdout.strip()
        dirty = bool(subprocess.run(
            ["git", "status", "--porcelain", "--untracked-files=no", "--",
             "tools/gguf_tensor_profiler.py", "tools/gguf-profiler-requirements.txt", "tools/tests"],
            cwd=REPO_ROOT, check=True, capture_output=True, text=True,
        ).stdout.strip())
    except (OSError, subprocess.CalledProcessError):
        commit, dirty = None, None

    codec_versions: dict[str, str | None] = {}
    for codec, package in (("lz4", "lz4"), ("zstd", "zstandard")):
        if codec in codecs:
            try:
                codec_versions[codec] = importlib.metadata.version(package)
            except importlib.metadata.PackageNotFoundError:
                codec_versions[codec] = None

    return {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "tool_commit": commit,
        "tool_tree_dirty": dirty,
        "tool_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "python_version": platform.python_version(),
        "system_platform": platform.platform(),
        "processor": platform.processor(),
        "codec_versions": codec_versions,
    }
    try:
        return field.contents()
    except (IndexError, TypeError, ValueError):
        return None


def validate_tensor_bounds(path: Path, reader: GGUFReader, tensor: Any) -> None:
    file_size = path.stat().st_size
    offset = int(tensor.data_offset)
    size = int(tensor.n_bytes)
    if offset < reader.data_offset or size < 0 or offset > file_size or size > file_size - offset:
        raise ValueError(f"tensor {tensor.name!r} range [{offset}, {offset + size}) exceeds GGUF file size {file_size}")
    if int(tensor.data.nbytes) != size:
        raise ValueError(f"tensor {tensor.name!r} mapped byte count does not match GGUF metadata")


def profile_file(
    path: Path,
    chunk_sizes: list[int],
    sample_bytes: int,
    codecs: list[str],
    zstd_levels: list[int],
) -> dict[str, Any]:
    reader = GGUFReader(path, mode="r")
    tensor_records: list[dict[str, Any]] = []
    for tensor in reader.tensors:
        validate_tensor_bounds(path, reader, tensor)
        role, layer, expert_id = classify_tensor(tensor.name)
        byte_count = int(tensor.n_bytes)
        sampled_limit = byte_count if sample_bytes == 0 else min(byte_count, sample_bytes)
        estimates: dict[str, float] = {}
        measurements: list[dict[str, Any]] = []

        for chunk_size in chunk_sizes:
            hist, sampled_total = tensor_histogram(iter_sampled_chunks(tensor.data, sampled_limit, chunk_size))
            estimates[str(chunk_size)] = shannon_entropy(hist, sampled_total)
            for codec in codecs:
                levels: list[int | None] = zstd_levels if codec == "zstd" else [None]
                for level in levels:
                    result = measure_codec(iter_sampled_chunks(tensor.data, sampled_limit, chunk_size), codec, level)
                    result["chunk_size"] = chunk_size
                    result["sampled_bytes"] = sampled_total
                    result["sample_mode"] = "full" if sampled_limit == byte_count else "even_windows"
                    estimated_ratio = result["ratio"]
                    result["estimated_saving_bytes_full_tensor"] = int(round(byte_count * (1.0 - estimated_ratio)))
                    result["estimated_pcie_bytes_saved_per_tensor"] = int(round(byte_count * (1.0 - estimated_ratio)))
                    result["entropy_bits_per_byte"] = estimates[str(chunk_size)]
                    measurements.append(result)

        tensor_records.append({
            "name": tensor.name,
            "type": tensor.tensor_type.name,
            "dimensions": [int(dim) for dim in tensor.shape],
            "logical_elements": int(tensor.n_elements),
            "logical_bytes": byte_count,
            "role": role,
            "layer": layer,
            "expert_id": expert_id,
            "entropy_bits_per_byte_by_chunk_size": estimates,
            "measurements": measurements,
        })

    return {
        "schema_version": 1,
        "environment": tool_metadata(codecs),
        "source_file": str(path.resolve()),
        "source_size_bytes": path.stat().st_size,
        "model_name": metadata_value(reader, "general.name"),
        "architecture": metadata_value(reader, "general.architecture"),
        "tensor_count": len(tensor_records),
        "chunk_sizes": chunk_sizes,
        "sample_bytes_per_tensor": sample_bytes,
        "codecs": codecs,
        "zstd_levels": zstd_levels,
        "tensors": tensor_records,
    }


def flatten_report(report: dict[str, Any]) -> Iterator[dict[str, Any]]:
    for tensor in report["tensors"]:
        for measurement in tensor["measurements"]:
            yield {
                "source_file": report["source_file"],
                "timestamp_utc": report["environment"]["timestamp_utc"],
                "tool_commit": report["environment"]["tool_commit"],
                "tool_tree_dirty": report["environment"]["tool_tree_dirty"],
                "tool_sha256": report["environment"]["tool_sha256"],
                "python_version": report["environment"]["python_version"],
                "system_platform": report["environment"]["system_platform"],
                "processor": report["environment"]["processor"],
                "codec_versions": json.dumps(report["environment"]["codec_versions"], sort_keys=True),
                "model_name": report["model_name"],
                "architecture": report["architecture"],
                "tensor_name": tensor["name"],
                "type": tensor["type"],
                "dimensions": "x".join(str(x) for x in tensor["dimensions"]),
                "logical_bytes": tensor["logical_bytes"],
                "role": tensor["role"],
                "layer": tensor["layer"],
                "expert_id": tensor["expert_id"],
                "chunk_size": measurement["chunk_size"],
                "sampled_bytes": measurement["sampled_bytes"],
                "sample_mode": measurement["sample_mode"],
                "entropy_bits_per_byte": measurement["entropy_bits_per_byte"],
                "codec": measurement["codec"],
                "level": measurement["level"],
                "compressed_bytes": measurement["compressed_bytes"],
                "ratio": measurement["ratio"],
                "saving_bytes": measurement["saving_bytes"],
                "estimated_saving_bytes_full_tensor": measurement["estimated_saving_bytes_full_tensor"],
                "estimated_pcie_bytes_saved_per_tensor": measurement["estimated_pcie_bytes_saved_per_tensor"],
                "encode_mib_s": measurement["encode_mib_s"],
                "decode_mib_s": measurement["decode_mib_s"],
                "round_trip": measurement["round_trip"],
            }


def parse_int_list(value: str) -> list[int]:
    try:
        values = [int(part.strip()) for part in value.split(",") if part.strip()]
    except ValueError as exc:
        raise argparse.ArgumentTypeError("expected comma-separated integers") from exc
    if not values or any(item <= 0 for item in values):
        raise argparse.ArgumentTypeError("values must be positive")
    return values


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("gguf", type=Path, help="input GGUF model file")
    parser.add_argument("--chunk-sizes", type=parse_int_list, default=[4096, 16384, 65536, 262144, 1048576])
    parser.add_argument("--sample-bytes", type=int, default=1024 * 1024,
                        help="bytes sampled per tensor (0 scans all payload bytes; default: 1 MiB)")
    parser.add_argument("--codecs", default="lz4,zstd", help="comma-separated lossless codecs: lz4,zstd")
    parser.add_argument("--zstd-levels", type=parse_int_list, default=[1, 3, 9])
    parser.add_argument("--format", choices=("json", "csv"), default="json")
    parser.add_argument("--output", type=Path, help="output file (default: stdout)")
    args = parser.parse_args()
    if args.sample_bytes < 0:
        parser.error("--sample-bytes must be non-negative")
    if not args.gguf.is_file():
        parser.error(f"input file not found: {args.gguf}")
    codecs = [item.strip().lower() for item in args.codecs.split(",") if item.strip()]
    if not codecs or any(codec not in {"lz4", "zstd"} for codec in codecs):
        parser.error("--codecs accepts lz4 and/or zstd")

    try:
        report = profile_file(args.gguf, args.chunk_sizes, args.sample_bytes, codecs, args.zstd_levels)
    except (OSError, ValueError, RuntimeError, IndexError, OverflowError, MemoryError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    destination = args.output.open("w", newline="", encoding="utf-8") if args.output else sys.stdout
    try:
        if args.format == "json":
            json.dump(report, destination, indent=2)
            destination.write("\n")
        else:
            rows = list(flatten_report(report))
            if rows:
                writer = csv.DictWriter(destination, fieldnames=list(rows[0]))
                writer.writeheader()
                writer.writerows(rows)
    finally:
        if args.output:
            destination.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
