# 職人WEBタキサワ: 無料診断 + LINE導線 実装パック

このフォルダは、Wixで「無料診断 + LINE導線」を即実装するためのコピペ用パッケージです。

## 含まれるファイル

- `pages/shindan.js`  
  Wixページ `/shindan` 用。20問診断の採点、結果保存、結果ページ遷移。
- `pages/shindan-result.js`  
  Wixページ `/shindan-result` 用。結果タイプ表示、改善アクション表示、LINE導線。
- `data/questions-and-scoring.json`  
  20問4択、配点、カテゴリ、結果タイプの定義データ。
- `line/line-step-messages.md`  
  LINE自動返信7通テンプレ（そのまま投入可能）。
- `WIX_SETUP_GUIDE.md`  
  Wixで今日中に公開するための実装手順。

## 先にやること（5分）

1. WixでDev Mode (Velo) をONにする
2. Collection `ShindanResponses` を作る
3. `WIX_SETUP_GUIDE.md` の要素IDどおりにページ要素を配置する
4. `pages/shindan.js` と `pages/shindan-result.js` を貼り付ける

## 注意

- `pages/shindan-result.js` の `LINE_ADD_FRIEND_URL` は必ず置き換えてください。
- このコードはWix Velo環境向けです（ローカルNode実行用ではありません）。
