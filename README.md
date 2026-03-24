🧠 Modulatory Decision Architecture (MDA)

MDA is a lightweight decision-making architecture that combines: - fast
(heuristic) decisions
- slow (analytical) evaluation
- global modulatory state (risk, fatigue, reward drive)

Unlike Finite State Machines (FSM), MDA adapts behavior using internal
state variables rather than fixed thresholds.

------------------------------------------------------------------------

🚀 Key Advantages over FSM

Decision Stability
MDA reduces high-frequency switching by acting as a low-pass filter over
noisy environments.

Homeostasis
Internal variables (fatigue, reward drive) enable balance between
exploration, risk-taking, and recovery.

Context Memory
Past outcomes influence future behavior through internal state, without
retraining.

------------------------------------------------------------------------

## 🧩 Potential Applications

MDA is most useful in systems where:
- environment is uncertain
- strict rules (FSM) are too rigid
- full RL is too heavy

### 1. Service Robotics
Robots interacting with humans.

MDA allows modulation of behavior (e.g. caution, smoothness) based on context:
→ safer and more natural interaction

---

### 2. Autonomous Exploration (Drones / Rovers)
Agents operating without constant supervision.

Internal state (e.g. energy, risk) dynamically shifts priorities:
→ exploration → survival without hard switches

---

### 3. AI Assistants (Stateful Behavior)
Current assistants are stateless per request.

MDA introduces internal modulation:
→ response style adapts to interaction history

---

### 4. Training Simulations
(Military, medical, etc.)

NPC behavior becomes state-driven instead of scripted:
→ panic, hesitation, overconfidence

---

### 5. Distributed Systems (Traffic, Logistics)
Instead of rigid rules per node:

Global modulators adjust priorities system-wide:
→ smoother adaptation under load

---

## 📌 Why MDA

- Scales linearly with added state (vs combinatorial FSM explosion)
- Reduces decision noise via internal filtering
- Enables adaptive behavior without training loops

------------------------------------------------------------------------

📊 Benchmark (comparison_visual.py)

Run: python comparison_visual.py

------------------------------------------------------------------------

🛠 Usage

git clone
https://github.com/ko3bipb3000/modulatory-decision-architecture.git cd
modulatory-decision-architecture

python drift_demo.py python learning_demo.py python comparison_visual.py

------------------------------------------------------------------------

📌 Concept

Decision = f(Environment, Internal State)

------------------------------------------------------------------------

⚠️ Status

Conceptual architecture + simulation demos.

------------------------------------------------------------------------

👤 Author

Alexander Paseka
