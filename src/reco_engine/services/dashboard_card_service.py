from __future__ import annotations

from dataclasses import dataclass

from reco_engine.core.entity_resolution import display_entity_name
from reco_engine.services.ops_summary_service import OpsSummary


@dataclass(frozen=True)
class DashboardCards:
    today_candidates_card: dict
    conflict_top5_card: dict
    savings_top5_card: dict

    def to_list(self) -> list[dict]:
        return [
            self.today_candidates_card,
            self.conflict_top5_card,
            self.savings_top5_card,
        ]


class DashboardCardService:
    def build(self, summary: OpsSummary) -> DashboardCards:
        return DashboardCards(
            today_candidates_card={
                "type": "markdown",
                "title": "보완 필요 자동화 (지금 점검)",
                "content": self._render_classified(summary.review_now),
            },
            conflict_top5_card={
                "type": "markdown",
                "title": "정상 운영 자동화 (유지)",
                "content": self._render_classified(summary.keep_good),
            },
            savings_top5_card={
                "type": "markdown",
                "title": "미구현 자동화 추천 (신규)",
                "content": self._render_classified(summary.recommend_new),
            },
        )

    @staticmethod
    def _render_classified(rows: list[dict]) -> str:
        if not rows:
            return "항목 없음"
        lines = []
        for idx, row in enumerate(rows, start=1):
            entity_name = display_entity_name(row["entity_id"])
            reasons = [str(item) for item in row.get("reasons", []) if str(item)]
            reason_text = "; ".join(reasons) if reasons else "근거 로그 확인 필요"
            action_text = str(row.get("recommended_action", "정책 확인 필요"))
            lines.append(
                f"{idx}. **{entity_name}**\n"
                f"- 근거: {reason_text}\n"
                f"- 관측/실행 횟수: {row['evidence_count']}회\n"
                f"- 권장 액션: {action_text}"
            )
        return "\n".join(lines)
