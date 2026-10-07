# EXP-001: GGUF tensor compressibility

## Question
How much secondary compression remains in already quantized GGUF payloads, by tensor type, role, and independently decodable block size?

## Hypothesis
Some tensor classes may retain local redundancy, but already-quantized Q4-Q8 payloads may be poorly suited to generic compression. A profiler can show whether to retain a codec, test a transform, or stop the compression path.

## Implementation
`tools/gguf_tensor_profiler.py` reads GGUF metadata and mapped tensor payloads through gguf-py; it does not change inference or GGUF. It supports deterministic even-window sampling or full scans, byte entropy, LZ4 frames, Zstd levels, and 4 KiB through 1 MiB chunk sizes. It records type, dimensions, bytes, coarse role/layer/expert identity, ratio, encode/decode speed, sample mode, and theoretical savings. Exact lossless round trips are checked for each measured block.

## Hardware
- CPU: Intel Core i5-14600K.
- RAM: 63.7 GiB system memory.
- OS: Windows 11 Pro build 26200.
- GPU: NVIDIA RTX 3060 12 GiB; unused by this storage profiler experiment.

## Software
- Upstream/runtime base: `bd4eeaa047006cb1fe71999fbd11134b5836e167`.
- Profiler commit: `e47cba84f4b21f417279d5fab834874797683f86`; tool tree clean.
- Python 3.11.9, NumPy 2.4.6, LZ4 4.4.5, Zstandard 0.23.0.
- Full scan ran with no build running; the file pages were warm in the OS cache after earlier profile runs.
- Tool SHA-256: `75f30aadf5f34b24e7581871576812b8697c376b447fab7b48c652c769531e29`.

## Model and workload
Qwen3.5-0.8B BF16 GGUF, 772,845,888 parameters, 1,546,700,032 logical tensor bytes, 335 tensors. This is one BF16 model, not a coverage result for quantized Q2-Q8 weights. The model file is local and is not included in this repository. The full scan covered all tensor bytes at 4 KiB, 16 KiB, and 64 KiB chunk sizes; 1 MiB total scan time was 66.4 seconds.

## Baseline
Each source chunk is compared to its own lossless codec output. LZ4 frame defaults and Zstd levels 1 and 3 are used. The earlier full scan overlapped a CUDA build and is retained in `docs/benchmarks/raw/2026-10-07-qwen35-bf16-full-during-cuda-build.csv`; the table below uses the subsequent scan after the build completed.

## Results
Ratios below are total compressed payload bytes divided by total input bytes. Encode/decode rates are input-byte-weighted aggregates of per-tensor measurements. Framing/index overhead outside each independently compressed block is not included.

| Codec | Block | Ratio | Saved | Encode MiB/s | Decode MiB/s |
|---|---:|---:|---:|---:|---:|
| LZ4 frame | 4 KiB | 1.0053 | -7.8 MiB | 1,503 | 1,570 |
| LZ4 frame | 16 KiB | 1.0008 | -1.2 MiB | 2,836 | 4,458 |
| LZ4 frame | 64 KiB | 0.9996 | 0.5 MiB | 3,629 | 7,682 |
| Zstd level 1 | 4 KiB | 0.7963 | 300.4 MiB | 303 | 609 |
| Zstd level 1 | 16 KiB | 0.7846 | 317.7 MiB | 557 | 806 |
| Zstd level 1 | 64 KiB | 0.7823 | 321.1 MiB | 694 | 938 |
| Zstd level 3 | 4 KiB | 0.7964 | 300.3 MiB | 249 | 609 |
| Zstd level 3 | 16 KiB | 0.7847 | 317.6 MiB | 485 | 805 |
| Zstd level 3 | 64 KiB | 0.7823 | 321.1 MiB | 652 | 933 |

At 64 KiB blocks, the model contains 195 BF16 tensors totaling 1,473.1 MiB with ratio 0.7827, and 140 F32 tensors totaling 1.9 MiB with ratio 0.5007. The F32 subset is small and should not be treated as a model-wide result.

Raw CSV and runtime provenance: `docs/benchmarks/raw/2026-10-07-qwen35-bf16-full.csv`. Sampled pilot: `docs/benchmarks/raw/2026-10-07-qwen35-bf16-profiler-pilot.csv`. Elapsed-time record: `docs/benchmarks/raw/2026-10-07-qwen35-bf16-full-timing.txt`.

## RAM impact
No inference allocation or model file was modified. The profiler maps the GGUF and creates one temporary input/codec buffer per block. This experiment did not measure process peak/steady RAM or residency.

## VRAM impact
None. No CUDA work ran in this experiment.

## Performance impact
This measures host codec throughput only. It does not measure model load, TTFT, prompt processing, generation, PCIe transfer, or cache behavior. It provides no inference speed result.

## Interpretation
Zstd retains useful redundancy in this BF16 model: the measured ratio improves from 0.7963 at 4 KiB to 0.7823 at 64 KiB, while level 3 gives nearly the same ratio as level 1 at lower throughput. LZ4 frame is neutral or slightly expands the bytes. This makes Zstd a candidate for follow-up on other formats, but the result does not show that CPU decode can beat transfer cost or that compressed storage reduces peak RAM.

## Problems
The first full scan overlapped CUDA compilation and is not used for codec throughput conclusions. Bitshuffle and other transforms were not tested. Only one BF16 model was available; quantized types and MoE coverage remain unmeasured. The scan was warm-cache, and its throughput is not a cold-file or inference measurement.

## Conclusion
Positive storage-compressibility result for this BF16 GGUF with Zstd, neutral result for LZ4, and no demonstrated inference benefit. Do not generalize to already-quantized tensors.

## Next action
Keep M1 active. Run full scans for representative Q2/IQ2/Q3/Q4/Q5/Q6/Q8 models and an MoE model; compare 256 KiB and 1 MiB blocks; add bitshuffle only if justified; preserve per-type and per-role results. Gate CUDA transfer work on its own transfer/decode measurements.
