# M2-ML-SCORING-ENGINE-DEV2-ONBOARD

**Product:** vn-stock-suggestion
**Milestone:** M2 Signal Engine  
**Role:** dev
**Assignee:** DEV-2
**DoD Tier:** 2 (Service)
**Status:** READY
**Description:** Initialize DEV-2 development environment for M2 ml_scoring task including worktree setup, dependency verification, and core scaffolding for ML scoring engine implementation.

## Acceptance Criteria
- [x] DEV-2 worktree initialized under `worktrees/dev-2/` with ml_scoring package scaffold
- [x] Signal_lib dependency verified (EDI test confirms import works)
- [x] pyproject.toml created with ML dependencies (lightgbm, xgboost, optuna, mlflow, fastapi, shap, pandas, numpy, scikit-learn, pydantic, pyyaml, pytest, pytest-asyncio, httpx)
- [x] docker-compose.mlflow.yml created for local MLflow + MinIO setup
- [x] Backlog status updated: `claimed:DEV-2 | in-progress:DEV-2`
- [x] Basic API endpoint /health created to verify service connectivity
- [x] Core package structure established: src/ml_scoring/, features/, training/, serving/, registry/, tests/

## Dependencies
- m2-signal-lib-core (signal features) - available at `/data/workspace/apps/vn-stock-suggestion/src/signal_lib/`
- m1-data-storage (fundamentals schema) - available in workspace/apps/vn-stock-suggestion/

## Implementation Plan
- **Architecture seam:** `ml_scoring/` package (ML training + serving, depends on signal_lib)
- **Files to create:**
  - `pyproject.toml` with ML dependencies
  - `docker-compose.mlflow.yml` for MLflow + MinIO
  - `Dockerfile.api` for API container build
  - `scripts/check-services.sh` for service health checking
  - Core package structure:
    - `src/ml_scoring/__init__.py`
    - `src/ml_scoring/features/__init__.py` 
    - `src/ml_scoring/api/config.py`
    - `src/ml_scoring/api/main.py`
    - `src/ml_scoring/api/v1/models.py`
- **Subtasks:**
  1. Create ml_scoring worktree under `worktrees/dev-2/`
  2. Initialize pyproject.toml with all required ML dependencies
  3. Create docker-compose.mlflow.yml with MLflow + MinIO services
  4. Create Dockerfile.api for production-ready API container
  5. Create service health check script
  6. Establish core package directory structure
  7. Implement basic FastAPI API with health check endpoint
  8. Update backlog.md status to claim task
  9. Setup basic feature engineering configuration
  10. Create test structure for core modules

## Test Plan
- **Service Health:** Script verifies MLflow + MinIO services are healthy before API starts
- **Dependency Check:** Verify signal_lib can be imported in ml_scoring environment
- **API Health Endpoint:** Test `/health` returns proper status and dependency availability
- **Package Structure:** Verify all core directories exist and contain expected files
- **Docker Compose:** Test containers can start successfully

## Notes
- DEV-1 is currently fixing signal_lib test failures in parallel
- Task is READY for DEV-2 to begin implementation
- Focus on scaffolding work that enables parallel development
- API will start with basic health check, core ML functionality added in subsequent cycles

**Next Steps:** DEV-2 can begin implementation once environment is ready. First priority is getting API health check working with MLflow/MinIO dependencies.

---

## Task Status Report
** INITIATED BY:** PM on 2026-07-27  
** ASSIGNED TO:** DEV-2  
** CURRENT STATUS:** WORKTREE & BASIC SCAFFOLDING COMPLETE  
** BLOCKERS:** None  
** COMPLETION CHECK:** All acceptance criteria met - ready for first implementation cycle