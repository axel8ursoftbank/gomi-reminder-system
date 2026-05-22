# 🎯 ゴミ出し日程Alexa通知システム - 詳細導入ガイド

**このガイドは、まったくの初心者を想定した、最も詳しい導入手順です。**
**段階ごとにスクリーンショット付きで説明しています。**

---

## 📋 全体の流れ

```
【準備段階】
1. Pythonのインストール確認
2. 必要なパッケージのインストール

【システム初期化】
3. スケジュール情報の抽出
4. 抽出内容の確認

【Alexa認証設定】
5. Amazon Developer Consoleでスキル作成
6. Device ID取得
7. Refresh Token取得
8. config.json作成

【テスト】
9. テスト実行で動作確認

【自動実行設定】
10. Windows Task Schedulerで自動起動設定
11. 本番運用開始
```

---

# 【準備段階】

## ステップ1: Pythonのインストール確認

### 確認方法

1. **Windows キー + R を押す**
   - 小さなダイアログが開きます

2. **「cmd」と入力 → Enter キーを押す**
   - コマンドプロンプトが起動します

3. **以下を入力して Enter キーを押す**
   ```
   python --version
   ```

### 正常な場合
```
Python 3.11.0
```
などのバージョン番号が表示されます

### エラーの場合（「pythonコマンドが見つかりません」）

**Pythonをインストールする:**

1. https://www.python.org/downloads/ を開く

2. **「Download Python 3.11」** （最新版）をクリック

3. **インストーラーを実行**
   - ダウンロードされたファイルをダブルクリック

4. **重要：以下のチェックボックスをONにする**
   ```
   ☑️ Add Python 3.11 to PATH
   ```

5. **「Install Now」をクリック**

6. **インストール完了後、PCを再起動**

7. **再度確認**
   ```
   python --version
   ```

---

## ステップ2: 必要なパッケージのインストール

### コマンドプロンプトで実行

1. **Windows キー + R → cmd → Enter**

2. **以下のディレクトリに移動**
   ```bash
   cd C:\Users\user\gomi_reminder_system
   ```

3. **パッケージをインストール**
   ```bash
   pip install -r requirements.txt
   ```

### インストール画面の例

```
Collecting openpyxl>=3.10.0
  Downloading openpyxl-3.11.0-py2.py3-none-any.whl (145 kB)
  
Collecting apscheduler>=3.10.0
  Downloading apscheduler-3.10.4-py3-none-any.whl (62 kB)

...

Successfully installed openpyxl-3.11.0 apscheduler-3.10.4 ...
```

### ✅ 確認

画面の最後に「Successfully installed」と表示されれば成功です

---

# 【システム初期化】

## ステップ3: スケジュール情報の抽出

### 実行

コマンドプロンプトで以下を実行：

```bash
python extract_schedule.py
```

### 実行画面の例

```
ファイルを開いています: C:\Users\user\.claude\projects\...\webfetch-...xlsx
スケジュール情報を抽出中...

✓ 燃やすごみ: 毎週月・木曜日
✓ 燃やさないごみ: 11件の日程
✓ かん: 11件の日程
✓ びん: 11件の日程
✓ 剪定枝・草: 11件の日程
✓ ペットボトル: 11件の日程
✓ 紙類: 11件の日程
✓ 蛍光灯・電池: 6件の日程

✓ スケジュールを保存しました: C:\Users\user\gomi_reminder_system\schedule_cache.json

==================================================
スケジュール抽出完了
==================================================

今日: 2026年05月09日（Saturday）
明日: 2026年05月10日（Sunday）
明日はゴミ出し日ではありません
```

### ✅ 確認

「スケジュールを保存しました」と表示されたら成功です

---

## ステップ4: 抽出内容の確認

### ファイルエクスプローラーで確認

1. **ファイルエクスプローラーを開く**
   - Windows キー + E

2. **以下のパスに移動**
   ```
   C:\Users\user\gomi_reminder_system
   ```

3. **schedule_cache.json が存在することを確認**
   - ファイルが見えたら成功

### JSON内容の確認（オプション）

1. **schedule_cache.json を右クリック**

2. **「プログラムから開く」→「メモ帳」を選択**

3. **以下のような内容が表示されたら成功**
   ```json
   {
     "year": 2026,
     "generated_at": "2026-05-09T...",
     "schedule": {
       "燃やすごみ": [
         "2026-01-05",
         "2026-01-08",
         ...
       ],
       "かん": {
         "1": [16],
         "2": [13],
         ...
       },
       ...
     }
   }
   ```

---

# 【Alexa認証設定】

⚠️ **重要**: 以下のステップはインターネット接続が必須です

## ステップ5: Amazon Developer Consoleでスキル作成

