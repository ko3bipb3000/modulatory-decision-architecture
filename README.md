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
