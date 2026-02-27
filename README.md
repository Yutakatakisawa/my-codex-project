# 瀧澤屋根工業 - Takisawa Roof Website

盛岡市の屋根工事専門店「瀧澤屋根工業」の公式ウェブサイト。

## 概要

屋根葺き替え・カバー工法・雨漏り修理・雪止め・雨樋の修理まで幅広く対応する屋根工事専門店のウェブサイトです。

## 技術スタック

- HTML5
- CSS3 (カスタムプロパティ、Grid、Flexbox)
- Vanilla JavaScript (ES6+)
- Google Fonts (Noto Sans JP, Noto Serif JP)

## 特徴

- レスポンシブデザイン（モバイル・タブレット・デスクトップ対応）
- スムーズスクロール
- スクロールアニメーション（IntersectionObserver使用）
- FAQ アコーディオン
- お問い合わせフォーム
- モバイルナビゲーション
- バックトゥトップボタン
- 固定電話ボタン（モバイル表示時）

## ファイル構成

```
/
├── index.html          # メインHTML
├── homepageseisaku.html # 職人WEB制作の診断ページ（直リンク）
├── homepageseisaku/
│   └── index.html      # /homepageseisaku 用エントリ
├── css/
│   ├── style.css       # メインスタイルシート
│   └── homepage-seisaku.css # 診断ページ用スタイル
├── js/
│   ├── main.js         # メインJavaScript
│   └── homepage-seisaku.js # 診断ページ用JavaScript
├── autocollect-system/ # 自動集客システム実行パック
└── README.md           # このファイル
```

## ローカルでの確認

任意のHTTPサーバーで配信してください:

```bash
# Python 3を使う場合
python3 -m http.server 8000

# Node.jsのhttp-serverを使う場合
npx http-server
```

ブラウザで `http://localhost:8000` を開いてください。
