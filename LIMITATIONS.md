# Known limitations

At project start, no compressed inference format, tier manager, or new backend exists. There are no benchmark results. Environment inventory is incomplete for RAM, exact Windows build, compiler flags, model, and workload. Initial Linux access is WSL; bare-metal results are needed for OS and PCIe claims.

Current upstream already includes mmap/prefetch/locking wrappers, backend buffers and async copies, lazy tensor reads, KV backend allocation, and an MoE cache. These may address some needs. Establish gaps before building parallel infrastructure.
