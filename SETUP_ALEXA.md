# Alexa通知システムセットアップガイド

このガイドでは、ゴミ出し日程をAlexa画面に表示するために必要な設定方法を説明します。

## 必要な情報

以下の4つの情報を取得する必要があります:
1. **Device ID**: あなたのAlexa デバイスのID
2. **Refresh Token**: Amazon OAuth認証用のトークン
3. **Client ID**: Amazon Developer Consoleで作成
4. **Client Secret**: Amazon Developer Consoleで作成

---

## ステップ1: Amazon Developer Consoleアカウントの作成

1. https://developer.amazon.com/ にアクセス
2. 「Sign In」をクリック
3. Amazonアカウントで登録/ログイン
4. 「Alexa Skills Kit」を選択

---

## ステップ2: Alexaスキルの作成

1. Alexa Developer Consoleで「Create Skill」をクリック
2. Skill nameを入力 (例: "GomiReminder")
3. Primary locale: 「Japanese (Japan)」を選択
4. Choose a model: 「Custom」を選択
5. 「Create skill」をクリック

---

## ステップ3: LWAの設定（Client ID/Secret取得）

1. Developer Consoleで「Account Linking」セクションを開く
2. 「Security Profiles」セクションへ移動
3. 新しいSecurity Profileを作成:
   - Name: 「GomiReminder_Profile」
   - Description: 「Garbage collection reminders」
4. 「Web Settings」タブで:
   - **Allowed Return URLs**: 
     ```
     https://pitangui.amazon.com/auth/o2/oauth/success
     https://localhost:3000/callback
     ```
   - **Allowed Origins**:
     ```
     https://pitangui.amazon.com
     https://localhost:3000
     ```

5. 「Client ID」と「Client Secret」をコピーして保存

---

## ステップ4: Device IDの取得

### 方法1: Alexa Appで確認

1. スマートフォンのAlexaアプリを開く
2. 左上の「≡」メニューをタップ
3. 「デバイス」を選択
4. 通知を送信したいAlexaデバイスを選択
5. 詳細情報の中から「Device ID」をコピー

### 方法2: AWS Consoleで確認

1. https://console.aws.amazon.com/ にログイン
2. 「Systems Manager」を検索して選択
3. 左サイドバーから「Parameter Store」を選択
4. `/alexa/devices` で検索してデバイスIDを確認

---

## ステップ5: Refresh Tokenの取得

Alexa Notifications APIを使用するには、ユーザーの認可を得て Refresh Token を取得する必要があります。

### 手動取得方法:

1. 以下のURLをブラウザで開く（YOUR_CLIENT_IDを置き換え）:

```
https://www.amazon.com/ap/oa?client_id=YOUR_CLIENT_ID&scope=alexa:devices:all&response_type=code&redirect_uri=http://localhost:3000/callback
```

2. Amazonアカウントでログインして許可
3. URLに返される「code」パラメータをコピー
4. コマンドラインで以下を実行:

```bash
curl -X POST \
  https://api.amazon.com/auth/o2/token \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'grant_type=authorization_code&code=YOUR_CODE&client_id=YOUR_CLIENT_ID&client_secret=YOUR_CLIENT_SECRET&redirect_uri=http://localhost:3000/callback'
```

5. レスポンスから `refresh_token` をコピー

---

## ステップ6: config.jsonの作成

1. `config.json.template` を `config.json` にリネーム

2. 以下の値を入力:

```json
{
  "device_id": "amzn1.ask.device.XXXXX...",
  "refresh_token": "Atzr|IwEBIHZ...",
  "client_id": "amzn1.application.XXXXX...",
  "client_secret": "YOUR_CLIENT_SECRET_HERE"
}
```

---

## ステップ7: テスト実行

1. コマンドプロンプトを開く
2. 以下を実行:

```bash
cd C:\Users\user\gomi_reminder_system
python main.py --mode test --once
```

3. Alexa画面にテスト通知が表示されることを確認

---

## トラブルシューティング

### 通知が送信されない場合:

1. **Device ID が正しいか確認**
   - Alexa Appで確認してコピー直後の値と比較

2. **Refresh Token の有効期限**
   - トークンの有効期限が切れていないか確認
   - 期限切れの場合は、ステップ5をやり直す

3. **Client IDとClient Secretが正しいか確認**
   - Developer Consoleで再確認

4. **ログを確認**
   - `gomi_reminder.log` の内容を確認
   - エラーメッセージから原因を特定

### ファイアウォール/セキュリティ:

- PCのファイアウォール設定でPythonスクリプトのアクセスを許可
- アンチウイルスソフトが通信をブロックしていないか確認

---

## セキュリティに関する注意

⚠️ **重要**: config.json には認証情報が含まれています

- **config.json を GitHub や公開リポジトリにアップロードしないこと**
- **config.json をメール等で送信しないこと**
- **config.json.template のみを共有すること**

---

## 次のステップ

config.json を作成した後:

1. テスト実行で動作確認
2. Windows Task Scheduler で自動起動を設定
   - 参照: `SETUP_TASK_SCHEDULER.md`

---

## 参考リンク

- [Amazon Alexa Notifications API](https://developer.amazon.com/docs/alexa-skills-kit/notification-management-api.html)
- [Amazon Developer Console](https://developer.amazon.com)
- [Alexa Skills Kit](https://developer.amazon.com/alexa-skills-kit)

