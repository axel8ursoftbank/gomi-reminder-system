# 🔐 Amazon Developer Console で認証情報を取得する - 超詳細ガイド

**このガイドは、Amazon Developer Console での設定を、ステップバイステップで説明しています。**

---

## 前提条件

- ✅ インターネット接続できるパソコン
- ✅ Webブラウザ（Chrome、Edge など）
- ✅ Amazonアカウント
  - なければ作成してください：https://www.amazon.co.jp

---

# 【ステップ1】Amazon Developer Console にアクセス

### 1-1. ブラウザを開く

1. **Chrome、Edge、Safari など任意のブラウザを開いてください**

2. **以下のURLを入力 or コピー＆ペースト**

   ```
   https://developer.amazon.com
   ```

3. **Enter キーを押す**

### 1-2. ページが開きます

```
画面イメージ：
┌─────────────────────────────────┐
│ Amazon Developer Portal          │
│                                 │
│  [Sign In]  [Tools] [Community] │
│                                 │
│  Alexa Skills Kit               │
│  Build and publish Alexa Skills │
│                                 │
└─────────────────────────────────┘
```

### 1-3. 「Sign In」をクリック

1. **右上の「Sign In」ボタンをクリック**

2. **Amazonアカウントでログイン**
   - メールアドレスと パスワードを入力
   - 「サインイン」をクリック

### 1-4. ログイン後

1. **画面右上に自分のアカウント名が表示されます**

   例：「kinoshita@example.com」

2. ✅ ログイン成功

---

# 【ステップ2】Alexa Skills Kit にアクセス

### 2-1. 左側のメニューから Alexa を探す

ページ左側に以下のようなメニューが見えます：

```
メニュー例：
┌──────────────────────┐
│ Alexa Skills Kit     │ ← ここ
│ Alexa for Business   │
│ AWS                  │
│ その他...             │
└──────────────────────┘
```

### 2-2. 「Alexa Skills Kit」をクリック

1. **メニューから「Alexa Skills Kit」をクリック**

2. **Alexa Skills Kit のページが開きます**

3. **「Alexa Developer Console」をクリック**

```
ページイメージ：
┌──────────────────────────────┐
│ Alexa Skills Kit              │
│                              │
│ [Alexa Developer Console] ←  ここをクリック
│                              │
│ [AWS Lambda] [AWS Account]   │
└──────────────────────────────┘
```

---

# 【ステップ3】スキルを作成

### 3-1. Create Skill ボタン

Alexa Developer Console が開きます：

```
ページイメージ：
┌──────────────────────────┐
│ Your Skills              │
│                          │
│  [Create Skill] ← ここをクリック
│                          │
│  Skill List:            │
│  （最初は空）             │
└──────────────────────────┘
```

### 3-2. 「Create Skill」をクリック

1. **「Create Skill」ボタンをクリック**

2. **スキル作成フォームが表示されます**

### 3-3. スキル情報を入力

**画面に以下のフォームが表示されます：**

```
┌────────────────────────────────┐
│ Skill name:                    │
│ [____________________________] │ ← 入力
│                                │
│ Primary locale:                │
│ [Japanese (Japan)] ← 選択      │
│                                │
│ Choose a model:                │
│ ○ Custom                       │
│ ○ Fact Skill                   │
│ ○ Flash Briefing              │
└────────────────────────────────┘
```

### 3-4. 情報を入力

1. **「Skill name」に以下を入力**

   ```
   Gomi Reminder
   ```

   （または任意の名前）

2. **「Primary locale」が「Japanese (Japan)」になっているか確認**
   - なっていなければ、ドロップダウンから選択

3. **「Choose a model」で「Custom」を選択**
   - 円形のボタンをクリック

4. **「Create skill」ボタンをクリック**

### 3-5. スキルが作成されました ✅

```
スキルダッシュボード
┌──────────────────────────────┐
│ Gomi Reminder                │
│                              │
│ Skill ID: amzn1.ask...      │
│                              │
│ [Invocation] [Intents] ...   │
│                              │
│ Published: No                │
└──────────────────────────────┘
```

---

# 【ステップ4】Security Profile を作成

### 4-1. Security Profiles へのアクセス

1. **Amazon Developer Console のトップページに戻る**
   - 左上の「Alexa」ロゴをクリック

2. **右上のメニューアイコン（≡）をクリック**

3. **「Security Profiles」を探してクリック**

   ```
   メニュー例：
   ┌──────────────────────┐
   │ Alexa Console Home   │
   │ Security Profiles ←  ここ
   │ Manage Login with... │
   │ Log Out              │
   └──────────────────────┘
   ```

### 4-2. Security Profiles ページ

以下のようなページが表示されます：

```
┌────────────────────────────────┐
│ Security Profiles              │
│                                │
│ [Create Security Profile] ←    │
│                                │
│ Profile List:                  │
│ （最初は空）                    │
└────────────────────────────────┘
```

### 4-3. 「Create Security Profile」をクリック

1. **「Create Security Profile」をクリック**

2. **フォームが表示されます**

