# learning_demo.py
# Minimal demonstration of fast <- slow adaptation

H = {
    "risk": 0.6,
    "reward_drive": 0.5,
    "fatigue": 0.2
}

actions = {
    "safe_action": {"reward": 0.5, "risk": 0.1},
    "risky_action": {"reward": 0.9, "risk": 0.8},
    "balanced_action": {"reward": 0.7, "risk": 0.4}
}

# Fast layer has adjustable weights
fast_weights = {
    "reward_weight": 1.0,
    "risk_weight": 0.5,
    "drive_weight": 0.2,
    "fatigue_weight": 0.3
}


def fast_pass(actions, H, fast_weights):
    scores = {}

    for action, params in actions.items():
        score = 0.0
        score += params["reward"] * fast_weights["reward_weight"]
        score -= H["risk"] * params["risk"] * fast_weights["risk_weight"]
        score += H["reward_drive"] * fast_weights["drive_weight"]
        score -= H["fatigue"] * fast_weights["fatigue_weight"]
        scores[action] = score

    best = max(scores, key=scores.get)
    return best, scores


def slow_pass(actions, H):
    scores = {}

    for action, params in actions.items():
        utility = params["reward"]
        utility -= H["risk"] * params["risk"] * 1.0

        # balanced action gets slight bonus under moderate risk
        if action == "balanced_action" and 0.4 <= H["risk"] <= 0.8:
            utility += 0.15

        # risky action is punished more strongly under fatigue
        if action == "risky_action":
            utility -= H["fatigue"] * 0.2

        scores[action] = utility

    best = max(scores, key=scores.get)
    return best, scores


def update_fast_weights(fast_weights, fast_action, slow_action):
    # If slow and fast agree, no update needed
    if fast_action == slow_action:
        return fast_weights

    # If slow prefers safer/balanced choice over risky one,
    # increase fast sensitivity to risk slightly
    if slow_action in ["safe_action", "balanced_action"] and fast_action == "risky_action":
        fast_weights["risk_weight"] += 0.05

    # If slow prefers reward-rich action over too conservative choice,
    # increase reward sensitivity slightly
    if slow_action in ["risky_action", "balanced_action"] and fast_action == "safe_action":
        fast_weights["reward_weight"] += 0.03

    return fast_weights


print("Initial fast weights:", fast_weights)
print("-" * 60)

for step in range(1, 11):
    fast_action, fast_scores = fast_pass(actions, H, fast_weights)
    slow_action, slow_scores = slow_pass(actions, H)

    fast_weights = update_fast_weights(fast_weights, fast_action, slow_action)

    print(f"Step {step}")
    print("  Fast action:", fast_action, "| score:", round(fast_scores[fast_action], 3))
    print("  Slow action:", slow_action, "| score:", round(slow_scores[slow_action], 3))
    print("  Updated weights:", {k: round(v, 3) for k, v in fast_weights.items()})
    print()