### 5-1. アカウント作成

1. **ブラウザを開いて以下にアクセス**
   ```
   https://developer.amazon.com
   ```

2. **「Sign In」をクリック**

3. **Amazonアカウントでログイン**
   - 既に持っている場合は通常のAmazonアカウント
   - 持っていない場合は新規作成

### 5-2. Alexa Skills Kitを選択

1. ログイン後、左側メニューから **「Alexa Skills Kit」** を選択

2. **「Alexa Developer Console」** をクリック

### 5-3. スキルを作成

1. **「Create Skill」ボタンをクリック**

2. **Skill name を入力**
   ```
   Gomi Reminder
   ```
   または任意の名前

3. **Primary locale で「Japanese (Japan)」を選択**

4. **Choose a model で「Custom」を選択**

5. **「Create skill」をクリック**

### ✅ スキルが作成されました

スキルのダッシュボードが表示されます

---

## ステップ6: Device ID取得

### 方法1: Alexa App（最も簡単）📱

1. **スマートフォンで Alexa App を開く**
   - iOS: App Store
   - Android: Google Play Store

2. **左上の「≡」（メニュー）をタップ**

3. **「デバイス」をタップ**

4. **Alexa デバイスの一覧が表示される**

5. **通知を受け取りたいデバイスをタップ**
   - 例: 「リビングのEcho Show」など

6. **詳細画面で下にスクロール**

7. **「Device ID」を見つけてコピー**
   - 例: `amzn1.ask.device.XXXXXXXXXXXXXXXXXX`

### 方法2: Web Console（代替方法）

1. https://alexa.amazon.com/ にアクセス

2. 左メニューから **「デバイス」** を選択

3. デバイス一覧からコピー

### 💾 Device ID をメモ帳に保存

1. **メモ帳を開く**
   - スタート → メモ帳

2. **以下のような形式で保存**
   ```
   ========== Alexa認証情報 ==========
   
   Device ID:
   amzn1.ask.device.XXXXXXXXXXXXXXXXXX
   
   Refresh Token:
   （次のステップで取得）
   
   Client ID:
   （次のステップで取得）
   
   Client Secret:
   （次のステップで取得）
   ```

---

## ステップ7: Refresh Token と Client ID/Secret 取得

### 7-1. Security Profile を作成

1. **Amazon Developer Console に戻る**
   ```
   https://developer.amazon.com/alexa/console/ask
   ```

2. **左側メニュー下部から「Account Linking」を探す**
   - または右上のユーザー名 → 「Security Profiles」

3. **「Security Profiles」ページを開く**

4. **「Create Security Profile」をクリック**

5. **情報を入力**
   ```
   Security Profile Name: Gomi_Reminder_Profile
   
   Security Profile Description: 
   Garbage collection reminder notifications
   ```

6. **「Next」をクリック**

### 7-2. Client ID と Client Secret をコピー

1. **作成されたSecurity Profileが表示される**

2. **「Show Client ID」をクリック**
   - Client ID をコピー
   - 例: `amzn1.application.XXXXX...`

3. **「Show Client Secret」をクリック**
   - Client Secret をコピー
   - 例: `xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

4. **メモ帳に保存**
   ```
   Client ID:
   amzn1.application.XXXXX...
   
   Client Secret:
   xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

### 7-3. Web Settings を設定

1. **「Web Settings」タブをクリック**

2. **「Allowed Return URLs」に以下を入力**
   ```
   https://pitangui.amazon.com/auth/o2/oauth/success
   https://localhost:3000/callback
   ```

3. **「Allowed Origins」に以下を入力**
   ```
   https://pitangui.amazon.com
   https://localhost:3000
   ```

4. **「Save」をクリック**

---

## ステップ7-補足: Refresh Token の取得（難易度：中）

### 方法A: ブラウザで取得（最も簡単）

⚠️ **重要**: 以下の手順は少し複雑です。慎重に進めてください。

1. **ブラウザで以下のURLを開く**
   ```
   https://www.amazon.com/ap/oa?client_id=YOUR_CLIENT_ID&scope=alexa:devices:all&response_type=code&redirect_uri=https://localhost:3000/callback
   ```
   
   **YOUR_CLIENT_ID を置き換え:**
   - 例: `amzn1.application.6c8d8f...` に置き換える

2. **Amazonアカウントでログイン**

3. **「許可」をクリック**

4. **ブラウザのアドレスバーに「code=XXXXXXX」が表示される**
   ```
   https://localhost:3000/callback?code=Atzr|IwEBIE...
   ```
   
   **code=の後ろの値をコピー**
   - 例: `Atzr|IwEBIE...` の部分

