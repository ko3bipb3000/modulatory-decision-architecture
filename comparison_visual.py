import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)


# --------------------------------------------------
# Environment
# --------------------------------------------------
def generate_environment(steps=200):
    t = np.arange(steps)

    # Volatile environment with regime changes + noise
    env_risk = 0.3 + 0.4 * (np.sin(t / 10) > 0).astype(float)
    env_risk += np.random.normal(0, 0.05, steps)
    env_risk = np.clip(env_risk, 0, 1)

    return t, env_risk


# --------------------------------------------------
# Agents
# --------------------------------------------------
def run_fsm(env_risk, threshold=0.4):
    actions = []
    rewards = []
    total = 0
    cumulative = []

    for r in env_risk:
        # 1 = SAFE, 0 = RISKY
        action = 1 if r >= threshold else 0
        actions.append(action)

        if action == 1:  # SAFE
            reward = 1
        else:  # RISKY
            reward = -12 if np.random.rand() < r else 6

        rewards.append(reward)
        total += reward
        cumulative.append(total)

    return np.array(actions), np.array(rewards), np.array(cumulative)


def run_mda(env_risk):
    actions = []
    rewards = []
    total = 0
    cumulative = []

    internal_fear = 0.3
    fatigue = 0.0
    reward_drive = 0.5

    fear_hist = []
    fatigue_hist = []
    drive_hist = []

    for r in env_risk:
        safe_score = 1.0
        risky_score = (
            5.0
            - (internal_fear * r * 12.0)
            - (fatigue * 3.0)
            + (reward_drive * 2.0)
        )

        action = 0 if risky_score > safe_score else 1
        actions.append(action)

        if action == 1:  # SAFE
            reward = 1
            fatigue = max(0.0, fatigue - 0.05)
            internal_fear = max(0.1, internal_fear - 0.02)
            reward_drive = min(1.0, reward_drive + 0.01)
        else:  # RISKY
            reward = -12 if np.random.rand() < r else 6
            fatigue = min(1.0, fatigue + 0.03)

            if reward < 0:
                internal_fear = min(1.0, internal_fear + 0.08)
                reward_drive = max(0.0, reward_drive - 0.08)
            else:
                internal_fear = max(0.1, internal_fear - 0.01)
                reward_drive = min(1.0, reward_drive + 0.03)

        rewards.append(reward)
        total += reward
        cumulative.append(total)

        fear_hist.append(internal_fear)
        fatigue_hist.append(fatigue)
        drive_hist.append(reward_drive)

    return (
        np.array(actions),
        np.array(rewards),
        np.array(cumulative),
        np.array(fear_hist),
        np.array(fatigue_hist),
        np.array(drive_hist),
    )


# --------------------------------------------------
# Simulation
# --------------------------------------------------
steps = 200
t, env_risk = generate_environment(steps)

fsm_actions, fsm_rewards, fsm_cum = run_fsm(env_risk)
mda_actions, mda_rewards, mda_cum, fear_hist, fatigue_hist, drive_hist = run_mda(env_risk)

fsm_switches = np.sum(np.diff(fsm_actions) != 0)
mda_switches = np.sum(np.diff(mda_actions) != 0)

fsm_total = fsm_cum[-1]
mda_total = mda_cum[-1]

fsm_penalties = np.sum(fsm_rewards < 0)
mda_penalties = np.sum(mda_rewards < 0)


# --------------------------------------------------
# Visualization
# --------------------------------------------------
fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(12, 12), sharex=True)

# 1. Environment
ax1.plot(t, env_risk, alpha=0.7, label="Environment risk")
ax1.axhline(0.4, linestyle="--", alpha=0.7, label="FSM threshold")
ax1.set_title("Environment Dynamics")
ax1.set_ylabel("Risk")
ax1.legend()
ax1.grid(alpha=0.3)

# 2. Actions
ax2.step(t, fsm_actions, where="post", label=f"FSM actions (switches={fsm_switches})", linestyle="--")
ax2.step(t, mda_actions, where="post", label=f"MDA actions (switches={mda_switches})", linewidth=2)
ax2.set_title("Action Switching Comparison")
ax2.set_ylabel("Action (1=SAFE, 0=RISKY)")
ax2.legend()
ax2.grid(alpha=0.3)

# 3. Cumulative reward
ax3.plot(t, fsm_cum, label=f"FSM reward (final={fsm_total})", linestyle="--")
ax3.plot(t, mda_cum, label=f"MDA reward (final={mda_total})", linewidth=2)
ax3.set_title("Cumulative Reward")
ax3.set_ylabel("Total reward")
ax3.legend()
ax3.grid(alpha=0.3)

# 4. Internal state
ax4.plot(t, fear_hist, label="Internal fear")
ax4.plot(t, fatigue_hist, label="Fatigue")
ax4.plot(t, drive_hist, label="Reward drive")
ax4.fill_between(t, 0, env_risk, alpha=0.1, label="Environment risk")
ax4.set_title("MDA Internal Modulators")
ax4.set_xlabel("Steps")
ax4.set_ylabel("State value")
ax4.legend()
ax4.grid(alpha=0.3)

info_text = (
    f"FSM total reward: {fsm_total}\n"
    f"MDA total reward: {mda_total}\n"
    f"FSM switches: {fsm_switches}\n"
    f"MDA switches: {mda_switches}\n"
    f"FSM penalties: {fsm_penalties}\n"
    f"MDA penalties: {mda_penalties}"
)

fig.text(
    0.78,
    0.02,
    info_text,
    fontsize=10,
    bbox=dict(facecolor="white", alpha=0.85)
)

plt.tight_layout()
plt.savefig("mda_vs_fsm_comparison.png", dpi=300)
plt.show()
