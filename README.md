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
# Unified Modulatory Architecture - minimal prototype v3

H = {
    "risk": 0.7,
    "novelty": 0.4,
    "fatigue": 0.2,
    "reward_drive": 0.6
}

actions = {
    "safe_action": {"reward": 0.5, "risk": 0.1},
    "risky_action": {"reward": 0.9, "risk": 0.8},
    "explore_action": {"reward": 0.6, "risk": 0.3}
}

memory = []

def fast_pass(actions, H):
    scores = {}
    for action, params in actions.items():
        score = params["reward"]
        score -= H["risk"] * params["risk"] * 0.5
        score += H["reward_drive"] * 0.2
        score *= (1 - H["fatigue"] * 0.3)
        scores[action] = score
    best = max(scores, key=scores.get)
    return best, scores

def slow_pass(actions, H):
    scores = {}
    for action, params in actions.items():
        reward = params["reward"]
        risk = params["risk"]
        utility = reward
        utility -= risk * H["risk"]
        if action == "explore_action":
            utility += H["novelty"] * 0.4
        utility *= (1 + H["reward_drive"] * 0.3)
        utility *= (1 - H["fatigue"] * 0.5)
        scores[action] = utility
    best = max(scores, key=scores.get)
    return best, scores

def override(a_fast, a_slow, fast_val, slow_val, H):
    threshold = 0.05 + H["fatigue"] * 0.2
    if (slow_val - fast_val) > threshold:
        return a_slow
    return a_fast

def simulate_outcome(action):
    if action == "safe_action":
        return {"success": True, "reward": 0.4, "stress": 0.05}
    if action == "risky_action":
        return {"success": False, "reward": -0.3, "stress": 0.35}
    if action == "explore_action":
        return {"success": True, "reward": 0.5, "stress": 0.15}
    return {"success": False, "reward": 0.0, "stress": 0.0}

def update_state(H, outcome, action):
    new_H = H.copy()
    new_H["fatigue"] = min(1.0, new_H["fatigue"] + 0.08)
    new_H["risk"] = min(1.0, new_H["risk"] + outcome["stress"] * 0.5)
    if outcome["reward"] > 0:
        new_H["reward_drive"] = min(1.0, new_H["reward_drive"] + outcome["reward"] * 0.2)
    else:
        new_H["reward_drive"] = max(0.0, new_H["reward_drive"] + outcome["reward"] * 0.2)
    if action == "explore_action":
        new_H["novelty"] = max(0.0, new_H["novelty"] - 0.1)
    else:
        new_H["novelty"] = min(1.0, new_H["novelty"] + 0.03)
    return new_H

def update_memory(memory, step, action, outcome, H_before, H_after):
    memory.append({
        "step": step,
        "action": action,
        "success": outcome["success"],
        "reward": outcome["reward"],
        "stress": outcome["stress"],
        "state_before": H_before.copy(),
        "state_after": H_after.copy()
    })

steps = 5

for step in range(1, steps + 1):
    H_before = H.copy()
    a_fast, fast_scores = fast_pass(actions, H)
    a_slow, slow_scores = slow_pass(actions, H)
    final_action = override(
        a_fast,
        a_slow,
        fast_scores[a_fast],
        slow_scores[a_slow],
        H
    )
    outcome = simulate_outcome(final_action)
    H = update_state(H, outcome, final_action)
    update_memory(memory, step, final_action, outcome, H_before, H)

    print(f"Step {step}")
    print("  Fast decision:", a_fast, round(fast_scores[a_fast], 3))
    print("  Slow decision:", a_slow, round(slow_scores[a_slow], 3))
    print("  Final action :", final_action)
    print("  Outcome      :", outcome)
    print("  New state    :", {k: round(v, 3) for k, v in H.items()})
    print()

print("Memory log:")
for item in memory:
    print(item)
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
