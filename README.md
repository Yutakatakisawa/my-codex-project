# 屋根レスキュー24 - Roofing Landing Page

X投稿（Claude + Figmaで短時間に本番品質サイトを作るという内容）を参考に、  
**屋根工事業者向けの1ページサイト**として再構築した静的Webサイトです。

## 実装内容

- 強い訴求を持つヒーローセクション（即日対応・無料見積り）
- サービス一覧（雨漏り修理 / カバー工法 / 葺き替え / 雨どい ほか）
- 施工事例・料金目安・工事フロー
- FAQアコーディオン
- お問い合わせフォーム（フロント側バリデーション付き）
- モバイルメニュー / スムーズスクロール / スクロール時のUI変化
- モバイル用の固定電話CTA

## 技術スタック

- HTML5
- CSS3（Grid / Flexbox / カスタムプロパティ）
- Vanilla JavaScript（ES6）

## ファイル構成

```text
/workspace
├── index.html
├── css/
│   └── style.css
├── js/
│   └── main.js
└── README.md
```

## ローカル確認

```bash
python3 -m http.server 8000
```

ブラウザで `http://localhost:8000` を開いて確認してください。

