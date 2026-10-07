# Benchmark methodology

Every benchmark compares (1) current upstream, (2) fork with feature disabled, and (3) fork with feature enabled on the same workload and machine. Pin commits and binaries. Warm up, repeat, and report median plus spread rather than the best run. Avoid concurrent workloads and record observable thermal or clock limits.

## Required workload manifest
Git/upstream SHAs; OS/build/kernel; CPU/core count; RAM; GPU/VRAM/driver/CUDA; compiler and flags; model/architecture/quant/size; context and prompt; batch/ubatch; GPU layers; flash attention; mmap/mlock/load mode; KV type; threads; NUMA; seed; all relevant flags; cold/warm cache condition; repetitions.

## Required outcomes
Peak/steady host RAM and VRAM; load time; TTFT; prompt and generation tokens/s; total latency; CPU/GPU utilization; H2D/D2H bytes where measurable; page faults; compressed/logical bytes; ratio; encode/decode throughput; cache hits/misses; expert promotions/evictions; prefetch accuracy and wasted bytes.

Keep capacity separate from bandwidth and speed. Note resident, mapped, committed, pinned, shared, and virtual memory. Profile codec microbenchmarks and end-to-end inference separately. See docs/experiments/EXPERIMENT_TEMPLATE.md and RESULTS.md.
