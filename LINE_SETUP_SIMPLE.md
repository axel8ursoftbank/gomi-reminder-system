# 📱 LINE通知版 - シンプルセットアップ（10分）

**LINE Messaging APIを使った最もシンプルな方法です。**

---

## 【ステップ1】LINE Bot を作成（3分）

### 1-1. LINE Developers Console にアクセス

```
https://developers.line.biz/console/
```

### 1-2. ログイン

- LINEアカウントでログイン

### 1-3. チャネルを作成

```
「Create」をクリック
  ↓
プロバイダー名: Gomi Reminder
チャネルタイプ: Messaging API
チャネル名: Gomi Reminder
  ↓
「作成」
```

---

## 【ステップ2】Channel Access Token を取得（1分）

### 2-1. チャネル設定を開く

```
作成したチャネルをクリック
  ↓
「Messaging API」タブ
```

### 2-2. トークンを取得

```
「Issue」をクリック
  ↓
長い文字列が表示される（Channel Access Token）
  ↓
コピー
```

**例：**
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

## 【ステップ3】User ID を取得（2分）

### 3-1. Bot を友達追加

```
「QR code」を見つける
  ↓
スマートフォンのカメラで読み込む
  ↓
「追加」をクリック
```

### 3-2. User ID を確認

以下の2つの方法のどちらか：

**方法A: Webhook ログから**
```
LINE bot にメッセージを送る
  ↓
Developers Console の Webhook セクションを見る
  ↓
"userId": "U1234..." をコピー
```

**方法B: LINE Official Account Manager から**
```
https://manager.line.biz/ にアクセス
  ↓
左側「自動応答」
  ↓
User ID を確認
```

**例：**
```
U1234567890abcdef1234567890abcdef
```

---

## 【ステップ4】config.json を作成（2分）

### 4-1. config.json を作成

```
C:\Users\user\gomi_reminder_system\config.json
```

を以下の内容で作成：

```json
{
  "notification_type": "line",
  "line_channel_access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "line_user_id": "U1234567890abcdef1234567890abcdef"
}
```

### 4-2. 注意

- `line_channel_access_token` に Channel Access Token をペースト
- `line_user_id` に User ID をペースト
- ダブルクォーテーションを削除しないこと
- ファイルを保存

---

## 【ステップ5】テスト実行（2分）

### 5-1. コマンドを実行

```bash
cd C:\Users\user\gomi_reminder_system
python main.py --mode test --once
```

### 5-2. LINE で確認

スマートフォンのLINEを見て、メッセージが届いたか確認

```
画面に表示される内容:
「[テストモード] LINE通知送信」
```

**LINEに来るメッセージの例:**
```
明日は燃やすごみ、缶の日です
```

---

## 【ステップ6】自動実行設定（5分）

### 6-1. Windows Task Scheduler を開く

```
Windows キー + R
  ↓
「tasksched.msc」と入力
  ↓
Enter
```

### 6-2. 基本タスクを作成

```
右側「基本タスクの作成」をクリック

【一般】
名前: Gomi Reminder System

【トリガー】
毎日 08:00

【操作】
C:\Users\user\gomi_reminder_system\start_gomi_reminder.bat

【完了】
```

---

## ✅ 完成！

毎日自動的にLINEで通知が届きます。

```
毎日 08:00 → PC が自動起動
毎日 18:00-23:00 → 毎時間チェック
           → 明日がゴミ出し日なら LINE で通知
```

---

## 🆘 トラブル

### LINE に通知が来ない

確認項目：
```
□ Channel Access Token が正しいか
□ User ID が正しいか
□ Bot が友達追加されているか
□ config.json が正しい形式か
```

### 「module not found」エラー

```bash
pip install requests
```

---

## 📞 参考

詳細ガイド: `LINE_MESSAGING_API_SETUP.md`

