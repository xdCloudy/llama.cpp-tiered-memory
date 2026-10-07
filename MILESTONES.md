# Milestones

GitHub milestones mirror this list. Dates are unset until work is scoped. A milestone is complete only when acceptance evidence is published in RESULTS.md or a linked report.

| ID | Name | Initial state | Exit evidence |
|---|---|---|---|
| M0 | Research & Baseline | active | architecture map, baseline builds/manifests, repeatable measurement procedure |
| M1 | Tensor Compressibility Profiler | planned | reproducible tensor report with codecs, chunk sizes, ratios and throughput |
| M2 | Memory Instrumentation | planned | allocation/copy/fault counters with known limits |
| M3 | Packed Memory Backend | planned | opt-in random-access block store, corruption checks, fallback |
| M4 | Hot/Warm/Cold Tiering | planned | bounded promotion/demotion and thrash measurements |
| M5 | CUDA Packed Transfer | planned | transfer bytes, decode cost, end-to-end effect |
| M6 | Fused GPU Decode + Compute | planned | correctness and kernel-shape performance evidence |
| M7 | MoE Expert Cache | planned | locality data and strategy comparison on realistic prompts |
| M8 | KV Cache Research | planned | architecture-aware capacity, speed, and quality report |
| M9 | mmap / OS Memory Path | planned | Linux/Windows comparison under matched workloads |
| M10 | CPU Decode Optimisation | planned | CPU-only throughput, utilization, and correctness |
| M11 | Prefetching & Prediction | planned | hit/accuracy, overlap, wasted bytes, and throughput |
| M12 | Memory Footprint Optimisation | planned | allocation/copy audit and quantified changes |
| M13 | Windows Optimisation | planned | Windows-specific repeatable results and fallback review |
| M14 | Linux Optimisation | planned | Linux-specific repeatable results and fallback review |
| M15 | Productionisation | planned | stable opt-in interface, tests, docs, CI, compatibility, fallback |

M0 and M1 are created as GitHub milestones first; each receives separate scoped issues. Later milestones receive issues before implementation begins.
