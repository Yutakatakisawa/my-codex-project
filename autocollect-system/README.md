# 職人WEBタキサワ 自動集客システム（実行版）

このパッケージは、以下の目標を**実行できる形**でまとめた運用キットです。

- SEOで安定問い合わせを獲得
- ITが苦手な職人にも認知される導線を構築
- 月5件以上の制作受注を安定化
- 将来的に半自動で回る仕組みを実装

---

## フォルダ構成

```text
autocollect-system/
├── 01_recognition/   # 認知フェーズ設計（SEO/SNS/無料オファー/広告）
├── 02_seo/           # SEO実務（キーワード、30記事、テンプレ、内部リンク）
├── 03_sales/         # 販売導線（診断、LINE、LP、クロージング）
├── 04_ai/            # AIエージェント設計 + 自動化スクリプト
└── 05_execution/     # 90日ロードマップ + KPI運用
```

---

## まず今日やること（最短）

1. `03_sales/diagnostic_20_questions.json` をWixフォームへ反映
2. `03_sales/line_7day_sequence.md` をLINEステップ配信に登録
3. `02_seo/content_calendar_30.csv` で記事制作を開始
4. `04_ai/scripts/run_pipeline.py` を実行して週次レポートを自動生成

---

## 推奨KPI（最初の90日）

- 月間流入: 2,000セッション
- リード: 50件 / 月
- 相談: 20件 / 月
- 受注: 5件 / 月
- 診断完了率: 60%+
- LINE登録率: 35%+

---

## 実行コマンド（AI自動化）

```bash
cd /workspace/autocollect-system/04_ai
python3 scripts/run_pipeline.py \
  --keywords ../02_seo/keywords_master.csv \
  --calendar ../02_seo/content_calendar_30.csv \
  --leads data/leads_sample.csv \
  --metrics data/metrics_weekly_sample.csv
```

実行後に以下が生成されます。

- `outputs/briefs/*.md`
- `outputs/leads_scored.csv`
- `outputs/weekly_report.md`

