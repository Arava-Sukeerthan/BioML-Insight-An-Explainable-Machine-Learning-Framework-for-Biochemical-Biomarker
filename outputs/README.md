# outputs/

Added in PROTOCOL-DRAFT-002 (2026-10-24). No experiment has been run, and this folder holds no results.

**The repository is public.** Outputs are split by whether they can identify participants:

| Location | Content | In Git? |
|---|---|---|
| `outputs/aggregate/` | Aggregate tables and figures intended for publication: counts, metrics with CIs, calibration summaries, global importance. **No row may describe a single participant, and no column may hold a participant identifier (e.g., `SEQN`)** | Yes. This is the only output location meant for committed results |
| `outputs/participant_level/` | Per-participant predictions, SHAP values, conformal prediction sets, fold assignments | **No** (ignored) |
| `outputs/models/`, `/models/` | Fitted models and serialized objects. These can contain training rows (e.g., a k-NN training set or SVM support vectors) | **No** (ignored) |
| `outputs/tmp/` | Scratch output | **No** (ignored) |

The rules are in `/.gitignore`. The checks are in `tests/data_protection/test_data_protection.py`:
```
python3 -I -m unittest discover -s tests/data_protection -v
```
The checks reduce, but cannot remove, the risk of committing participant-level data. Their docstring lists what they cannot detect. Small-cell aggregate tables can still disclose information; that is a reporting judgement, not something these checks test.
