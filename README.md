# Component Gallery Clone

`https://component.gallery/` のような体験を目指した、**UIコンポーネント検索・比較サイト**のMVPです。

## 実装している機能

- コンポーネントカード一覧表示
- キーワード検索
- カテゴリフィルタ
- フレームワークフィルタ（React / Vue / Svelte / Angular / Solid）
- 並び順変更（名前順 / 実装数順 / カテゴリ順）
- お気に入り登録（`localStorage` 保存）
- 詳細モーダル
  - フレームワーク別タブ
  - 実装スニペット表示
  - コードコピー
  - 外部リンク（Docs / Source）
- 比較ビュー
  - 同一コンポーネントを複数フレームワークで横並び比較

## 技術スタック

- HTML5
- CSS3
- Vanilla JavaScript (ES6+)

## ファイル構成

```text
/
├── index.html
├── css/
│   └── style.css
├── js/
│   └── main.js
└── README.md
```

## ローカル確認

任意のHTTPサーバーで配信してください。

```bash
python3 -m http.server 8000
```

ブラウザで `http://localhost:8000` を開きます。

## データの拡張方法

`js/main.js` の `COMPONENTS` 配列に要素を追加すると、一覧・詳細・比較ビューへ自動反映されます。

- `id`
- `name`
- `category`
- `description`
- `preview`
- `tags`
- `frameworks`（各フレームワークの `status`, `snippet`, `docs`, `source`, `note`）

`status` は以下のいずれかを想定しています。

- `stable`
- `beta`
- `planned`
