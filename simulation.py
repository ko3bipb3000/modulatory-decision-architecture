# Simple simulation to test state drift and recovery

H = {
    "risk": 0.7,
    "novelty": 0.4,
    "fatigue": 0.2,
    "reward_drive": 0.6
}

baseline = {
    "risk": 0.5,
    "novelty": 0.5,
    "fatigue": 0.2,
    "reward_drive": 0.5
}

actions = {
    "safe_action": {"reward": 0.4, "risk": 0.1},
    "risky_action": {"reward": 0.9, "risk": 0.8},
    "explore_action": {"reward": 0.6, "risk": 0.3}
}


def choose_action(H):
    # simple fast heuristic
    scores = {}
    for a, p in actions.items():
        score = p["reward"]
        score -= H["risk"] * p["risk"]
        score += H["reward_drive"] * 0.2
        score *= (1 - H["fatigue"] * 0.3)
        scores[a] = score
    return max(scores, key=scores.get)


def simulate_outcome(action):
    if action == "safe_action":
        return {"reward": 0.3, "stress": 0.05}
    if action == "risky_action":
        return {"reward": -0.2, "stress": 0.3}
    if action == "explore_action":
        return {"reward": 0.5, "stress": 0.15}


def update_state(H, outcome):
    H["fatigue"] = min(1.0, H["fatigue"] + 0.05)
    H["risk"] = min(1.0, H["risk"] + outcome["stress"] * 0.3)

    if outcome["reward"] > 0:
        H["reward_drive"] = min(1.0, H["reward_drive"] + 0.05)
    else:
        H["reward_drive"] = max(0.0, H["reward_drive"] - 0.05)

    return H


def apply_recovery(H, baseline, rate=0.02):
    for k in H:
        H[k] += rate * (baseline[k] - H[k])
    return H


# -------- RUN --------
steps = 100
use_recovery = True  # переключи False, чтобы увидеть drift

for step in range(steps):
    action = choose_action(H)
    outcome = simulate_outcome(action)
    H = update_state(H, outcome)

    if use_recovery:
        H = apply_recovery(H, baseline)

    if step % 10 == 0:
        print(f"Step {step}")
        print("  Action:", action)
        print("  State:", {k: round(v, 3) for k, v in H.items()})
        print()
