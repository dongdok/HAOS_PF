#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sqlite3
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass(frozen=True)
class SnapshotInput:
    db_path: Path
    lovelace_path: Path
    dashboard_cards_path: Path
    output_path: Path


def _query_one(conn: sqlite3.Connection, sql: str) -> int:
    row = conn.execute(sql).fetchone()
    if not row:
        return 0
    return int(row[0] or 0)


def _query_pairs(conn: sqlite3.Connection, sql: str) -> list[tuple[str, int]]:
    rows = conn.execute(sql).fetchall()
    return [(str(k), int(v)) for k, v in rows]


def _load_lovelace_stats(path: Path) -> dict:
    if not path.exists():
        return {"exists": False, "views": 0, "sections": 0, "cards": 0, "view_types": {}}
    data = json.loads(path.read_text(encoding="utf-8"))
    views = data.get("views", [])
    section_count = 0
    card_count = 0
    view_types: dict[str, int] = {}
    for view in views:
        view_type = str(view.get("type", "masonry"))
        view_types[view_type] = view_types.get(view_type, 0) + 1
        sections = view.get("sections") or []
        section_count += len(sections)
        if sections:
            for section in sections:
                card_count += len(section.get("cards") or [])
        else:
            card_count += len(view.get("cards") or [])
    return {
        "exists": True,
        "views": len(views),
        "sections": section_count,
        "cards": card_count,
        "view_types": view_types,
    }


def _load_dashboard_card_titles(path: Path) -> list[str]:
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    cards = data.get("cards", [])
    titles: list[str] = []
    for card in cards:
        title = card.get("title")
        if isinstance(title, str) and title.strip():
            titles.append(title.strip())
    return titles


