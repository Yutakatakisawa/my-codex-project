# 音声要約LINE送信アプリ

このプロジェクトは、マイクから音声を録音し、OpenAI Whisper APIで文字起こしを行い、簡易要約を生成してLINEの指定ユーザーへテキスト送信するためのコマンドラインツールです。

## 機能概要

1. **音声録音**: `sounddevice` を利用して任意秒数の音声をWAV形式で収録します。
2. **文字起こし**: OpenAIの音声認識API（Whisper）で音声をテキストに変換します。
3. **要約生成**: NLTKを用いた頻度ベース要約アルゴリズムでテキストを要約します。
4. **LINE送信**: LINE Messaging APIを利用して要約テキストを送信します。

## 事前準備

1. 必要ライブラリのインストール:

   ```bash
   pip install -r requirements.txt
   ```

2. NLTKデータのダウンロード（初回のみ）:

   ```python
   python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
   ```

3. 環境変数の設定:

   - `OPENAI_API_KEY`: OpenAIのAPIキー
   - `OPENAI_TRANSCRIBE_MODEL`: 利用するWhisperモデル名（省略時は `gpt-4o-mini-transcribe`）
   - `LINE_CHANNEL_ACCESS_TOKEN`: LINE Messaging APIのチャネルアクセストークン

   Linux/macOSの場合の設定例:

   ```bash
   export OPENAI_API_KEY="sk-..."
   export LINE_CHANNEL_ACCESS_TOKEN="YOUR_LINE_TOKEN"
   ```

4. LINEの宛先ユーザーIDを取得し、送信可能な状態にしておきます（Botと友達になるなど）。

## 使い方

```bash
python -m app.main --duration 30 --line-user-id YOUR_USER_ID
```

オプション:

- `--duration`: 録音秒数（デフォルト15秒）
- `--keep-audio`: 録音した音声ファイルを削除せず保持します

コマンド実行後、文字起こし結果が要約され、指定したLINEユーザーへメッセージ送信されます。

## テスト

```bash
pytest
```

## 注意点

- マイク入力が必要なため、実行環境でマイクが利用可能であることを確認してください。
- OpenAI APIおよびLINE Messaging APIの利用には別途料金が発生する可能性があります。
- テストコードではNLTKのコーパスを自動ダウンロードしますが、オフライン環境では事前にダウンロードが必要です。
