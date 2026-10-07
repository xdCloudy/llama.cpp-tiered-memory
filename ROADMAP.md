# Roadmap

Evidence comes before runtime integration. Milestones use planned/active/blocked/complete; completion requires recorded evidence rather than implementation alone.

## Phase A: establish evidence
- M0 Research & Baseline: map current architecture, review research, create repeatable harness, and collect build/measurement controls.
- M1 Tensor Compressibility Profiler: profile GGUF payloads by quant, tensor role, and independent block size.
- M2 Memory Instrumentation: allocation, transfer, fault, and residency counters without changing placement.

## Phase B: test compact storage
- M3 opt-in random-access packed-memory prototype and block index.
- M4 bounded HOT/WARM/COLD/VERY COLD tier policy with hysteresis and thrash measurements.
- M5 CUDA packed-transfer economics and decode/transfer overlap.
- M6 fused GPU decode/compute only for measured kernel/shape combinations.

## Phase C: semantic workloads
- M7 MoE routing locality and expert-cache strategies, based on the existing MoE cache.
- M8 architecture-aware KV representation and tiering.
- M9 Linux and Windows mmap/OS paths measured separately.
- M10 CPU SIMD and decode/compute fusion.
- M11 layer/expert prefetch and overlap.
- M12 whole-path duplication, staging, workspace, and fragmentation audit.

## Phase D: platforms and stability
- M13 Windows-specific profiling and improvements.
- M14 Linux-specific profiling and optional capabilities.
- M15 productionization only for experiments with measured, repeatable benefit.

See MILESTONES.md for exit criteria. Do not start CUDA implementation before M0/M1 evidence identifies a worthwhile format and workload.
