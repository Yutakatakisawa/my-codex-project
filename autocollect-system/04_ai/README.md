# 04_ai 実行ガイド

## 実装済みスクリプト

- `scripts/build_article_briefs.py`
- `scripts/generate_article_drafts.py`
- `scripts/lead_scoring.py`
- `scripts/weekly_report.py`
- `scripts/run_pipeline.py`

---

## 実行例

```bash
cd /workspace/autocollect-system/04_ai
python3 scripts/run_pipeline.py \
  --keywords ../02_seo/keywords_master.csv \
  --calendar ../02_seo/content_calendar_30.csv \
  --leads data/leads_sample.csv \
  --metrics data/metrics_weekly_sample.csv

# 30記事の下書きを生成
python3 scripts/generate_article_drafts.py \
  --calendar ../02_seo/content_calendar_30.csv \
  --outdir ../02_seo/drafts
```

---

## 出力

- `outputs/briefs/*.md`（30記事分ブリーフ）
- `outputs/leads_scored.csv`（HOT/WARM/COLD）
- `outputs/weekly_report.md`（週次レポート）
- `../02_seo/drafts/*.md`（30記事分下書き）

