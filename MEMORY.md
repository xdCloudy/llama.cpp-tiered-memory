# Memory model and accounting

Distinguish virtual address space, committed bytes, resident physical pages, file-backed pages, pinned/locked host memory, backend allocations, staging, and VRAM. Shared mmap pages may appear in process statistics without being private physical memory. On CUDA, account for device allocations and host staging separately.

Classify data by semantics and lifetime: immutable weights; individual MoE expert matrices; mutable KV cells; activation/workspace buffers; temporary staging; metadata. Safe eviction, mutability, reuse, and decode requirements differ. A packed cache needs a hard budget and ownership rules so eviction cannot invalidate in-flight work.

Measure existing mmap/mlock/prefetch, lazy tensor reads, per-layer backend buffer assignment, model duplication, scheduler copies, pinned staging, KV allocation, and allocator fragmentation before adding a manager.