```
┌────────────────────────────────┐
│ Security Profile Name:         │
│ [____________________________] │ ← 入力
│                                │
│ Description (optional):        │
│ [____________________________] │ ← 入力
└────────────────────────────────┘
```

### 4-4. 情報を入力

1. **「Security Profile Name」に入力**

   ```
   Gomi_Reminder_Profile
   ```

2. **「Description」に入力**

   ```
   Garbage collection reminder notifications
   ```

3. **「Next」をクリック**

### 4-5. Security Profile が作成されました ✅

---

# 【ステップ5】Client ID と Client Secret を取得

### 5-1. Client Credentials を確認

作成した Security Profile のページが表示されます：

```
ページイメージ：
┌─────────────────────────────────┐
│ Gomi_Reminder_Profile           │
│                                 │
│ Security Profile Details        │
│                                 │
│ General │ Web Settings │ Other  │
│                                 │
│ [Show Client ID]                │
│ [Show Client Secret]            │
└─────────────────────────────────┘
```

### 5-2. Client ID をコピー

1. **「Show Client ID」をクリック**

2. **Client ID が表示されます**

   例：
   ```
   amzn1.application.6c8d8f1a2b3c4d5e6f7g8h9i0j
   ```

3. **その文字列を右クリック → コピー**

   または：
   - 選択して Ctrl + C キーを押す

4. **メモ帳に貼り付けて保存**

   ```
   ========== Alexa認証情報 ==========
   
   Client ID:
   amzn1.application.6c8d8f1a2b3c4d5e6f7g8h9i0j
   ```

### 5-3. Client Secret をコピー

1. **「Show Client Secret」をクリック**

2. **Client Secret が表示されます**

   例：
   ```
   8d1f2a9b7c4e6f3h5i2j8k1l9m6n3o4p
   ```

3. **メモ帳に貼り付けて保存**

   ```
   ========== Alexa認証情報 ==========
   
   Device ID:
   amzn1.ask.device.ABCDEFGHIJKLMNOPQRSTUVWXYZ
   
   Client ID:
   amzn1.application.6c8d8f1a2b3c4d5e6f7g8h9i0j
   
   Client Secret:
   8d1f2a9b7c4e6f3h5i2j8k1l9m6n3o4p
   ```

---

# 【ステップ6】Web Settings を設定

### 6-1. Web Settings タブをクリック

Security Profile のページで：

1. **「Web Settings」タブをクリック**

2. **編集フォームが表示されます**

```
┌────────────────────────────────────┐
│ Web Settings                       │
│                                    │
│ Allowed Return URLs:               │
│ [__________________________] ← 入力  │
│ [+ Add URL]                        │
│                                    │
│ Allowed Origins:                   │
│ [__________________________] ← 入力  │
│ [+ Add Origin]                     │
└────────────────────────────────────┘
```

### 6-2. Allowed Return URLs を入力

1. **テキストボックスをクリック**

2. **以下を入力**

   ```
   https://pitangui.amazon.com/auth/o2/oauth/success
   ```

3. **「+ Add URL」をクリック**

4. **もう1つ入力**

   ```
   https://localhost:3000/callback
   ```

5. **「+ Add URL」をクリック**

最終的に：
```
Allowed Return URLs:
✓ https://pitangui.amazon.com/auth/o2/oauth/success
✓ https://localhost:3000/callback
```

### 6-3. Allowed Origins を入力

1. **「Allowed Origins」のテキストボックスをクリック**

2. **以下を入力**

   ```
   https://pitangui.amazon.com
   ```

3. **「+ Add Origin」をクリック**

4. **もう1つ入力**

   ```
   https://localhost:3000
   ```

5. **「+ Add Origin」をクリック**

最終的に：
```
Allowed Origins:
✓ https://pitangui.amazon.com
✓ https://localhost:3000
```

### 6-4. 「Save」をクリック

1. **ページの下部の「Save」ボタンをクリック**

2. **✅ 「Web Settings saved」と表示されたら成功**

---

# 【ステップ7】Refresh Token を取得

### ⚠️ 難易度：中程度

このステップは少し複雑です。慎重に進めてください。

### 7-1. ブラウザで認可ページを開く

**新しいタブを開いて、以下を入力:**

```
https://www.amazon.com/ap/oa?client_id=YOUR_CLIENT_ID&scope=alexa:devices:all&response_type=code&redirect_uri=https://localhost:3000/callback
```

**⚠️ 重要: YOUR_CLIENT_ID を置き換えてください**

例：
```
Client ID が amzn1.application.6c8d8f1a2b3c4d5e6f7g8h9i0j の場合：

https://www.amazon.com/ap/oa?client_id=amzn1.application.6c8d8f1a2b3c4d5e6f7g8h9i0j&scope=alexa:devices:all&response_type=code&redirect_uri=https://localhost:3000/callback
```

### 7-2. Amazonでログイン

