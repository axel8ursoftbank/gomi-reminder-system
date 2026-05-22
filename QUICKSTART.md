# クイックスタートガイド

ゴミ出し日程Alexa通知システムを5分で開始する方法です。

---

## 前提条件

- ✅ Windows 10 以降
- ✅ Python 3.9 以上
- ✅ インターネット接続
- ✅ Amazonアカウント
- ✅ Alexa対応デバイス

---

## ステップ1: ファイルセットアップ (2分)

```bash
# コマンドプロンプトで以下を実行
cd C:\Users\user\gomi_reminder_system

# 必要なパッケージをインストール
pip install -r requirements.txt

# スケジュール情報を抽出
python extract_schedule.py
```

**確認事項:**
- `schedule_cache.json` が作成されたか
- スケジュール抽出が完了したか

---

## ステップ2: Alexa認証設定 (2分 + 認証待ち)

### 簡単版: 基本情報の取得

1. **Device IDを取得**
   - Alexa App を開く
   - 左上「≡」 → 「デバイス」
   - 通知を受け取るデバイスを選択
   - 詳細情報から "Device ID" をコピー

2. **Amazon Developer Console へ**
   - https://developer.amazon.com へアクセス
   - 「Alexa Skills Kit」を選択
   - スキルを新規作成して "Client ID" と "Client Secret" を取得

3. **Refresh Token を取得**
   - SETUP_ALEXA.md の「ステップ5」を参照

### 設定ファイル作成

`config.json` を以下の内容で作成:

```json
{
  "device_id": "ここにDevice IDをペースト",
  "refresh_token": "ここにRefresh Tokenをペースト",
  "client_id": "ここにClient IDをペースト",
  "client_secret": "ここにClient Secretをペースト"
}
```

**保存場所**: `C:\Users\user\gomi_reminder_system\config.json`

---

## ステップ3: テスト実行 (1分)

```bash
# テストモードで実行（Alexa通知は表示されません）
python main.py --mode test --once

# 以下が表示されたら成功
# 「テスト実行完了」
```

---

## ステップ4: 本番運用開始

### オプションA: 自動起動（推奨）

Windows Task Scheduler で自動起動を設定:

```bash
# SETUP_TASK_SCHEDULER.md を参照して設定
# または以下の簡易手順を使用

# 1. バッチファイルを作成
# start_gomi_reminder.bat（既に存在）

# 2. タスクスケジューラーを起動
tasksched.msc

# 3. 「基本タスクの作成」
#    - 名前: Gomi Reminder System
#    - トリガー: 毎日 08:00
#    - 操作: start_gomi_reminder.bat を実行
```

### オプションB: 手動実行

毎日、または必要な時に手動で実行:

```bash
python main.py --mode real
```

---

## 完了チェックリスト

- [ ] Python 3.9+ がインストール済み
- [ ] `schedule_cache.json` が作成済み
- [ ] Amazon Developer Console でスキルを作成済み
- [ ] Device ID を取得済み
- [ ] Refresh Token を取得済み
- [ ] `config.json` を作成済み
- [ ] テスト実行で成功
- [ ] Task Scheduler で自動起動を設定済み

---

## よくある問題と解決

### 「config.json が見つかりません」

→ `config.json` を作成してください（テンプレートは `config.json.template`）

### 「Pythonが見つかりません」

→ Pythonをインストール後、パスに追加:
```bash
python --version
```

で確認できない場合はPythonを再インストール

### Alexa通知が来ない

1. Device ID が正しいか確認
2. Refresh Token の有効期限確認
3. ネットワーク接続確認
4. `gomi_reminder.log` でエラー確認

---

## 次のステップ

- 詳細な設定方法: [SETUP_ALEXA.md](SETUP_ALEXA.md)
- Task Scheduler詳細: [SETUP_TASK_SCHEDULER.md](SETUP_TASK_SCHEDULER.md)
- システム詳細: [README.md](README.md)
- トラブル対応: README.md の「トラブルシューティング」

---

## サポートドキュメント

| ドキュメント | 対象 |
|----------|------|
| [README.md](README.md) | 全般的な説明 |
| [SETUP_ALEXA.md](SETUP_ALEXA.md) | Amazon認証設定 |
| [SETUP_TASK_SCHEDULER.md](SETUP_TASK_SCHEDULER.md) | Windows自動起動 |
| このファイル | クイックスタート |

---

**準備完了！Alexa通知システムが稼働開始します🎉**

