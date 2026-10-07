# Experiment: EXP-NNN short title

## Question
What single question does this experiment answer?

## Hypothesis
State the expected benefit and the condition under which it could fail.

## Implementation
Commit/branch, feature flag, data path, codec, block size, and fallback.

## Hardware
CPU, RAM, GPU/VRAM, driver, interconnect, NUMA, and power/clock constraints.

## Software
OS/kernel, compiler/build options, CUDA/backend versions, upstream SHA, fork SHA.

## Model and workload
Model, architecture, quant, size, context, prompt, batch/ubatch, GPU layers, flash attention, mmap/mlock/load mode, KV type, threads, seed, cache state, repetitions.

## Baseline
Upstream and fork-disabled measurements with exact commands and raw logs.

## Results
Report median/spread and units. Include RAM, VRAM, disk, transfer bytes, load/TTFT, prompt tok/s, generation tok/s, latency, utilization, faults, ratio, codec throughput, and cache/prefetch metrics as applicable.

## RAM impact
Peak/steady; distinguish resident, committed, mapped, and pinned.

## VRAM impact
Peak/steady and buffers involved.

## Performance impact
Load, TTFT, prompt, generation, tail latency, and source of regressions.

## Interpretation
Separate measured facts from inference. State limitations and confidence.

## Problems
Correctness, build, platform, and measurement issues.

## Conclusion
Positive, neutral, negative, or inconclusive; state exact scope.

## Next action
Continue, narrow, redesign, or stop. Negative results remain in the registry.
