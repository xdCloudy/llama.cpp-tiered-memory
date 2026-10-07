# Performance engineering

Optimize end-to-end inference, not compression ratio alone. The path includes disk/NVMe, page cache and mmap, system RAM, pinned buffers, PCIe, VRAM, GPU caches/registers/shared memory, and compute. Find the limiting stage before changing it.

For each proposal state expected saved bytes, added decode/copy work, granularity, concurrency, and likely effects on TTFT, prompt processing, and token generation. Generation can be weight-bandwidth sensitive; prompt processing has different compute and batching behavior. Do not extrapolate one from the other. Report latency spread and capacity separately.

The disabled fork is a regression control. Resolve or explain material differences from upstream before interpreting an enabled feature. Preserve failed experiments; do not change default paths without repeatable evidence.
