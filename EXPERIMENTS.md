# Experiment registry

Every significant experiment gets a report under docs/experiments/ using EXPERIMENT_TEMPLATE.md. Negative and inconclusive reports remain in the registry.

| ID | Question | Status | Report |
|---|---|---|---|
| EXP-001 | Secondary compressibility of GGUF payloads by type, role, and chunk size | planned | docs/experiments/EXP-001-tensor-compressibility.md |
| EXP-002 | MoE expert locality and reuse distance | planned | docs/experiments/EXP-002-moe-locality.md |
| EXP-003 | Packed host-to-CUDA transfer economics | planned; gated on EXP-001 | docs/experiments/EXP-003-packed-pcie-transfer.md |

Reports preserve tested configurations, raw inputs, known gaps, interpretation, and next action. Do not infer inference gains from compression ratio alone.
