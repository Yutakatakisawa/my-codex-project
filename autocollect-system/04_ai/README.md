# 04_ai 実行ガイド

## 実装済みスクリプト

- `scripts/build_article_briefs.py`
- `scripts/generate_article_drafts.py`
- `scripts/generate_area_pages.py`
- `scripts/prioritize_ab_tests.py`
- `scripts/build_dm_queue.py`
- `scripts/send_dm_webhook.py`
- `scripts/lead_scoring.py`
- `scripts/weekly_report.py`
- `scripts/funnel_forecast.py`
- `scripts/run_pipeline.py`

---

## 実行例

```bash
cd /workspace/autocollect-system/04_ai
python3 scripts/run_pipeline.py \
  --keywords ../02_seo/keywords_master.csv \
  --calendar ../02_seo/content_calendar_30.csv \
  --leads data/leads_sample.csv \
  --metrics data/metrics_weekly_sample.csv \
  --cities ../06_growth/national_city_expansion_list.csv \
  --area-template ../06_growth/templates/area_page_template.md \
  --ab-tests ../06_growth/ab_test_backlog.csv \
  --dm-prospects ../07_dm/dm_prospects_sample.csv \
  --dm-templates ../07_dm/dm_templates.json \
  --dm-dry-run

# 30記事の下書きを生成
python3 scripts/generate_article_drafts.py \
  --calendar ../02_seo/content_calendar_30.csv \
  --outdir ../02_seo/drafts

# 受注目標から必要流入を逆算
python3 scripts/funnel_forecast.py \
  --target-deals 5 \
  --consult-to-deal 0.25 \
  --lead-to-consult 0.40 \
  --visit-to-lead 0.025
```

---

## 出力

- `outputs/briefs/*.md`（30記事分ブリーフ）
- `outputs/leads_scored.csv`（HOT/WARM/COLD）
- `outputs/weekly_report.md`（週次レポート）
- `outputs/area_pages/*.md`（地域拡張ページ）
- `outputs/ab_test_priority.md`（ABテスト優先順位）
- `outputs/dm_queue.csv`（DM送信キュー）
- `outputs/dm_preview.md`（DM文面プレビュー）
- `outputs/dm_send_results.csv`（DM送信結果）
- `../02_seo/drafts/*.md`（30記事分下書き）

