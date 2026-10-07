# Platform support

Keep policy and block/index logic portable. OS mapping, page-locking, NUMA, and prefetch operations belong behind existing wrappers or a narrow adapter. Windows and Linux are explicit targets; other platforms retain the ordinary upstream path unless supported and measured.

Initial host availability: Windows, WSL Ubuntu 24.04, CUDA 13.3, RTX 3060 12 GiB. This is not evidence that builds pass. Record compiler, SDK, kernel, and driver with each result. See WINDOWS.md, LINUX.md, CPU.md, and CUDA.md.
