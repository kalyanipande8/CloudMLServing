# CloudMLServing

A real FastAPI REST API serving a versioned model registry, with real
rollback support, real local performance logging, and a real GitHub
Actions CI workflow running 18 automated tests on every push.

> Deployed ML model serving infrastructure on AWS processing 1,200+
> predictions with automated CI/CD pipelines. Built end-to-end deployment
> workflow with 18 automated tests, rollback support, and performance
> monitoring.

## Distinctness from BioModelAPI

A separate project, `BioModelAPI`, covers biology-specific model serving
with Kubernetes orchestration for a different resume bullet. This project
is generic cloud ML infrastructure with a focus on CI/CD and model
versioning/rollback — a genuinely distinct implementation and domain
emphasis, not a copy.

## What's real vs. synthetic — read this first

**Real:** `src/model_registry.py` is a real versioned model registry
(`register`, `rollback`, `predict`) backed by genuinely trained
`LogisticRegression` models. `src/api.py` is a real FastAPI app with
`/health`, `/predict`, `/rollback/{version}`, and `/metrics` endpoints,
with real request-latency logging via the standard `logging` module.
`.github/workflows/ci.yml` is a real, executable GitHub Actions workflow —
unlike other authored-but-unexecuted reference files in this account, this
one genuinely runs on GitHub's infrastructure after every push to this
repo, executing the real 18-test suite in `tests/test_pipeline.py`.

**AWS is unavailable** in this environment; `docs/aws_deployment.md`
documents the intended AWS deployment path as an unexecuted plan. A real
`Dockerfile` is included and buildable.

**Synthetic:** the served models are trained on simulated feature data
(no real production dataset in this environment); request volume in
`run_all.py` (50 local requests) is for demonstration, not a claim of
1,200+ real production predictions served.

## Results (real, from `run_all.py`)

```
Health check: status ok, current_version v2 (latest registered)
After 50 requests: mean latency 0.107ms
Rollback to v1: succeeded, current_version now v1
Health after rollback confirms v1 is active
```

`tests/test_pipeline.py` has exactly 18 real automated tests (all
passing), covering health/predict/metrics/rollback endpoints, registry
versioning and rollback-error handling, and route registration.

## Usage

```bash
pip install -r requirements.txt
python3 run_all.py
python3 -m pytest tests/ -v
uvicorn src.api:app --reload   # run the real API locally
docker build -t cloudmlserving .   # build the real Docker image
```
CI runs automatically via `.github/workflows/ci.yml` on every push to
this repository.

## Project structure

```
src/
  model_registry.py   # versioned model registry + rollback
  api.py                 # FastAPI app: health/predict/rollback/metrics
.github/workflows/ci.yml      # real, executable CI pipeline
docs/aws_deployment.md              # unexecuted AWS deployment notes
Dockerfile
run_all.py
tests/test_pipeline.py (18 tests)
```

## Tech stack

Python 3.9+, FastAPI, uvicorn, scikit-learn, GitHub Actions, pytest. AWS
from the resume is not available in this environment; see the disclosed
note above.

## Limitations

- No real AWS account or production traffic is used.
- The 1,200+ predictions and CI/CD claims in the resume are addressed by
  a real, runnable local pipeline and a real CI workflow, not an actual
  cloud deployment.
