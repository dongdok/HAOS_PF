from __future__ import annotations

import argparse
import json
import tomllib
from datetime import datetime, timedelta
from pathlib import Path

from reco_engine.adapters.ha_client import HAClient, HAConnection
from reco_engine.adapters.repository_sqlite import SQLiteRepository
from reco_engine.core.policy import EnginePolicy
from reco_engine.services.collect_service import CollectService
from reco_engine.services.detection_service import DetectionService
from reco_engine.services.kpi_service import KpiService
from reco_engine.services.proposal_service import ProposalService
from reco_engine.services.intervention_service import InterventionService
from reco_engine.services.approval_service import ApprovalService
from reco_engine.services.dashboard_card_service import DashboardCardService
from reco_engine.services.feedback_service import FeedbackService
from reco_engine.services.ops_summary_service import OpsSummaryService
from reco_engine.services.pipeline_service import PipelineService
from reco_engine.services.validation_service import ValidationService


def _load_policy(policy_path: Path) -> EnginePolicy:
    config = tomllib.loads(policy_path.read_text(encoding="utf-8"))
    values = config["policy"]
    return EnginePolicy(
        manual_repeat_min_count=int(values["manual_repeat_min_count"]),
        cancel_window_minutes=int(values["cancel_window_minutes"]),
        conflict_window_minutes=int(values["conflict_window_minutes"]),
        movement_repeat_min_count=int(values["movement_repeat_min_count"]),
        movement_window_minutes=int(values["movement_window_minutes"]),
        env_pattern_min_count=int(values["env_pattern_min_count"]),
        env_response_window_minutes=int(values["env_response_window_minutes"]),
        door_pattern_min_count=int(values["door_pattern_min_count"]),
        door_pattern_window_minutes=int(values["door_pattern_window_minutes"]),
        test_window_days=int(values["test_window_days"]),
        min_confidence_to_propose=float(values["min_confidence_to_propose"]),
    )


def _load_toml(path: Path) -> dict:
    return tomllib.loads(path.read_text(encoding="utf-8"))


def _parse_candidate_ids(value: str) -> list[int]:
    ids = [part.strip() for part in value.split(",") if part.strip()]
    return [int(item) for item in ids]


def _measurement_entity_ids(canonical: dict) -> list[str]:
    specs = canonical.get("required_measurement_entities")
    if not isinstance(specs, list):
        return []
    entity_ids: list[str] = []
    for spec in specs:
        if not isinstance(spec, dict):
            continue
        entity_id = spec.get("entity_id")
        if isinstance(entity_id, str) and entity_id:
            entity_ids.append(entity_id)
    return list(dict.fromkeys(entity_ids))


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="reco-engine")
    sub = parser.add_subparsers(dest="command", required=True)

    init_db = sub.add_parser("init-db")
    init_db.add_argument("--db", required=True, type=Path)

    collect = sub.add_parser("collect-logbook")
    collect.add_argument("--db", required=True, type=Path)
    collect.add_argument("--ha-url", required=True)
    collect.add_argument("--ha-token", required=True)
    collect.add_argument("--hours", required=True, type=int)
    collect.add_argument("--canonical", required=True, type=Path)

    detect = sub.add_parser("detect")
    detect.add_argument("--db", required=True, type=Path)
    detect.add_argument("--policy", required=True, type=Path)

    propose = sub.add_parser("propose")
    propose.add_argument("--db", required=True, type=Path)
    propose.add_argument("--policy", required=True, type=Path)

    approve = sub.add_parser("approve-candidates")
    approve.add_argument("--db", required=True, type=Path)
    approve.add_argument("--candidate-ids", required=True)

    start_test = sub.add_parser("start-test-batch")
    start_test.add_argument("--db", required=True, type=Path)
    start_test.add_argument("--candidate-ids", required=True)
    start_test.add_argument("--days", required=True, type=int)

    finalize = sub.add_parser("finalize-test-batch")
    finalize.add_argument("--db", required=True, type=Path)
    finalize.add_argument("--batch-id", required=True, type=int)
    finalize.add_argument("--result", required=True, choices=["pass", "fail"])
    finalize.add_argument("--reason", required=False, default="")

    rollback = sub.add_parser("rollback-batch")
    rollback.add_argument("--db", required=True, type=Path)
    rollback.add_argument("--batch-id", required=True, type=int)
    rollback.add_argument("--reason", required=True)

    intervene = sub.add_parser("enrich-interventions")
    intervene.add_argument("--db", required=True, type=Path)
    intervene.add_argument("--window-minutes", required=True, type=int)

    vcanon = sub.add_parser("validate-canonical")
    vcanon.add_argument("--ha-url", required=True)
    vcanon.add_argument("--ha-token", required=True)
    vcanon.add_argument("--canonical", required=True, type=Path)

    vutil = sub.add_parser("validate-utility")
    vutil.add_argument("--ha-url", required=True)
    vutil.add_argument("--ha-token", required=True)
    vutil.add_argument("--canonical", required=True, type=Path)

    kpi = sub.add_parser("kpi")
    kpi.add_argument("--db", required=True, type=Path)
    kpi.add_argument("--monthly-energy-kwh", required=True, type=float)

    kpi_auto = sub.add_parser("kpi-auto")
    kpi_auto.add_argument("--db", required=True, type=Path)
    kpi_auto.add_argument("--ha-url", required=True)
    kpi_auto.add_argument("--ha-token", required=True)
    kpi_auto.add_argument("--canonical", required=True, type=Path)

    ops_summary = sub.add_parser("ops-summary")
    ops_summary.add_argument("--db", required=True, type=Path)

    dashboard_cards = sub.add_parser("dashboard-cards")
    dashboard_cards.add_argument("--db", required=True, type=Path)
    dashboard_cards.add_argument("--output", required=False, type=Path)

    run_cycle = sub.add_parser("run-daily-cycle")
    run_cycle.add_argument("--db", required=True, type=Path)
    run_cycle.add_argument("--ha-url", required=True)
    run_cycle.add_argument("--ha-token", required=True)
    run_cycle.add_argument("--policy", required=True, type=Path)
    run_cycle.add_argument("--canonical", required=True, type=Path)
    run_cycle.add_argument("--collect-hours", required=True, type=int)
    run_cycle.add_argument("--intervention-window-minutes", required=True, type=int)

    ingest_feedback = sub.add_parser("ingest-conflict-feedback")
    ingest_feedback.add_argument("--db", required=True, type=Path)

    return parser


