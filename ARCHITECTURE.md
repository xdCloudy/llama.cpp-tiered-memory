# Architecture map and integration constraints

This map reflects upstream SHA bd4eeaa047006cb1fe71999fbd11134b5836e167. Refresh it after each upstream sync.

## Current paths inspected
- **GGML backend/buffer:** ggml/include/ggml-backend.h exposes buffer types and allocation, tensor set/get, async tensor copy, devices, events, and scheduler placement/copy callbacks. Backend implementations live in ggml/src/ggml-backend-impl.h and per-backend sources. The scheduler is a seam for movement instrumentation, but does not imply compressed tensors can be consumed directly.
- **GGUF and loader:** ggml/include/gguf.h exposes names, dimensions, types, offsets, and sizes. src/llama-model-loader.* maps metadata into tensor weights, selects buffer types by tensor/layer, initializes mappings, and loads/copies data. It supports lazy row reads for selected tensors.
- **Mapping and host memory:** src/llama-mmap.* wraps files, mappings, range prefetch, and page locking. Loader code uses mappings and backend upload paths; non-mmap uploads can stage through temporary buffers.
- **CUDA/CPU:** ggml/src/ggml-cuda owns device/buffer operations, streams, copies, and quantized kernels. CUDA host-pinned staging already exists. ggml/src/ggml-cpu contains CPU quant kernels, traits, repacking, and architecture variants.
- **KV:** src/llama-kv-cache.* owns cache cells/slots and backend tensors. Recurrent and MSA memory have specialized implementations. KV representation must respect graph access, sequence reuse, sliding windows, and placement.
- **MoE:** src/llama-graph.cpp selects experts and can query llama_moe_cache; src/llama-moe-cache.* already tracks/copies expert groups and reports hits/misses. Measure this before adding another cache.
- **Quantization:** GGUF types select existing GGML block formats and CPU/CUDA kernels. Secondary packing must not reinterpret file-format semantics.

## Candidate seams
1. A standalone profiler reads GGUF metadata and samples or streams tensor payloads without altering inference.
2. Loader experiments can retain semantic tensor/layer identity, but must preserve existing buffer selection and lazy-read behavior.
3. GGML buffers/scheduler can measure or prototype placement/copies; alternate storage needs an explicit read contract, not a fake ordinary tensor pointer.
4. The MoE cache is the narrowest existing semantic cache for expert studies.
5. KV is mutable and distinct from immutable weight caching.

## Design constraint
A smaller file can still increase peak RAM and latency if the loader materializes whole tensors. Every experiment states which representation lives at each tier and when decoded bytes are live. See DESIGN.md and component pages.
