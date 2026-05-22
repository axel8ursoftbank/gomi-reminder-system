# 📱 LINE Messaging API でゴミ出し日程通知 - セットアップガイド

**LINE Messaging APIを使ってLINE botから通知します。**

---

## 準備

- ✅ Lineアカウント（個人アカウント）
- ✅ Messaging API 用の Channel を作成できる状態

---

# 【ステップ1】LINE Developers Console にアクセス

## 1-1. ブラウザでアクセス

```
https://developers.line.biz/ja/
```

または

```
https://developers.line.biz/console/channel/
```

## 1-2. ログイン

1. **「ログイン」をクリック**
2. **LINEアカウントでログイン**

---

# 【ステップ2】Messaging API チャネルを作成

## 2-1. 新しいプロバイダーを作成

1. **「Create」をクリック**
2. **プロバイダー名を入力**
   ```
   Gomi Reminder
   ```

## 2-2. Messaging API チャネルを作成

1. **「Create channel」をクリック**
2. **チャネルタイプ：「Messaging API」を選択**
3. **情報を入力**
   ```
   チャネル名: Gomi Reminder
   チャネルの説明: Garbage collection reminder
   大業種: 個人
   小業種: その他
   ```
4. **「作成」をクリック**

---

# 【ステップ3】Channel Access Token を取得

## 3-1. チャネル設定ページを開く

1. **作成されたチャネルをクリック**
2. **「Messaging API」タブを選択**

## 3-2. Channel Access Token を取得

```
ページイメージ:
┌────────────────────────────────┐
│ Channel access token           │
│                                │
│ [Issue]                        │ ← クリック
│                                │
│ トークンが表示される            │
│ eyJhbGciOiJIUzI1NiIs...        │
└────────────────────────────────┘
```

1. **「Issue」をクリック**
2. **Channel Access Token をコピー**

```
Channel Access Token:
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

# 【ステップ4】User ID を取得

## 4-1. Bot を友達追加

1. **同じページで「QR code」を見つける**
2. **QRコードをスマートフォンのカメラで読み込む**
3. **「追加」をクリック**

## 4-2. User ID を取得

### 方法1: Webhook を使う（簡単）

1. **LINE bot にメッセージを送る**
   - 「こんにちは」など任意のメッセージ

2. **Developers Console で Webhook ログを確認**
   - メッセージに含まれる userId をコピー
   ```
   "userId": "U1234567890abcdef1234567890abcdef"
   ```

### 方法2: LINE Official Account Manager から取得

1. **LINE Official Account Manager にアクセス**
   ```
   https://manager.line.biz/
   ```
2. **左側メニュー →「自動応答」**
3. **Bot の情報から User ID を確認

---

# 【ステップ5】config.json を設定

## 5-1. 認証情報をまとめる

メモ帳に以下をまとめます：

```
LINE Messaging API 認証情報
========================================

Channel Access Token:
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

User ID:
U1234567890abcdef1234567890abcdef

========================================
```

## 5-2. config.json を編集

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

---

# 【ステップ6】システムを更新

Python モジュールを LINE Messaging API 対応に変更します。

## 6-1. alexa_notifier.py を line_notifier.py に変更

```python
# C:\Users\user\gomi_reminder_system\line_notifier.py

import requests
import json
import sys
import os
from typing import List

