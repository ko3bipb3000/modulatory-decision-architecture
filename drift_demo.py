# Drift vs Recovery demonstration (console visualization)
# Shows how state variables diverge without recovery
# and stabilize when recovery is applied

steps = 60

# Initial states
H_drift = {"risk": 0.5, "fatigue": 0.2}
H_recov = {"risk": 0.5, "fatigue": 0.2}

history_drift = []
history_recov = []


def run_step(H, recovery_rate=0.0):
    # Simulate accumulation
    H["risk"] = min(1.0, H["risk"] + 0.05)
    H["fatigue"] = min(1.0, H["fatigue"] + 0.03)

    # Apply recovery toward baseline (0.5)
    if recovery_rate > 0:
        for k in H:
            H[k] += recovery_rate * (0.5 - H[k])

    return H.copy()


# Run simulation
for _ in range(steps):
    history_drift.append(run_step(H_drift, 0.0))
    history_recov.append(run_step(H_recov, 0.04))


# Console visualization
print("Risk Comparison:")
print("[D] Drift (no recovery) | [R] With recovery")
print("-" * 70)

for i in range(0, steps, 3):
    d_val = history_drift[i]["risk"]
    r_val = history_recov[i]["risk"]

    line = [" "] * 41
    d_pos = int(d_val * 40)
    r_pos = int(r_val * 40)

    if d_pos == r_pos:
        line[d_pos] = "X"
    else:
        line[d_pos] = "D"
        line[r_pos] = "R"

    print(f"Step {i:02} |{''.join(line)}| (R:{r_val:.2f}, D:{d_val:.2f})")

print("-" * 70)
