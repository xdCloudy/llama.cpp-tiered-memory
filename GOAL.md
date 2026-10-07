# Project goals

## Measurable outcomes
Reproducible workloads should show one or more of: lower peak/steady host RAM or VRAM; larger models or context on fixed hardware; less duplicate/staging memory; fewer page faults or less fragmentation; less host-device traffic; higher effective PCIe throughput; faster model load or first-token latency; or higher prompt/generation throughput for partially offloaded or MoE models.

Capacity and speed are separate claims. Report model fit, RAM, VRAM, disk, transfer bytes, load time, TTFT, prompt tokens/s, generation tokens/s, and latency independently. A memory win that slows decode is a tradeoff, not an unqualified improvement.

## Architecture goals
- Windows and Linux, CUDA as an optional first-class backend, and CPU fallback.
- Modular, opt-in experiments with graceful fallback and upstream-compatible defaults.
- Preserve compact representations as far into the path as measurements and backend kernels permit.
- Use tensor, layer, expert, KV, backend, and lifetime semantics to choose what to pack, move, prefetch, retain, or evict.
- Compare every result against current upstream and feature-disabled fork builds.

## Non-goals
- Generic user-space ZRAM or a literal CRAM hardware port.
- Implicitly changing existing GGUF quantization meanings.
- Lossy compression without explicit opt-in and quality/perplexity measurement.
- Claiming smaller byte streams improve inference without end-to-end evidence.
- Merging experiments into default paths because they compile.