def main() -> None:
    args = _parser().parse_args()

    if args.command == "init-db":
        repo = SQLiteRepository(db_path=args.db)
        repo.initialize()
        print("initialized")
        return

    if args.command == "collect-logbook":
        repo = SQLiteRepository(db_path=args.db)
        repo.initialize()
        ha = HAClient(
            HAConnection(
                base_url=args.ha_url,
                token=args.ha_token,
            )
        )
        canonical = _load_toml(args.canonical)
        now = datetime.now().astimezone()
        start = now - timedelta(hours=args.hours)
        summary = CollectService(ha_client=ha, repository=repo).collect_logbook_window(
            start_time=start,
            end_time=now,
            measurement_entity_ids=_measurement_entity_ids(canonical),
        )
        print(
            json.dumps(
                {
                    "inserted": summary.inserted,
                    "rejected": summary.rejected,
                    "rejected_reasons": summary.rejected_reasons,
                },
                ensure_ascii=False,
            )
        )
        return

    if args.command == "detect":
        policy = _load_policy(args.policy)
        findings = DetectionService(db_path=args.db, policy=policy).run()
        print(json.dumps(findings, ensure_ascii=False, indent=2))
        return

    if args.command == "propose":
        policy = _load_policy(args.policy)
        repo = SQLiteRepository(db_path=args.db)
        findings = DetectionService(db_path=args.db, policy=policy).run()
        inserted = ProposalService(repository=repo, policy=policy).persist_proposals(findings)
        print(inserted)
        return

    if args.command == "approve-candidates":
        SQLiteRepository(db_path=args.db).initialize()
        svc = ApprovalService(db_path=args.db)
        summary = svc.approve_candidates(_parse_candidate_ids(args.candidate_ids))
        print(summary.updated)
        return

    if args.command == "start-test-batch":
        SQLiteRepository(db_path=args.db).initialize()
        svc = ApprovalService(db_path=args.db)
        summary = svc.start_test_batch(
            candidate_ids=_parse_candidate_ids(args.candidate_ids),
            test_days=args.days,
        )
        print(
            json.dumps(
                {
                    "batch_id": summary.batch_id,
                    "linked_candidates": summary.linked_candidates,
                    "started_at": summary.started_at,
                    "ends_at": summary.ends_at,
                },
                ensure_ascii=False,
            )
        )
        return

    if args.command == "finalize-test-batch":
        SQLiteRepository(db_path=args.db).initialize()
        svc = ApprovalService(db_path=args.db)
        summary = svc.finalize_test_batch(
            batch_id=args.batch_id,
            passed=args.result == "pass",
            reason=args.reason or None,
        )
        print(
            json.dumps(
                {
                    "batch_id": summary.batch_id,
                    "updated_candidates": summary.updated_candidates,
                    "new_batch_status": summary.new_batch_status,
                },
                ensure_ascii=False,
            )
        )
        return

    if args.command == "rollback-batch":
        SQLiteRepository(db_path=args.db).initialize()
        svc = ApprovalService(db_path=args.db)
        summary = svc.rollback_batch(batch_id=args.batch_id, reason=args.reason)
        print(
            json.dumps(
                {
                    "batch_id": summary.batch_id,
                    "updated_candidates": summary.updated_candidates,
                    "new_batch_status": summary.new_batch_status,
                },
                ensure_ascii=False,
            )
        )
        return

    if args.command == "enrich-interventions":
        repo = SQLiteRepository(db_path=args.db)
        summary = InterventionService(db_path=args.db, repository=repo).apply_manual_override_rule(
            window_minutes=args.window_minutes
        )
        print(summary.updated_events)
        return

    if args.command == "validate-canonical":
        config = _load_toml(args.canonical)
        ha = HAClient(HAConnection(base_url=args.ha_url, token=args.ha_token))
        result = ValidationService(ha_client=ha).validate_canonical_entities(config)
        print(
            json.dumps(
                {"ok": result.ok, "errors": result.errors, "warnings": result.warnings},
                ensure_ascii=False,
                indent=2,
            )
        )
        if not result.ok:
            raise SystemExit(2)
        return

    if args.command == "validate-utility":
        config = _load_toml(args.canonical)
        ha = HAClient(HAConnection(base_url=args.ha_url, token=args.ha_token))
        result = ValidationService(ha_client=ha).validate_utility_meter_health(config)
        print(
            json.dumps(
                {"ok": result.ok, "errors": result.errors, "warnings": result.warnings},
                ensure_ascii=False,
                indent=2,
            )
        )
        if not result.ok:
            raise SystemExit(2)
        return

    if args.command == "kpi":
        repo = SQLiteRepository(db_path=args.db)
        repo.initialize()
        snapshot = KpiService(db_path=args.db, repository=repo).compute_and_store(
            monthly_energy_kwh=args.monthly_energy_kwh
        )
        print(
            json.dumps(
                {
                    "measured_at": snapshot.measured_at.isoformat(),
                    "manual_ops_total": snapshot.manual_ops_total,
                    "automation_cancel_rate": snapshot.automation_cancel_rate,
                    "unnecessary_on_minutes": snapshot.unnecessary_on_minutes,
                    "monthly_energy_kwh": snapshot.monthly_energy_kwh,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return

    if args.command == "kpi-auto":
        repo = SQLiteRepository(db_path=args.db)
        repo.initialize()
        ha = HAClient(HAConnection(base_url=args.ha_url, token=args.ha_token))
        canonical = _load_toml(args.canonical)
        kpi_service = KpiService(db_path=args.db, repository=repo)
        monthly_entity = kpi_service.resolve_monthly_energy_entity(canonical)
        snapshot = kpi_service.compute_and_store_auto(
            ha_client=ha,
            canonical_config=canonical,
        )
        print(
            json.dumps(
                {
                    "source_entity_id": monthly_entity,
                    "measured_at": snapshot.measured_at.isoformat(),
                    "manual_ops_total": snapshot.manual_ops_total,
                    "automation_cancel_rate": snapshot.automation_cancel_rate,
                    "unnecessary_on_minutes": snapshot.unnecessary_on_minutes,
                    "monthly_energy_kwh": snapshot.monthly_energy_kwh,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return

    if args.command == "ops-summary":
        SQLiteRepository(db_path=args.db).initialize()
        summary = OpsSummaryService(db_path=args.db).build()
        print(
            json.dumps(
                {
                    "review_now": summary.review_now,
                    "keep_good": summary.keep_good,
                    "recommend_new": summary.recommend_new,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return

    if args.command == "dashboard-cards":
        SQLiteRepository(db_path=args.db).initialize()
        summary = OpsSummaryService(db_path=args.db).build()
        cards = DashboardCardService().build(summary)
        payload = {
            "cards": cards.to_list(),
        }
        if args.output is not None:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(
                json.dumps(payload, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return

    if args.command == "run-daily-cycle":
        repo = SQLiteRepository(db_path=args.db)
        repo.initialize()
        ha = HAClient(HAConnection(base_url=args.ha_url, token=args.ha_token))
        policy = _load_policy(args.policy)
        canonical = _load_toml(args.canonical)
        summary = PipelineService(
            db_path=args.db,
            ha_client=ha,
            repository=repo,
            policy=policy,
            canonical_config=canonical,
        ).run_daily_cycle(
            collect_hours=args.collect_hours,
            intervention_window_minutes=args.intervention_window_minutes,
        )
        print(
            json.dumps(
                {
                    "collected_inserted": summary.collected_inserted,
                    "collected_rejected": summary.collected_rejected,
                    "collected_rejected_reasons": summary.collected_rejected_reasons,
                    "interventions_updated": summary.interventions_updated,
                    "feedback_ingested": summary.feedback_ingested,
                    "proposals_inserted": summary.proposals_inserted,
                    "findings": summary.findings,
                    "monthly_energy_entity_id": summary.monthly_energy_entity_id,
                    "monthly_energy_kwh": summary.monthly_energy_kwh,
                    "kpi_measured_at": summary.kpi_measured_at,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return

    if args.command == "ingest-conflict-feedback":
        repo = SQLiteRepository(db_path=args.db)
        repo.initialize()
        svc = FeedbackService(db_path=args.db, repository=repo)
        summary = svc.ingest_from_event_log()
        print(
            json.dumps(
                {
                    "inserted": summary.inserted,
                    "skipped": summary.skipped,
                    "latest_verdict_map": svc.latest_verdict_map(),
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return

    raise RuntimeError(f"unsupported command: {args.command}")


if __name__ == "__main__":
    main()
