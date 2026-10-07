# Upstream relationship

- Upstream: https://github.com/ggml-org/llama.cpp.git (remote: upstream)
- Fork: https://github.com/xdCloudy/llama.cpp-tiered-memory.git (remote: origin)
- Base/default branch: master
- Initial upstream SHA: bd4eeaa047006cb1fe71999fbd11134b5836e167
- Initial sync date: 2026-10-07
- Initial divergence: documentation and experiment scaffolding only; no runtime patch yet.

The fork was created from current upstream. Both fork HEAD and upstream/master were verified at the recorded SHA after upstream moved during initial discovery. Before syncing, fetch both remotes, record new SHAs, inspect merge conflicts in loader/backend/graph areas, and update this file and CHANGELOG.md.

## Conflict-sensitive areas
Likely sensitive paths include ggml/include/ggml-backend.h, ggml/src/ggml-backend*, src/llama-model-loader.*, src/llama-mmap.*, src/llama-graph.cpp, src/llama-moe-cache.*, and src/llama-kv-cache.*. Keep early prototypes in new files/tools and isolated branches where possible.