def _build_markdown(payload: dict) -> str:
    now = datetime.now().astimezone().isoformat()
    actor = payload["actor_counts"]
    result = payload["result_counts"]
    candidates = payload["candidate_counts"]
    feedback = payload["feedback_counts"]
    lovelace = payload["lovelace"]

    lines: list[str] = []
    lines.append("# HAOS_Control — 라이브 포트폴리오 스냅샷")
    lines.append("")
    lines.append(f"- 생성 시각: {now}")
    lines.append(f"- DB: `{payload['db_path']}`")
    lines.append(f"- Lovelace: `{payload['lovelace_path']}`")
    lines.append("")
    lines.append("## 1) 추천 엔진 운영 지표")
    lines.append("")
    lines.append(f"- 이벤트 총량: **{payload['event_total']}건**")
    lines.append(f"- 자동화 액션: **{actor.get('automation', 0)}건**")
    lines.append(f"- 수동 액션: **{actor.get('manual', 0)}건**")
    lines.append(f"- 시스템 액션: **{actor.get('system', 0)}건**")
    lines.append(f"- 성공: **{result.get('success', 0)}건**, 취소: **{result.get('cancelled', 0)}건**, 실패: **{result.get('failed', 0)}건**")
    lines.append("")
    lines.append("## 2) 추천 후보/피드백 상태")
    lines.append("")
    lines.append(f"- 추천 후보 총량: **{payload['candidate_total']}건**")
    lines.append(f"- 후보 상태 분포: `proposed={candidates.get('proposed', 0)}`, `approved={candidates.get('approved', 0)}`, `testing={candidates.get('testing', 0)}`, `active={candidates.get('active', 0)}`, `rejected={candidates.get('rejected', 0)}`, `rolled_back={candidates.get('rolled_back', 0)}`")
    lines.append(f"- 충돌 피드백 총량: **{payload['feedback_total']}건** (`intended={feedback.get('intended', 0)}`, `unintended={feedback.get('unintended', 0)}`)")
    lines.append("")
    lines.append("## 3) 최근 KPI 스냅샷")
    lines.append("")
    if payload["latest_kpi"]:
        k = payload["latest_kpi"]
        lines.append(f"- 측정 시각: `{k['measured_at']}`")
        lines.append(f"- 수동 조작 누적: **{k['manual_ops_total']}회**")
        lines.append(f"- 자동화 취소율: **{k['automation_cancel_rate']}**")
        lines.append(f"- 월 전력(kWh): **{k['monthly_energy_kwh']}**")
    else:
        lines.append("- KPI 스냅샷 없음")
    lines.append("")
    lines.append("## 4) 대시보드 구조 지표")
    lines.append("")
    lines.append(f"- 뷰 수: **{lovelace['views']}개**")
    lines.append(f"- 섹션 수: **{lovelace['sections']}개**")
    lines.append(f"- 카드 수: **{lovelace['cards']}개**")
    if lovelace["view_types"]:
        parts = [f"`{k}:{v}`" for k, v in sorted(lovelace["view_types"].items())]
        lines.append(f"- 뷰 타입 분포: {', '.join(parts)}")
    titles = payload["dashboard_card_titles"]
    if titles:
        lines.append("- 운영 카드 타이틀:")
        for title in titles:
            lines.append(f"  - {title}")
    lines.append("")
    lines.append("## 5) 포트폴리오에 바로 넣을 문장 (예시)")
    lines.append("")
    lines.append(f"- \"실운영 환경에서 이벤트 로그 **{payload['event_total']}건**을 축적하고, 추천 후보 **{payload['candidate_total']}건**을 규칙 기반으로 자동 생성했습니다.\"")
    lines.append("- \"추천 엔진은 승인-테스트-롤백 수명주기를 DB 스키마로 분리하여 운영 안정성을 확보했습니다.\"")
    lines.append(f"- \"대시보드는 **{lovelace['cards']}개 카드**를 섹션형 레이아웃으로 구성해 운영/분석 관점을 분리했습니다.\"")
    lines.append("")
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Export portfolio snapshot from live project data")
    parser.add_argument("--db", type=Path, default=Path("data/reco_engine.db"))
    parser.add_argument("--lovelace", type=Path, default=Path("lovelace_active.json"))
    parser.add_argument("--dashboard-cards", type=Path, default=Path("data/dashboard_cards.json"))
    parser.add_argument("--out", type=Path, default=Path("docs/portfolio_live_metrics_snapshot_v1.md"))
    args = parser.parse_args()

    input_data = SnapshotInput(
        db_path=args.db,
        lovelace_path=args.lovelace,
        dashboard_cards_path=args.dashboard_cards,
        output_path=args.out,
    )

    with sqlite3.connect(input_data.db_path) as conn:
        event_total = _query_one(conn, "SELECT COUNT(*) FROM event_log")
        actor_counts = dict(_query_pairs(conn, "SELECT actor_type, COUNT(*) FROM event_log GROUP BY actor_type"))
        result_counts = dict(_query_pairs(conn, "SELECT result, COUNT(*) FROM event_log GROUP BY result"))
        candidate_total = _query_one(conn, "SELECT COUNT(*) FROM recommendation_candidate")
        candidate_counts = dict(
            _query_pairs(conn, "SELECT status, COUNT(*) FROM recommendation_candidate GROUP BY status")
        )
        feedback_total = _query_one(conn, "SELECT COUNT(*) FROM conflict_feedback")
        feedback_counts = dict(_query_pairs(conn, "SELECT verdict, COUNT(*) FROM conflict_feedback GROUP BY verdict"))

        latest_kpi_row = conn.execute(
            """
            SELECT measured_at, manual_ops_total, automation_cancel_rate, monthly_energy_kwh
            FROM kpi_snapshot
            ORDER BY id DESC
            LIMIT 1
            """
        ).fetchone()
        latest_kpi = (
            {
                "measured_at": str(latest_kpi_row[0]),
                "manual_ops_total": int(latest_kpi_row[1]),
                "automation_cancel_rate": float(latest_kpi_row[2]),
                "monthly_energy_kwh": float(latest_kpi_row[3]),
            }
            if latest_kpi_row
            else None
        )

    payload = {
        "db_path": str(input_data.db_path),
        "lovelace_path": str(input_data.lovelace_path),
        "event_total": event_total,
        "actor_counts": actor_counts,
        "result_counts": result_counts,
        "candidate_total": candidate_total,
        "candidate_counts": candidate_counts,
        "feedback_total": feedback_total,
        "feedback_counts": feedback_counts,
        "latest_kpi": latest_kpi,
        "lovelace": _load_lovelace_stats(input_data.lovelace_path),
        "dashboard_card_titles": _load_dashboard_card_titles(input_data.dashboard_cards_path),
    }

    input_data.output_path.parent.mkdir(parents=True, exist_ok=True)
    input_data.output_path.write_text(_build_markdown(payload), encoding="utf-8")
    print(str(input_data.output_path))


if __name__ == "__main__":
    main()
