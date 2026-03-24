import random
import matplotlib.pyplot as plt

random.seed(42)

RUNS = 20
STEPS = 100


def get_environment(step):
    if step < 30:
        return {"risk_prob": 0.2}
    elif step < 60:
        return {"risk_prob": 0.7}
    else:
        return {"risk_prob": 0.3}


# ---------- BASELINES ----------
def fsm_threshold(env):
    return "RISKY" if env["risk_prob"] < 0.4 else "SAFE"


def always_safe(_):
    return "SAFE"


def always_risky(_):
    return "RISKY"


# ---------- MDA ----------
def modulatory_agent(env, H):
    safe_score = 1.0
    risky_score = (
        5.0
        - (H["risk"] * env["risk_prob"] * 15.0)
        - (H["fatigue"] * 4.0)
        + (H["reward_drive"] * 2.0)
    )
    return "RISKY" if risky_score > safe_score else "SAFE"


def update_state(H, action, outcome):
    if action == "SAFE":
        H["fatigue"] = max(0.0, H["fatigue"] - 0.08)
        H["risk"] = max(0.1, H["risk"] - 0.02)
        H["reward_drive"] = min(1.0, H["reward_drive"] + 0.01)
    else:
        H["fatigue"] = min(1.0, H["fatigue"] + 0.05)

    if action == "RISKY":
        if outcome < 0:
            H["risk"] = min(1.0, H["risk"] + 0.25)
            H["reward_drive"] = max(0.0, H["reward_drive"] - 0.2)
        else:
            H["reward_drive"] = min(1.0, H["reward_drive"] + 0.05)
            H["risk"] = max(0.1, H["risk"] - 0.01)

    return H


def get_outcome(action, prob):
    if action == "SAFE":
        return 1
    return -15 if random.random() < prob else 7


# ---------- STORAGE ----------
avg_safe = [0] * STEPS
avg_risky = [0] * STEPS
avg_fsm = [0] * STEPS
avg_mda = [0] * STEPS

sample_risk = []
sample_fatigue = []


# ---------- SIMULATION ----------
for run in range(RUNS):
    H = {"risk": 0.3, "fatigue": 0.0, "reward_drive": 0.5}

    total_safe = 0
    total_risky = 0
    total_fsm = 0
    total_mda = 0

    for step in range(STEPS):
        env = get_environment(step)

        a_safe = always_safe(env)
        a_risky = always_risky(env)
        a_fsm = fsm_threshold(env)
        a_mda = modulatory_agent(env, H)

        r_safe = get_outcome(a_safe, env["risk_prob"])
        r_risky = get_outcome(a_risky, env["risk_prob"])
        r_fsm = get_outcome(a_fsm, env["risk_prob"])
        r_mda = get_outcome(a_mda, env["risk_prob"])

        total_safe += r_safe
        total_risky += r_risky
        total_fsm += r_fsm
        total_mda += r_mda

        H = update_state(H, a_mda, r_mda)

        avg_safe[step] += total_safe
        avg_risky[step] += total_risky
        avg_fsm[step] += total_fsm
        avg_mda[step] += total_mda

        if run == 0:
            sample_risk.append(H["risk"])
            sample_fatigue.append(H["fatigue"])


# ---------- AVERAGE ----------
avg_safe = [x / RUNS for x in avg_safe]
avg_risky = [x / RUNS for x in avg_risky]
avg_fsm = [x / RUNS for x in avg_fsm]
avg_mda = [x / RUNS for x in avg_mda]


# ---------- ENV LINE ----------
env_line = [get_environment(s)["risk_prob"] for s in range(STEPS)]


# ---------- PLOT ----------
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

ax1.plot(avg_safe, label="Always SAFE", linestyle=":")
ax1.plot(avg_risky, label="Always RISKY", linestyle=":")
ax1.plot(avg_fsm, label="FSM Threshold", linestyle="--")
ax1.plot(avg_mda, label="MDA", linewidth=2)

ax1.set_title(f"Performance Comparison ({RUNS} runs)")
ax1.set_ylabel("Total Reward")
ax1.legend()
ax1.grid(alpha=0.2)

ax2.plot(sample_risk, label="Internal Risk", color="orange")
ax2.plot(sample_fatigue, label="Fatigue", color="purple")
ax2.fill_between(range(STEPS), env_line, color="grey", alpha=0.1, label="Env Risk")

ax2.set_title("MDA Internal State (Sample Run)")
ax2.set_xlabel("Step")
ax2.set_ylabel("State")
ax2.legend()
ax2.grid(alpha=0.2)

plt.tight_layout()
plt.show()


# ---------- RESULT ----------
print("Final average reward:")
print(f"SAFE:  {avg_safe[-1]:.1f}")
print(f"RISKY: {avg_risky[-1]:.1f}")
print(f"FSM:   {avg_fsm[-1]:.1f}")
print(f"MDA:   {avg_mda[-1]:.1f}")
