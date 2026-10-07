# Maintainer and agent guide

## Project identity
This fork, llama.cpp-tiered-memory, studies semantic, backend-aware compact representations and memory tiers for llama.cpp inference. It is inspired by CRAM-style compressed-memory principles but is an independent llama.cpp-specific research implementation. It is not a literal CRAM port.

## Mission and boundaries
Investigate RAM, VRAM, transfer, loading, KV, MoE, paging, and inference improvements using llama.cpp knowledge of tensor role, layer, backend, routing, and lifetime. Keep lossless packed storage, lossy model/KV changes, and OS paging experiments clearly distinguished. Do not build generic user-space ZRAM. Keep upstream behavior unchanged when an experiment is disabled.

## Working rules
- Read current upstream implementation before proposing an integration. UPSTREAM.md records fork base, sync state, and divergence.
- Prefer small modules, existing GGML buffer/backend interfaces, explicit experimental options, and CPU fallback. Do not reshape public APIs or alter GGUF quant semantics without an ADR and measured need.
- Validate file-derived sizes before arithmetic/allocation; define ownership and async lifetimes; check alignment, corruption, fallback, and concurrency.
- Never claim a performance improvement without benchmark evidence. Compare current upstream, fork with feature disabled, and fork with feature enabled on the same workload.
- Report RAM, VRAM, disk, transfer bandwidth, load/startup, TTFT, prompt throughput, generation throughput, and latency separately. Never hide regressions.
- Every benchmark records hardware, OS/kernel, compiler/build options, driver/CUDA, model/architecture/quant, context, prompt, batch/ubatch, GPU layers, attention, mmap/mlock, KV type, threads, NUMA, and relevant flags.
- Failed and neutral experiments remain documented in docs/experiments and RESULTS.md.
- Each architecture change updates ARCHITECTURE.md, the relevant component page, compatibility notes, and DECISIONS.md/an ADR.
- Update milestone status in MILESTONES.md. GitHub issues define scoped deliverables and include hypothesis, code areas, measurement/acceptance, risks, platforms, dependencies, and results.
- Isolate runtime experiments on exp/<topic> branches. Keep master close to upstream; document sync conflicts in UPSTREAM.md.
- Maintain Windows and Linux wherever practical. Platform calls stay behind narrow adapters; CUDA is optional and CPU inference remains supported.
- Do not change default behavior without repeatable evidence. A disabled fork path must remain close to upstream and regressions must be explained.

## Benchmark workflow
State a falsifiable question, record upstream/fork commits and complete workload manifest, establish upstream and disabled controls, repeat measurements, preserve raw output, report spread and measurement limits, and record the next action. Do not infer tokens/s from compression ratio or PCIe savings alone.

## Current architecture guide
GGML owns backend/device/buffer abstractions and scheduler placement/copies. src/llama-model-loader.* maps GGUF tensors to buffers; src/llama-mmap.* implements mapping, prefetch, and locking; src/llama-kv-cache.* owns KV allocations and slot semantics; src/llama-moe-cache.* and graph construction provide an MoE cache path. CUDA and CPU backends live under ggml/src/ggml-cuda and ggml/src/ggml-cpu. Read current code before changes because upstream contracts move.
