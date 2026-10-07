# GGUF and tensor metadata

GGUF metadata includes tensor names, dimensions, GGML type, offsets, and byte sizes. gguf-py and the C GGUF API support offline inspection; src/llama-model-loader.* maps metadata to model tensors and buffers. Treat models and sizes/offsets as untrusted input.

The initial profiler reads metadata and payloads without changing GGUF. It may derive layer/expert role from names and architecture metadata, but must report unknown mappings rather than guess. Secondary compressed representations need a distinct sidecar/container with versioning, bounds checks, alignment, index, and corruption detection. Never reinterpret existing quant bytes without explicit metadata.

Run the offline profiler from the repository root with `python tools/gguf_tensor_profiler.py model.gguf --output report.json`. Its default 1 MiB per-tensor sample is spread across the tensor; set `--sample-bytes 0` to scan all bytes. Codec packages are listed in `tools/gguf-profiler-requirements.txt`; use JSON for the detailed report or `--format csv` for flattened rows. Reports record tool/source environment and codec versions. The profiler validates mapped byte counts and exact round trips; it does not model inference speed or guarantee that a sample represents every tensor region.
