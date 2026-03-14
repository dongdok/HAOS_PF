# Phase 6 Approval/Test/Rollback Layer (2026-03-13, Asia/Seoul)

## Objective

Implement operational policy:
- proposal only
- explicit approval
- time-boxed test window (default 7 days)
- rollback switch for batch-level revert

## Implemented Code

- Approval/test/rollback service:
  - `/Users/dy/Desktop/HAOS_Control/src/reco_engine/services/approval_service.py`
- DB schema extension + migration:
  - `/Users/dy/Desktop/HAOS_Control/src/reco_engine/adapters/repository_sqlite.py`
- CLI commands:
  - `/Users/dy/Desktop/HAOS_Control/src/reco_engine/interfaces/cli.py`

## Data Model Additions

### `recommendation_candidate` columns
- `approved_at`
- `test_batch_id`
- `test_start_at`
- `test_end_at`
- `finalized_at`
- `rejection_reason`

### New table: `recommendation_test_batch`
- `status` (`testing|passed|failed|rolled_back`)
- `started_at`
- `ends_at`
- `finalized_at`
- `rollback_reason`

## Command Set

```bash
PYTHONPATH=src python3 -m reco_engine.interfaces.cli approve-candidates \
  --db data/reco_engine.db --candidate-ids 1,2,3

PYTHONPATH=src python3 -m reco_engine.interfaces.cli start-test-batch \
  --db data/reco_engine.db --candidate-ids 1,2,3 --days 7

PYTHONPATH=src python3 -m reco_engine.interfaces.cli finalize-test-batch \
  --db data/reco_engine.db --batch-id 1 --result pass

PYTHONPATH=src python3 -m reco_engine.interfaces.cli rollback-batch \
  --db data/reco_engine.db --batch-id 1 --reason "rollback reason"
```

## Guardrails

- `start-test-batch` accepts only `approved` candidates.
- If zero approved candidates are linked, batch creation is cancelled with explicit error.
- Rollback applies only to candidates in `testing` or `active`.

## Verified State Transition

Validated on real DB:

1. `proposed -> approved`
2. `approved -> testing` (batch created)
3. `testing -> active` (finalize pass)
4. `active -> rolled_back` (rollback command)

Observed records:
- Batch status transitions persisted in `recommendation_test_batch`
- Candidate statuses updated consistently with batch actions

## Integrity Notes

- This layer changes recommendation workflow state only.
- It does not auto-apply HA automation YAML.
- Rollback is explicit and auditable by batch ID + reason.
