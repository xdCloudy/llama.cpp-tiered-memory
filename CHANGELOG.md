# Changelog

## 2026-10-07 - Research fork bootstrap
- Forked current ggml-org/llama.cpp at bd4eeaa047006cb1fe71999fbd11134b5836e167.
- Added upstream remote and named the fork llama.cpp-tiered-memory.
- Added research, architecture, measurement, platform, compatibility, and experiment documentation.
- No runtime behavior or performance changes are included.

## 2026-10-07 - M1 profiler prototype
- Added a standalone GGUF payload profiler for full and sampled scans with LZ4 and Zstandard.
- Added focused tests for sampling, quantized byte accounting, metadata classification, and exact codec round trips.
- Recorded an initial full-scan BF16 storage result; no inference path or default behavior changed.