class LineNotifier:
    """LINE Messaging API 通知クラス"""
    
    LINE_API_ENDPOINT = "https://api.line.me/v2/bot/message/push"
    
    def __init__(self, config_file: str = None):
        self.config_file = config_file or r"C:\Users\user\gomi_reminder_system\config.json"
        self.config = self._load_config()
    
    def _load_config(self) -> dict:
        """設定ファイルを読み込む"""
        if not os.path.exists(self.config_file):
            raise FileNotFoundError(f"config.json が見つかりません: {self.config_file}")
        
        with open(self.config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def send_message(self, message: str, test_mode: bool = False) -> bool:
        """LINE にメッセージを送信"""
        
        channel_access_token = self.config.get('line_channel_access_token')
        user_id = self.config.get('line_user_id')
        
        if not channel_access_token or not user_id:
            raise ValueError("Channel Access Token または User ID が設定されていません")
        
        if test_mode:
            print(f"[テストモード] LINE通知送信")
            print(f"  ユーザーID: {user_id}")
            print(f"  メッセージ: {message}")
            return True
        
        try:
            headers = {
                "Authorization": f"Bearer {channel_access_token}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "to": user_id,
                "messages": [
                    {
                        "type": "text",
                        "text": message
                    }
                ]
            }
            
            response = requests.post(
                self.LINE_API_ENDPOINT,
                headers=headers,
                json=payload
            )
            
            if response.status_code == 200:
                print(f"✓ LINE通知送信完了: {message}")
                return True
            else:
                print(f"✗ LINE通知送信失敗 (Status: {response.status_code})")
                print(f"  Response: {response.text}")
                return False
        
        except Exception as e:
            print(f"✗ エラー: {e}")
            return False
    
    def send_garbage_reminder(self, garbage_types: List[str], test_mode: bool = False) -> bool:
        """ゴミ出し通知を送信"""
        
        if not garbage_types:
            print("通知対象のゴミがありません")
            return False
        
        # メッセージを組み立て
        if len(garbage_types) == 1:
            message = f"明日は{garbage_types[0]}の日です"
        else:
            types_str = "、".join(garbage_types)
            message = f"明日は{types_str}の日です"
        
        return self.send_message(message, test_mode=test_mode)
```

## 6-2. main.py を更新

```python
# main.py の以下の部分を変更

from line_notifier import LineNotifier

# ...

class GomiReminderScheduler:
    def __init__(self, config_mode='real'):
        # ...
        try:
            self.line_notifier = LineNotifier()
        except Exception as e:
            logger.warning(f"LINE通知初期化: {e}")
            self.line_notifier = None
    
    def check_and_notify(self):
        try:
            if not self.schedule_checker:
                logger.warning("スケジュールチェッカーが初期化されていません")
                return
            
            has_garbage, garbage_types = self.schedule_checker.check_tomorrow()
            
            if has_garbage:
                logger.info(f"明日のゴミ: {', '.join(garbage_types)}")
                
                if self.line_notifier:
                    test_mode = (self.config_mode == 'test')
                    self.line_notifier.send_garbage_reminder(
                        garbage_types,
                        test_mode=test_mode
                    )
                else:
                    logger.warning("LINE通知が利用できません")
            else:
                logger.debug("明日はゴミ出し日ではありません")
        
        except Exception as e:
            logger.error(f"スケジュール確認エラー: {e}")
```

---

# 【ステップ7】テスト実行

## 7-1. テストモードで実行

```bash
cd C:\Users\user\gomi_reminder_system
python main.py --mode test --once
```

## 7-2. LINE で通知を確認

スマートフォンのLINEを見て、メッセージが届いたか確認します。

```
メッセージ例:
「明日は燃やすごみ、缶の日です」
```

---

# 【ステップ8】自動実行設定

## 8-1. Windows Task Scheduler で設定

1. **Windows キー + R → tasksched.msc**
2. **「基本タスクの作成」**
3. **以下を設定**
   ```
   名前: Gomi Reminder System
   トリガー: 毎日 08:00
   操作: C:\Users\user\gomi_reminder_system\start_gomi_reminder.bat
   ```

---

# ✅ 完成！

毎日自動的にLINEで通知が届きます。

```
毎日 08:00 → PC 自動起動
毎日 18:00-23:00 → 明日のゴミをチェック
         → LINE で通知送信
```

---

# 🆘 トラブルシューティング

## 問題: 「config.json が見つかりません」

```json
{
  "notification_type": "line",
  "line_channel_access_token": "...",
  "line_user_id": "..."
}
```

を作成して保存してください

## 問題: LINE に通知が来ない

確認項目：
1. **Channel Access Token が正しいか**
2. **User ID が正しいか**
3. **Bot が友達追加されているか**
4. **ネットワーク接続**

## 問題: User ID が見つからない

方法：
1. LINE Official Account Manager から確認
2. または Bot にメッセージ送信後、Webhook ログから取得

---

これで LINE Messaging API を使った通知が実装できます！

