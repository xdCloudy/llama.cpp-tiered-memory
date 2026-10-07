# Windows research notes

Current file-mapping abstractions are in src/llama-mmap.*; inspect the Windows implementation before changing loader paths. Candidate mechanisms include file mapping, VirtualLock, PrefetchVirtualMemory, large pages, and NUMA APIs. They have allocation and working-set implications; measure resident/locked bytes and faults rather than assuming a hint made pages resident.

Compare mmap and non-mmap loading, pageable and CUDA-pinned staging, partial GPU offload, and cold/warm file cache. Capture Windows build, SDK/compiler, CUDA runtime/driver, RAM, pagefile policy, and GPU. Windows is a first-class target. No Windows-specific optimization is accepted without a paired baseline and CPU fallback.
