# Unified Modulatory Architecture for Fast-Slow Decision Systems

**Author:** Alexander Paseka  
**Year:** 2026  

---

## Idea

This project proposes a unified decision architecture combining:

- fast (intuitive) decision-making  
- slow (analytical) reasoning  
- global modulatory states (analogous to hormones)  

The goal is not biological replication, but functional equivalence:
- prioritization  
- fast response under uncertainty  
- adaptive re-evaluation  
- override capability  

---

## Motivation

Modern AI systems already use:
- heuristics and policies (fast layer)  
- planning and reasoning (slow layer)  
- uncertainty and risk estimation  

But these are usually:
- fragmented  
- weakly integrated  
- lacking global state control  

This architecture unifies them into a single system.

---

## Core Model

### Global State (H)

H = {risk, novelty, fatigue, reward_drive, ...} ∈ [0,1]

Acts as a global modifier of behavior.

---

### Utility

Each action has base utility: U_i

---

### Modulation

W_i = U_i * M(H, C)

Where:
- H = internal state  
- C = context  
- M = modulation function  

---

### Fast Decision

a_fast = argmax(W_i)

- fast  
- approximate  
- low compute  

---

### Slow Decision

Deeper evaluation:
- comparison  
- planning  
- refinement  

a_slow

---

### Override

if ΔU(a_slow, a_fast) > τ(H):
    final = a_slow
else:
    final = a_fast

---

## Minimal Python Example (v3)

```python
# (code omitted for brevity in file version)
```

---

## Key Properties

- unified control layer  
- dynamic behavior adaptation  
- fast vs accurate trade-off  
- interpretable internal state  

---

## Limitations

- requires tuning  
- possible instability  
- needs safety constraints  

---

## Status

Conceptual architecture.  
Open for discussion and experimentation.

---

## Possible Extensions

This section outlines potential directions for further development and research.

- Baseline recovery to prevent state drift  
- Nonlinear modulation functions  
- Fast-confidence gating for slow-pass activation  
- Slow-to-fast distillation  
- Stagnation detection and forced exploration  

---

## Demo

A simple drift vs recovery demonstration is available:

```bash
python drift_demo.py
```

This illustrates how state variables diverge without recovery and stabilize when recovery is applied.

Run learning demo:

```bash
python learning_demo.py
```