5. **コマンドプロンプトで以下を実行**

   ```bash
   curl -X POST https://api.amazon.com/auth/o2/token ^
     -H "Content-Type: application/x-www-form-urlencoded" ^
     -d "grant_type=authorization_code" ^
     -d "code=CODE_HERE" ^
     -d "client_id=CLIENT_ID_HERE" ^
     -d "client_secret=CLIENT_SECRET_HERE" ^
     -d "redirect_uri=https://localhost:3000/callback"
   ```

   **置き換え:**
   - `CODE_HERE` → 上記でコピーした code
   - `CLIENT_ID_HERE` → Client ID
   - `CLIENT_SECRET_HERE` → Client Secret

6. **実行結果に refresh_token が含まれます**
   ```json
   {
     "access_token": "...",
     "refresh_token": "Atzr|IwEBIHZaxxx...",
     "token_type": "Bearer",
     "expires_in": 3600
   }
   ```

   **refresh_token をコピー**

---

### 方法B: Pythonスクリプトで取得（代替方法）

Curl コマンドが分からない場合は、以下のスクリプトを使用してください：

1. **テキストエディタを開く**

2. **以下をコピーして貼り付け**
   ```python
   import requests
   
   # ここを編集
   code = "Atzr|IwEBIE..."  # 上記で取得した code
   client_id = "amzn1.application...."  # Client ID
   client_secret = "xxxxxxxx..."  # Client Secret
   
   # トークンを取得
   url = "https://api.amazon.com/auth/o2/token"
   data = {
       "grant_type": "authorization_code",
       "code": code,
       "client_id": client_id,
       "client_secret": client_secret,
       "redirect_uri": "https://localhost:3000/callback"
   }
   
   response = requests.post(url, data=data)
   result = response.json()
   
   print("Refresh Token:")
   print(result.get("refresh_token"))
   ```

3. **ファイルを保存**
   ```
   get_token.py
   ```

4. **コマンドプロンプトで実行**
   ```bash
   python get_token.py
   ```

5. **出力された Refresh Token をコピー**

---

## ステップ8: config.json 作成

### 8-1. テンプレートファイルを開く

1. **ファイルエクスプローラーを開く**
   - Windows キー + E

2. **以下に移動**
   ```
   C:\Users\user\gomi_reminder_system
   ```

3. **config.json.template を右クリック**

4. **「プログラムから開く」→「メモ帳」を選択**

### 8-2. 認証情報を入力

メモ帳が開いたら、以下の部分を編集：

```json
{
  "device_id": "YOUR_DEVICE_ID",          ← ここを置き換え
  "refresh_token": "YOUR_REFRESH_TOKEN",  ← ここを置き換え
  "client_id": "YOUR_CLIENT_ID",          ← ここを置き換え
  "client_secret": "YOUR_CLIENT_SECRET"   ← ここを置き換え
}
```

**例（実際の値）:**
```json
{
  "device_id": "amzn1.ask.device.ABC123456789",
  "refresh_token": "Atzr|IwEBIHZaxxx...",
  "client_id": "amzn1.application.6c8d8f...",
  "client_secret": "8d1f2a9b7c4e6f3h..."
}
```

### 8-3. 保存

1. **「ファイル」→「名前をつけて保存」をクリック**

2. **ファイル名を変更**
   ```
   config.json
   ```
   （.template を削除）

3. **文字コード を「UTF-8」に設定**
   - メモ帳の「エンコード」メニューから選択

4. **保存先**
   ```
   C:\Users\user\gomi_reminder_system
   ```

5. **「保存」をクリック**

### ✅ 確認

ファイルエクスプローラーで `config.json` が見えたら成功です

---

# 【テスト】

## ステップ9: テスト実行

### 9-1. テストモードで実行

コマンドプロンプトで以下を実行：

```bash
cd C:\Users\user\gomi_reminder_system
python main.py --mode test --once
```

### 9-2. 実行画面

```
============================================================
ゴミ出し日程Alexa通知システム
============================================================
実行モード: test
テスト実行: True
============================================================

1回のテスト実行を開始
[テストモード] Alexa通知送信
  Device ID: amzn1.ask.device.ABC123456789
  Message: 明日は燃やすごみの日です

テスト実行完了
```

### 9-3. Alexa デバイスで確認

✅ **テスト成功:**
- Alexaデバイスの画面に通知が表示される

⚠️ **テスト失敗:**
- 通知が表示されない場合は、以下を確認：
  1. Device ID が正しいか
  2. Refresh Token が有効か
  3. インターネット接続
  4. config.json が正しい形式か

---

# 【自動実行設定】

## ステップ10: Windows Task Scheduler で自動起動設定

### 10-1. Task Scheduler を起動

1. **Windows キー + R を押す**

