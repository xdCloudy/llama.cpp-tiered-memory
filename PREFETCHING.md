# Prefetching and overlap

Candidates include next-layer weights, predicted MoE experts, and upcoming storage blocks. Existing model mapping prefetch and backend async copy/scheduler mechanisms are baselines. Do not assume useful bytes are known early enough to overlap.

Measure prediction accuracy, lead time, useful/wasted bytes, cache displacement, copy/decode duration, synchronization stalls, and full inference. A successful pipeline overlaps compute N with transfer/decode N+1 while respecting stream dependencies, buffer lifetime, and budget. Start with trace replay before changing runtime scheduling.
