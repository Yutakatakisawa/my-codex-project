# AIエージェント設計（実装版）

## 目的

- コンテンツ生産と追客業務を半自動化
- 人間は「最終判断」と「商談」に集中

---

## エージェント一覧

| Agent | 役割 | 入力 | 出力 | 自動化率 |
|---|---|---|---|---|
| data_collector | 週次データ収集 | GA4/GSC/LINE/広告CSV | 週次集計CSV | 90% |
| keyword_classifier | KW分類 | KWマスター | 優先度付きKW | 100% |
| brief_builder | 記事ブリーフ生成 | KW + カレンダー | ブリーフ.md | 100% |
| draft_assistant | 下書き生成 | ブリーフ + プロンプト | 記事下書き | 80% |
| seo_checker | SEO校正 | 記事下書き | 修正提案 | 80% |
| sns_repurposer | SNS展開 | 記事本文 | X/IG/Shorts案 | 100% |
| line_writer | LINE配信文作成 | セグメント情報 | 配信文 | 100% |
| lead_scorer | 見込み客評価 | 行動ログ | HOT/WARM/COLD | 100% |
| proposal_helper | 提案書初稿 | ヒアリングメモ | 提案書ドラフト | 70% |
| weekly_reporter | KPI可視化 | 週次指標CSV | 週報.md | 100% |

---

## 人間がやる部分

- 誤情報チェック
- 業界トーン最終調整
- 商談ヒアリングと契約判断
- 施工写真/動画の収集

---

## 自動化優先順位

1. 記事ブリーフ生成
2. リードスコアリング
3. 週次レポート作成
4. LINE配信文生成

