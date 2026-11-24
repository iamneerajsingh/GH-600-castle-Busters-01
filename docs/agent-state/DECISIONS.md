# Decisions log (long-term memory)

Agents must follow these decisions. Only a human may change or remove one.

| ID | Decision | Why | Expires / review |
|---|---|---|---|
| D1 | Game rules stay in physics.py, castle.py, scoring.py. game.py only draws. | Rules can be tested without a screen. | Review 2027-06 |
| D2 | Gravity is 9.8. Do not change it for a feature. | Changing it breaks every level. | Never |
| D3 | No new third-party packages without approval. | Keeps the build small and safe. | Review 2027-06 |
