# Architecture documentation

ARCHITECTURE.md is the current call-path map. GGML owns backend buffers, devices, asynchronous copies, and graph scheduling; the loader owns GGUF-to-tensor placement; memory classes own KV and MoE semantics. Add cross-component details here with an evidence link and upstream SHA because APIs change.
