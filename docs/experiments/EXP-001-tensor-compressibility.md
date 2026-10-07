# EXP-001: GGUF tensor compressibility

## Question
How much secondary compression remains in already quantized GGUF payloads, by tensor type, role, and independent block size?

## Hypothesis
Some tensors may retain local redundancy, but Q4-Q8 blocks may be poorly suited to generic compression. The profiler may show that a transform or no secondary compression is preferable.

## Implementation
Initial standalone profiler is `tools/gguf_tensor_profiler.py`; it uses gguf-py mapped tensor payloads and does not change inference. It supports evenly sampled or full scans, byte entropy, LZ4 and selected Zstd levels at independent 4 KiB, 16 KiB, 64 KiB, 256 KiB, and 1 MiB chunks. It records tensor name/dimensions/type/bytes, coarse role/layer/embedded expert identity, ratio, encode/decode speed, sample mode, and theoretical bytes saved. Additional transforms remain future work if data justifies them.

## Status
Profiler implementation and BF16 full-payload scan are in progress. The first model is Qwen3.5-0.8B BF16 (1,546,700,032 tensor bytes, 335 tensors), measured on Windows 11 Pro build 26200 with an Intel Core i5-14600K. The tool ran under Python 3.11.9, NumPy 2.4.6, LZ4 4.4.5, and Zstandard 0.23.0. Exact raw reports and a pinned tool commit will be added with the results update.

The first full scan ran concurrently with a CUDA build and is retained as a diagnostic, not a clean throughput measurement. A second scan after the build completed took 66.03 seconds. The payload was warm in the OS page cache for the repeat. Results below are exact for this one BF16 model; they do not cover already-quantized Q2-Q8 tensors, other architectures, or inference.

| Codec | Block | Ratio | Bytes saved | Encode MiB/s | Decode MiB/s |
|---|---:|---:|---:|---:|---:|
| LZ4 frame | 4 KiB | 1.0053 | -7.8 MiB | 1,508 | 1,569 |
| LZ4 frame | 16 KiB | 1.0008 | -1.2 MiB | 2,866 | 4,461 |
| LZ4 frame | 64 KiB | 0.9996 | 0.5 MiB | 3,714 | 7,110 |
| Zstd level 1 | 4 KiB | 0.7963 | 300.4 MiB | 304 | 612 |
| Zstd level 1 | 16 KiB | 0.7846 | 317.7 MiB | 560 | 808 |
| Zstd level 1 | 64 KiB | 0.7823 | 321.1 MiB | 694 | 939 |
| Zstd level 3 | 4 KiB | 0.7964 | 300.3 MiB | 249 | 609 |
| Zstd level 3 | 16 KiB | 0.7847 | 317.6 MiB | 482 | 803 |
| Zstd level 3 | 64 KiB | 0.7823 | 321.1 MiB | 659 | 936 |

The model contains 195 BF16 tensors totaling 1,473.1 MiB and 140 F32 tensors totaling 1.9 MiB. At 64 KiB blocks, Zstd level 1 ratios were 0.7827 for BF16 and 0.5007 for the small F32 subset. These storage-only results make Zstd worth testing on other models and quant types; they do not establish that CPU decoding or PCIe transfer improves inference. LZ4 is effectively neutral here. The sample pilot and full scans are linked from docs/benchmarks/raw/.

## Next action
Keep M1 active. Add full scans for already-quantized Q2/IQ2/Q3/Q4/Q5/Q6/Q8 tensors and at least one MoE model, validate report provenance, and test 256 KiB/1 MiB blocks. Do not proceed to packed transfer based on this BF16 result alone.