1. **ページが開いて、以下のような画面が表示されます**

   ```
   Amazonサインイン画面
   ┌──────────────────────────┐
   │ Amazon.co.jp             │
   │                          │
   │ メールアドレス           │
   │ [___________________]    │
   │                          │
   │ パスワード               │
   │ [___________________]    │
   │                          │
   │    [サインイン]           │
   └──────────────────────────┘
   ```

2. **Amazonアカウントでログイン**
   - メールアドレスを入力
   - パスワードを入力
   - 「サインイン」をクリック

### 7-3. 許可ページが表示されます

```
許可ページ
┌───────────────────────────────┐
│ Alexa デバイスへのアクセス許可 │
│                               │
│ Gomi Reminder が以下にアクセス │
│ したいと要求しています:        │
│                               │
│ □ Alexa デバイスの一覧        │
│ □ Alexa デバイスの情報        │
│                               │
│  [許可する]  [拒否する]        │
└───────────────────────────────┘
```

### 7-4. 「許可する」をクリック

1. **「許可する」ボタンをクリック**

2. **ブラウザのアドレスバーが変わります**

   ```
   https://localhost:3000/callback?code=Atzr|IwEBIE...
   ```

### 7-5. code をコピー

1. **アドレスバーを見てください**

2. **「code=」の後ろの長い文字列をコピーします**

   ```
   コピーする部分：
   code=Atzr|IwEBIEZkx2q3gxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
                    ↑
                    ここから最後まで
   ```

3. **メモ帳に貼り付けます**

   ```
   Authorization Code:
   Atzr|IwEBIEZkx2q3gxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

### 7-6. Refresh Token を取得

⚠️ **複雑な操作です。慎重に進めてください。**

#### 方法A: Python スクリプト（推奨・簡単）

1. **テキストエディタを開く**

2. **以下を全てコピー**

   ```python
   import requests
   import json

   # ここを編集 ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
   code = "Atzr|IwEBIE..."  # 上記でコピーした code
   client_id = "amzn1.application.6c8d..."  # Client ID
   client_secret = "8d1f2a9b..."  # Client Secret
   # ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝

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

   if "refresh_token" in result:
       print("✅ 成功！")
       print("\nRefresh Token:")
       print(result.get("refresh_token"))
   else:
       print("❌ エラー:")
       print(result)
   ```

3. **赤い部分（# ここを編集 の3行）を自分の情報に置き換え**

   ```python
   code = "Atzr|IwEBIE..."           # ← 7-5でコピーしたコード
   client_id = "amzn1.application...."  # ← Client ID
   client_secret = "8d1f..."        # ← Client Secret
   ```

4. **ファイルを保存**
   - 名前: `get_refresh_token.py`
   - 場所: `C:\Users\user\gomi_reminder_system`

5. **コマンドプロンプトで実行**

   ```bash
   cd C:\Users\user\gomi_reminder_system
   pip install requests
   python get_refresh_token.py
   ```

6. **実行結果**

   ```
   ✅ 成功！

   Refresh Token:
   Atzr|IwEBIHZaxxx...
   ```

7. **Refresh Token をメモ帳に保存**

#### 方法B: Curl コマンド（上級）

Windows の PowerShell で以下を実行：

```powershell
$code = "Atzr|IwEBIE..."  # コピーした code
$client_id = "amzn1.application...."  # Client ID
$client_secret = "8d1f..."  # Client Secret

curl.exe -X POST https://api.amazon.com/auth/o2/token `
  -H "Content-Type: application/x-www-form-urlencoded" `
  -d "grant_type=authorization_code&code=$code&client_id=$client_id&client_secret=$client_secret&redirect_uri=https://localhost:3000/callback"
```

**返された JSON から refresh_token をコピーします**

---

# 【完了】4つの認証情報をすべて集めました！

メモ帳に以下が揃っているか確認：

```
========== Alexa認証情報 ==========

Device ID:
amzn1.ask.device.ABCDEFGHIJKLMNOPQRSTUVWXYZ

Client ID:
amzn1.application.6c8d8f1a2b3c4d5e6f7g8h9i0j

Client Secret:
8d1f2a9b7c4e6f3h5i2j8k1l9m6n3o4p

Refresh Token:
Atzr|IwEBIHZaxxx...

====================================
```

✅ **すべて揃ったら、次のステップに進みます！**

---

# 🎯 次のステップ

config.json を作成します：

1. **DETAILED_SETUP_GUIDE.md の「ステップ8」を参照**
2. **上記の4つの情報を config.json に入力**
3. **ファイルを保存**

---

## 🆘 トラブルシューティング

### 問題: code が取得できない

**原因**: 「許可する」をクリックしなかった

**解決方法**:
1. ステップ7-1 の URL を再度開く
2. 「許可する」をクリック
3. アドレスバーから code をコピー

### 問題: Refresh Token が表示されない

**原因**: Client ID/Secret が間違っている

**解決方法**:
1. Client ID/Secret を再度確認
2. Security Profile ページで「Show」をクリック
3. 完全にコピー（余分なスペースなし）
4. スクリプトを再実行

---

**これで4つの認証情報がすべて揃いました！**
**次は config.json を作成します。**

