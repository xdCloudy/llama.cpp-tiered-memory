# Research questions and literature

## Questions
1. What redundancy remains in Q2/IQ2, Q3, Q4, Q5, Q6, Q8, F16, and BF16 payloads?
2. Do results vary by tensor role, layer, expert, or 4 KiB-1 MiB block size?
3. Are bit-plane transforms or quant-block repacking more useful than LZ4/Zstd for random decode and GPU consumption?
4. Can transfer savings cover decode cost, and can GPU decode overlap with compute?
5. What expert locality and reuse distance occur on realistic prompts? Can routes inform timely prefetch?
6. Which KV access patterns permit cold placement without full-per-token decompression?
7. Are pinned host memory, mmap hints, or staging avoidance better than compression?
8. How do Linux/Windows paging and partial GPU offload affect faults, startup, and throughput?
9. Are duplicate CPU/GPU tensors, copies, workspaces, or fragmentation a larger opportunity?

## Literature starting points
Meta's CRAM paper, *CRAM: Efficient Hardware-Based Memory Compression for Bandwidth Enhancement*, studies hardware memory compression and bandwidth, with a bypass scheme when compression is not useful: https://arxiv.org/abs/1807.07685. This fork adapts the motivation, not the hardware mechanism. Meta's Transparent Memory Offloading is relevant to tiering economics but is a fleet/OS system, not an inference implementation: https://engineering.fb.com/2022/06/20/data-infrastructure/transparent-memory-offloading-more-memory-at-a-fraction-of-the-cost-and-power/.

## Method
Start with descriptive profiling; establish upstream controls; isolate one variable. Compression ratio is only a storage metric. Measure decode throughput, random access, cache effects, transfer bytes, full inference, and quality for lossy paths. Preserve workloads and raw outputs.
