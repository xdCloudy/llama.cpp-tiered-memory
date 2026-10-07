# Results ledger

No compression or inference improvement is established yet. Current upstream is bd4eeaa047006cb1fe71999fbd11134b5836e167. Initial CPU builds and one small-model CPU throughput capture are recorded in [the baseline report](docs/benchmarks/2026-10-07-baseline.md).

## Environment inventory (not a performance result)
- OS: Windows 11 Pro build 26200; WSL2 Ubuntu 24.04 kernel 6.18.33.2.
- CPU: Intel Core i5-14600K.
- GPU: NVIDIA GeForce RTX 3060, 12,288 MiB; driver 610.74.
- CUDA Toolkit: 13.3.
- System RAM: 63.7 GiB physical; WSL reports 15 GiB.
- Compiler/build flags and workload: see baseline report.

## Results
| Date | Experiment | Commit | Hardware/workload | RAM | VRAM | Load/TTFT | Prompt tok/s | Generation tok/s | Transfer/faults | Outcome |
|---|---|---|---|---|---|---|---|---|---|---|
| 2026-10-07 | CPU baseline | upstream/fork runtime SHA bd4eeaa | Qwen3.5-0.8B BF16, Windows, p=256, n=64, ngl=0 | pending | n/a | pending | 237.97 (sd 19.70) | 15.35 (sd 2.66) | pending | reference only |
