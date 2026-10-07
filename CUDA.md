# CUDA research notes

CUDA sources under ggml/src/ggml-cuda implement device/buffer management, streams, asynchronous copies, and quantized kernels. Host-pinned staging helpers already exist. Inspect call paths and synchronization before adding a packed route.

Measure H2D bytes, copy latency/throughput, CPU/GPU decode, kernel occupancy, overlap, VRAM peaks, and tokens/s. Compare CPU decode before transfer, GPU decode after packed transfer, and fused decode/compute only on supported shapes. Source lifetime must extend through async completion; errors and cancellation must not leak pinned buffers. CUDA stays optional and CPU behavior intact.
