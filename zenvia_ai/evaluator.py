"""
Evaluation and Benchmark Engine for Model Performance Against Ground Truth.
"""

from typing import List, Tuple, Dict
from collections import Counter
from .models import ProductItem, ClassificationResult, EvaluationMetrics
from .config import setup_logger

logger = setup_logger("zenvia_ai.evaluator")


class ModelEvaluator:
    """Evaluates classification accuracy and agreement rates against manual curation."""

    @staticmethod
    def evaluate(pairs: List[Tuple[ProductItem, ClassificationResult]]) -> EvaluationMetrics:
        """Compute comprehensive statistical metrics over a test batch."""
        if not pairs:
            return EvaluationMetrics()

        total = len(pairs)
        exact_matches = 0
        partial_matches = 0
        subcat_matches = 0
        confidence_sum = 0.0
        latency_sum = 0.0

        vibe_counter: Counter = Counter()
        occasion_counter: Counter = Counter()

        for item, res in pairs:
            confidence_sum += res.confidence
            latency_sum += res.latency_seconds

            for vibe in res.vibe_tags:
                vibe_counter[vibe] += 1
            occasion_counter[res.occasion] += 1

            # Ground truth vibes from manual curation
            ground_truth_vibes = {
                v.strip().lower()
                for v in (item.manual_vibes or "").split(",")
                if v.strip()
            }
            pred_vibes = {v.strip().lower() for v in res.vibe_tags if v.strip()}

            # Exact Set Match
            if ground_truth_vibes and ground_truth_vibes == pred_vibes:
                exact_matches += 1

            # Partial Intersection (Any shared tag)
            if ground_truth_vibes and (ground_truth_vibes & pred_vibes):
                partial_matches += 1

            # Subcategory Match
            if item.manual_subcategory and res.subcategory:
                if item.manual_subcategory.strip().lower() == res.subcategory.strip().lower():
                    subcat_matches += 1

        agreement_rate = (partial_matches / total * 100) if total > 0 else 0.0
        avg_conf = (confidence_sum / total) if total > 0 else 0.0
        avg_latency = (latency_sum / total) if total > 0 else 0.0

        metrics = EvaluationMetrics(
            total_evaluated=total,
            exact_match_count=exact_matches,
            partial_match_count=partial_matches,
            subcategory_match_count=subcat_matches,
            average_confidence=round(avg_conf, 4),
            average_latency=round(avg_latency, 2),
            agreement_rate=round(agreement_rate, 2),
            vibe_distribution=dict(vibe_counter.most_common(10)),
            occasion_distribution=dict(occasion_counter.most_common(5)),
        )

        logger.info(f"Evaluation complete: {total} items | Agreement: {metrics.agreement_rate}% | Latency: {metrics.average_latency}s")
        return metrics

    @staticmethod
    def generate_markdown_report(metrics: EvaluationMetrics) -> str:
        """Format metrics into a presentation-ready markdown report."""
        report = [
            "# 📊 Zenvia AI — Model Benchmark & Evaluation Report",
            "",
            "## Summary Metrics",
            f"- **Total Products Evaluated:** `{metrics.total_evaluated}`",
            f"- **Curator Agreement Rate:** `{metrics.agreement_rate}%`",
            f"- **Subcategory Accuracy:** `{(metrics.subcategory_match_count / max(metrics.total_evaluated, 1)) * 100:.1f}%`",
            f"- **Average Model Confidence:** `{metrics.average_confidence * 100:.1f}%`",
            f"- **Average Latency per Item:** `{metrics.average_latency}s`",
            "",
            "## Top Aesthetic Vibes Identified",
            "| Vibe Tag | Item Count | Share (%) |",
            "|---|---|---|",
        ]

        total_vibe_hits = max(sum(metrics.vibe_distribution.values()), 1)
        for vibe, count in metrics.vibe_distribution.items():
            share = (count / total_vibe_hits) * 100
            report.append(f"| `{vibe}` | {count} | {share:.1f}% |")

        report.extend([
            "",
            "## Target Occasion Distribution",
            "| Occasion | Count |",
            "|---|---|",
        ])
        for occ, count in metrics.occasion_distribution.items():
            report.append(f"| `{occ}` | {count} |")

        return "\n".join(report)
