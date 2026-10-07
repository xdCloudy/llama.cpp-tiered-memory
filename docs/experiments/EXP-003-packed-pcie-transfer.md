# EXP-003: packed PCIe transfer economics

## Question
Can reduced host-to-device bytes and overlap compensate for codec decode cost on supported CUDA shapes?

## Hypothesis
Selected cold blocks under transfer pressure may benefit; decode can dominate for small blocks or compute-bound workloads.

## Dependencies
Run after EXP-001 identifies a viable lossless format/block size and transfer baselines exist.

## Measurements
Packed/logical bytes, copy throughput/latency, CPU/GPU decode, synchronization/overlap, peak RAM/VRAM, TTFT, prompt tok/s, and generation tok/s against upstream and feature-disabled controls. No result is established.
