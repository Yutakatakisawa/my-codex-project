# Wix実装手順: 無料診断 + LINE導線

この手順は「今日中に動かす」ことを目的にしています。  
完了目安: 2〜3時間

---

## 0. 事前準備（10分）

1. Wixサイトで **Dev Mode (Velo)** をON
2. LINE公式アカウントを作成し、友だち追加URLを取得
3. 予約URL（Calendly等）を準備
4. 本フォルダの以下を開く
   - `pages/shindan.js`
   - `pages/shindan-result.js`
   - `data/questions-and-scoring.json`
   - `line/line-step-messages.md`

---

## 1. Collection作成（10分）

CMSに `ShindanResponses` を作成し、以下フィールドを追加:

| フィールドキー | 型 |
|---|---|
| `name` | Text |
| `industry` | Text |
| `area` | Text |
| `q1`〜`q20` | Number |
| `totalScore` | Number |
| `score100` | Number |
| `resultType` | Text |
| `weakestCategory` | Text |
| `createdAt` | Date and Time |

権限（最低限）:
- Create: Site member author または Everyone（運用方針に合わせる）
- Read: Admin only 推奨

---

## 2. 診断ページ `/shindan` 作成（40分）

ページ上に以下要素を配置して、**IDを完全一致** で設定:

### 基本入力
- `#nameInput`（Text Input）
- `#industryDropdown`（Dropdown）
- `#areaInput`（Text Input）

### 設問（RadioGroup）
- `#q1` 〜 `#q20`

各RadioGroupは4択で value を以下に統一:
- A: `3`
- B: `2`
- C: `1`
- D: `0`

### 補助要素
- `#errorText`（Text）  
  - 初期状態で collapse
  - 色は赤推奨
- `#submitBtn`（Button）  
  - 初期ラベル: `診断結果を見る`

---

## 3. 結果ページ `/shindan-result` 作成（30分）

ページ上に以下要素を配置してID設定:

- `#typeTitle`（Text）
- `#scoreText`（Text）
- `#weakText`（Text）
- `#resultLeadText`（Text）
- `#resultBody`（Text）
- `#action1`（Text）
- `#action2`（Text）
- `#action3`（Text）
- `#lineLeadText`（Text）
- `#lineBtn`（Button）

任意（カテゴリ別スコア表示を出す場合）:
- `#scoreDiscoverability`
- `#scoreTrust`
- `#scoreFunnel`
- `#scoreFollowup`
- `#scoreOperations`

---

## 4. Veloコード貼り付け（20分）

1. `/shindan` ページコードに `pages/shindan.js` の内容を貼る
2. `/shindan-result` ページコードに `pages/shindan-result.js` の内容を貼る
3. `pages/shindan-result.js` の以下を差し替える

```js
const LINE_ADD_FRIEND_URL = 'https://lin.ee/REPLACE_ME';
```

---

## 5. スコアロジック（実装済み）

- 4択配点: A=3, B=2, C=1, D=0
- 合計点: 0〜60
- 100点換算: `round(total / 60 * 100)`
- 弱点カテゴリ同点時の優先順位:
  1. 導線
  2. 見つかりやすさ
  3. 信頼性
  4. 追客
  5. 運用継続

### 結果タイプ4分類
- 0〜39: Type D（緊急改善型）
- 40〜64: Type C（土台再構築型）
- 65〜84: Type B（伸びしろ加速型）
- 85〜100: Type A（自動集客準備完了型）

---

## 6. LINE導線設計（20分）

1. 結果ページの `#lineBtn` を有効化（コードで自動リンク）
2. `line/line-step-messages.md` の7通をLINE（またはLステップ）に登録
3. 配信タイミングを `0,1,2,3,4,5,6日後` に設定
4. キーワード応答を設定
   - `診断` -> 特典URL
   - `相談` -> 予約URL
   - `テンプレ` -> 施工事例テンプレURL

---

## 7. 公開前テスト（15分）

### 正常系
- 20問すべて回答 -> 結果ページへ遷移する
- `ShindanResponses` にレコードが保存される
- 結果ページでタイプ/スコア/弱点/3アクションが表示される
- LINEボタンが正しいURLに飛ぶ

### 異常系
- 未回答で送信 -> エラー表示される
- `rid` なしで結果ページアクセス -> エラー文言表示

---

## 8. 初回公開後の改善（当日）

1. 診断完了率を確認（開始数に対する完了率）
2. LINE登録率を確認（結果ページ到達者に対する登録率）
3. 低い場合は以下を改善
   - 設問文を短くする
   - 結果ページのCTAを上部に移動
   - LINE登録ボタン文言を強化

---

## 9. すぐ使える運用KPI

- 診断開始数 / 日
- 診断完了率（目標 60%以上）
- LINE登録率（目標 35%以上）
- 相談予約率（目標 15%以上）
- 受注率（目標 25%以上）

これで「無料診断 -> LINE -> 相談」導線の最小構成が完成です。
