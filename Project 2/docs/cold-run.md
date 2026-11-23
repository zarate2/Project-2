# Cold-run record

## Automated local isolation check

The checker copies this project without neighboring labs, runs `python3 run.py` inside that copy, and compares generated output with the working baseline. It records the command, time, exit code, elapsed seconds, result path and hashes in [cold-run.json](../outputs/cold-run.json), with [stdout](../outputs/cold-run.txt). It uses the existing system Python and performs no new dependency installation.

The interactive app is separately exercised by Streamlit AppTest using the installed dependency environment. That validates control behavior but does not claim a fresh dependency installation or user study.
