# Linux research notes

The portable loader wrappers already contain Linux mmap/prefetch/locking behavior. Study src/llama-mmap.cpp and loader ranges first. Candidate knobs include madvise, mlock/mlock2, NUMA, huge pages, page residency, direct I/O, and cgroup pressure; keep them optional.

Benchmark mmap versus buffered/direct reads, faults, lazy tensor access, pinned staging, and partial GPU offload under recorded kernel, filesystem, cgroup, NUMA, compiler, driver, and CUDA versions. WSL is useful for iteration but is not equivalent to bare-metal Linux PCIe or page-cache behavior.
