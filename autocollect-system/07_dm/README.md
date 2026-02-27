# 07_dm 実行ガイド（DM自動化）

## 目的

- 見込み客へのDMを半自動で回す
- 手動対応を「返信対応」に集中させる
- 相談予約数を増やす

---

## 追加ファイル

- `dm_templates.json`：チャネル別テンプレ
- `dm_prospects_sample.csv`：見込み客サンプル
- `dm_policy.md`：運用ルール
- `webhook_payload_example.json`：Webhook送信サンプル

---

## 実行手順

```bash
cd /workspace/autocollect-system/04_ai

# 1) DMキュー作成
python3 scripts/build_dm_queue.py \
  --prospects ../07_dm/dm_prospects_sample.csv \
  --templates ../07_dm/dm_templates.json \
  --output outputs/dm_queue.csv \
  --preview outputs/dm_preview.md

# 2) Webhook送信（dry-run）
python3 scripts/send_dm_webhook.py \
  --queue outputs/dm_queue.csv \
  --output outputs/dm_send_results.csv \
  --dry-run
```

---

## 運用ポイント

1. 1日に送る通数を上限管理（例: 30通）
2. 返信が来た相手には自動送信停止
3. 1回目->3日後->7日後の最大3通で打ち止め
4. NGワードやスパム判定を避ける文面で運用

