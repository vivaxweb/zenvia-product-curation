"""
CLI Script: Run Batch Vibe Tagging on a Product Catalog.

Usage:
  python scripts/run_tagger.py --input "demo/sample_curated_products.xlsx" --limit 10
"""

import sys
import io
import os
import argparse
import time

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from zenvia_ai.config import Config, setup_logger
from zenvia_ai.data_loader import CatalogLoader
from zenvia_ai.pipeline import VibeClassificationPipeline
from zenvia_ai.evaluator import ModelEvaluator

logger = setup_logger("run_tagger")


def main():
    parser = argparse.ArgumentParser(description="Zenvia AI Batch Vibe Classification CLI")
    parser.add_argument("--input", "-i", required=True, help="Path to input Excel spreadsheet")
    parser.add_argument("--output", "-o", default=None, help="Path to save enriched output spreadsheet")
    parser.add_argument("--limit", "-l", type=int, default=None, help="Max items to process")
    parser.add_argument("--delay", "-d", type=float, default=1.0, help="Delay between API requests in seconds")
    args = parser.parse_args()

    input_path = os.path.abspath(args.input)
    if not os.path.exists(input_path):
        logger.error(f"Input file not found: {input_path}")
        sys.exit(1)

    filename = os.path.basename(input_path)
    output_path = args.output or os.path.join(Config.OUTPUT_DIR, f"ai_tagged_{filename}")

    logger.info("=" * 65)
    logger.info("⚡ ZENVIA AI — MULTIMODAL VIBE CLASSIFICATION")
    logger.info(f"📁 Input File:  {filename}")
    logger.info(f"🤖 Model:       {Config.DEFAULT_MODEL}")
    logger.info(f"💾 Output Target:{output_path}")
    logger.info("=" * 65)

    products = CatalogLoader.load_products_from_excel(input_path, limit=args.limit)
    if not products:
        logger.warning("No valid products loaded. Exiting.")
        return

    pipeline = VibeClassificationPipeline()
    results = []

    for idx, item in enumerate(products, start=1):
        print(f"[{idx:3d}/{len(products):3d}] {item.name[:45]:<45}", end=" ", flush=True)
        res = pipeline.classify(item)
        results.append((item, res))

        if res.status == "ok":
            print(f"-> [{res.vibe_string}] ({res.subcategory}) conf={res.confidence:.2f} ({res.latency_seconds}s)")
        else:
            print(f"-> ⚠️ {res.status}")

        # Save checkpoint periodically
        if idx % 5 == 0 or idx == len(products):
            CatalogLoader.save_enriched_excel(input_path, results, output_path)

        if idx < len(products) and args.delay > 0:
            time.sleep(args.delay)

    # Compute quick stats
    metrics = ModelEvaluator.evaluate(results)
    print("\n" + "=" * 65)
    print(f"✅ Finished: {len(results)} items processed successfully.")
    print(f"🎯 Curator Agreement Rate: {metrics.agreement_rate}%")
    print(f"⏱️ Average Latency:       {metrics.average_latency}s / item")
    print(f"📁 Saved to:              {output_path}")
    print("=" * 65)


if __name__ == "__main__":
    main()