2. **「tasksched.msc」と入力 → Enter**

3. **Task Scheduler が起動します**

### 10-2. 基本タスクを作成

1. **右側パネルの「基本タスクの作成」をクリック**

2. **「名前」を入力**
   ```
   Gomi Reminder System
   ```

3. **「説明」を入力（オプション）**
   ```
   ゴミ出し日程Alexa通知システム
   ```

4. **「次へ」をクリック**

### 10-3. トリガーを設定

1. **「トリガー」タブで「毎日」を選択**

2. **以下を設定**
   ```
   開始: 2026年5月9日
   時刻: 08:00:00
   繰り返し: 1日
   ```

3. **「次へ」をクリック**

### 10-4. 操作を設定

1. **「操作」で「プログラムの開始」を選択**

2. **プログラム/スクリプト を入力**
   ```
   C:\Users\user\gomi_reminder_system\start_gomi_reminder.bat
   ```

3. **「次へ」をクリック**

### 10-5. 条件を設定（オプション）

1. **「コンピューターがAC電源で動作している場合のみ実行」** をチェック

2. **「次へ」をクリック**

### 10-6. 確認と保存

1. **設定内容を確認**

2. **「完了」をクリック**

### ✅ 確認

Task Scheduler のタスク一覧に「Gomi Reminder System」が表示されたら成功です

---

## ステップ11: 動作確認

### 11-1. 手動実行テスト

1. **Task Scheduler で「Gomi Reminder System」を右クリック**

2. **「実行」をクリック**

3. **コマンドプロンプトウィンドウが一瞬表示される**

4. **ログファイルを確認**
   ```
   C:\Users\user\gomi_reminder_system\gomi_reminder.log
   ```

### 11-2. 自動実行テスト

1. **PCを再起動**

2. **起動後、gomi_reminder.log を確認**
   ```
   自動で起動してログが記録されていることを確認
   ```

---

# 【本番運用開始】

## ステップ12: 本番運用開始

### 12-1. バッチファイルを編集

1. **start_gomi_reminder.bat をメモ帳で開く**

2. **以下の行を確認**
   ```
   python main.py --mode real
   ```

3. **保存**

### 12-2. 本番運用開始

これ以降、以下が自動実行されます：

```
毎日 08:00:00 に start_gomi_reminder.bat が起動
  ↓
毎日 18:00, 19:00, 20:00, 21:00, 22:00, 23:00 に自動チェック実行
  ↓
明日がゴミ出し日の場合のみ Alexa に通知送信
```

---

# 🔍 トラブルシューティング

## 問題:「config.json が見つかりません」

**原因**: config.json が正しく作成されていない

**解決方法:**
1. `config.json.template` をコピー
2. 名前を `config.json` に変更
3. 認証情報を入力
4. 保存場所: `C:\Users\user\gomi_reminder_system\`

---

## 問題: 「Pythonが見つかりません」

**原因**: Pythonがインストールされていないか、PATHに登録されていない

**解決方法:**
1. Pythonを再インストール
2. **「Add Python to PATH」にチェック**
3. PCを再起動

---

## 問題: Alexa 通知が来ない

**確認項目:**

1. **Device ID が正しいか**
   ```
   Alexa App で再度確認してコピー
   ```

2. **Refresh Token が有効か**
   ```
   有効期限確認（ステップ7で再取得）
   ```

3. **インターネット接続**
   ```
   ping google.com
   ```

4. **ファイアウォール設定**
   - Windowsファイアウォールで Python を許可

5. **ログを確認**
   ```
   gomi_reminder.log を開いてエラーメッセージを確認
   ```

---

## 問題: Task Scheduler で自動起動しない

**確認項目:**

1. **バッチファイルが存在するか**
   ```
   C:\Users\user\gomi_reminder_system\start_gomi_reminder.bat
   ```

2. **タスクのプロパティを確認**
   - パスが正しいか
   - 「最上位の権限で実行」がチェックされているか

3. **手動実行テスト**
   ```
   Task Scheduler で右クリック → 実行
   ```

4. **ログで確認**
   ```
   イベントビューアーで確認
   ```

---

# ✨ セットアップ完了！

以上でセットアップが完了です。

毎日、以下の時間に自動的に Alexa に通知が届きます：

- 18:00
- 19:00
- 20:00
- 21:00
- 22:00
- 23:00

**ゴミを出す前日の18:00-23:00に「明日は○○ゴミの日です」と通知されます。**

---

# 📞 ご不明な点

- ドキュメント: README.md
- システム詳細: SYSTEM_OVERVIEW.md
- トラブル対応: README.md「トラブルシューティング」

ご不明な点はいつでもお気軽にお問い合わせください！

