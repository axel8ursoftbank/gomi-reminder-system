# ゴミ出し日程Alexa通知システム

加古川市「鳩里１」地区のゴミ出し予定を自動的に取得し、Alexaデバイスの画面に前日18:00-23:00の間、1時間ごとに「明日は○○ゴミの日です」と通知するシステムです。

---

## 機能

✅ **自動スケジュール抽出**
- 加古川市公開Excelファイル（R8gabcal_JPex.xlsx）から自動的にゴミ出し日程を抽出
- JSON形式でキャッシュして高速アクセス

✅ **複数ゴミ種別対応**
- 燃やすごみ（毎週月・木）
- 燃やさないごみ
- 缶、瓶、ペットボトル
- 紙類
- 剪定枝・草
- 蛍光灯・電池類

✅ **Alexa画面通知**
- Amazon Notifications APIを使用
- 複数のゴミ種別がある場合はまとめて通知
- テストモードで動作確認可能

✅ **自動スケジューリング**
- APSchedulerで毎日18:00-23:00に自動実行
- Windows Task Schedulerで常時実行管理

---

## ディレクトリ構成

```
gomi_reminder_system/
├── extract_schedule.py          # Phase 1: スケジュール抽出モジュール
├── schedule_cache.json          # 抽出済みスケジュール（JSON）
├── check_schedule.py            # Phase 2: スケジュール確認モジュール
├── alexa_notifier.py            # Phase 3: Alexa通知送信モジュール
├── main.py                      # Phase 4: メインスケジューラー
├── config.json.template         # 設定ファイル（テンプレート）
├── config.json                  # 設定ファイル（ユーザーが作成）
├── start_gomi_reminder.bat      # Windows 自動起動バッチファイル
├── requirements.txt             # Python依存パッケージ
├── gomi_reminder.log            # 実行ログ
│
├── SETUP_ALEXA.md               # Alexa設定ガイド
├── SETUP_TASK_SCHEDULER.md      # Windows Task Scheduler設定ガイド
├── README.md                    # このファイル
└── DEVELOPMENT.md               # 開発者向けドキュメント
```

---

## クイックスタート

### 1. 環境構築

```bash
# Python 3.9以上がインストールされていることを確認
python --version

# 依存パッケージのインストール
pip install -r requirements.txt
```

### 2. スケジュール抽出（初回のみ）

```bash
# Excelファイルからスケジュール情報を抽出
python extract_schedule.py
```

**出力例:**
```
ファイルを開いています: ...
スケジュール情報を抽出中...
✓ 燃やすごみ: 毎週月・木曜日
✓ 燃やさないごみ: 11件の日程
...
✓ スケジュールを保存しました: schedule_cache.json
```

### 3. スケジュール確認テスト

```bash
# 明日のゴミ出し予定を確認
python check_schedule.py
```

**出力例:**
```
==================================================
ゴミ出し日程チェック
==================================================

今日: 2026年05月09日（Saturday）
明日: 2026年05月10日（Sunday）
✗ 明日はゴミ出し日ではありません
```

### 4. Alexa通知設定

```bash
# SETUP_ALEXA.md を参照して認証情報を取得
# config.json を作成
```

### 5. テスト実行

```bash
# テストモードで1回実行（実通知は送信されません）
python main.py --mode test --once
```

### 6. 本番運用開始

```bash
# 実通知を送信しながら常時実行
python main.py --mode real
```

---

## セットアップガイド

### Alexa API設定
👉 **[SETUP_ALEXA.md](SETUP_ALEXA.md)** を参照

主な手順:
1. Amazon Developer Consoleでスキルを作成
2. Client ID/Secretを取得
3. Alexa Device IDを確認
4. Refresh Tokenを取得
5. config.json を作成

### Windows 自動起動設定
👉 **[SETUP_TASK_SCHEDULER.md](SETUP_TASK_SCHEDULER.md)** を参照

主な手順:
1. requirements.txt からパッケージをインストール
2. start_gomi_reminder.bat を作成
3. Windows Task Scheduler で定期実行を設定

---

## 使用方法

### 通常運用

PCを起動すると自動的にシステムが起動し、毎日18:00-23:00に自動チェックが実行されます。

明日がゴミ出し日の場合、Alexaデバイスの画面に通知が表示されます。

### ログ確認

```bash
# ログファイルをリアルタイムで監視
tail -f gomi_reminder.log

# または PowerShell
Get-Content -Path gomi_reminder.log -Wait -Tail 10
```

### マニュアルテスト

```bash
# テストモードで実行（Alexa通知画面のみ表示）
python main.py --mode test --once

# 本番モードで実行（実際にAlexa通知を送信）
python main.py --mode real --once
```

---

## トラブルシューティング

### 通知が送信されない

1. **config.json が正しいか確認**
   ```bash
   type config.json
   ```

2. **認証情報の有効性を確認**
   - Device ID
   - Refresh Token（有効期限）
   - Client ID/Secret

3. **ネットワーク接続を確認**
   ```bash
   ping api.amazonalexa.com
   ```

4. **ログを確認**
   ```bash
   tail -f gomi_reminder.log
   ```

### Python実行エラー

```bash
# 必要なパッケージが全てインストールされているか確認
pip list

# 不足しているパッケージを再インストール
pip install -r requirements.txt
```

### Task Schedulerで起動しない

1. バッチファイルが直接実行できるか確認
2. Pythonのフルパスを指定
3. Task Schedulerの「最上位の権限で実行」をチェック

---

## 日程更新

スケジュール情報は `schedule_cache.json` にキャッシュされています。

年度が変わった場合または情報を更新する場合:

```bash
# 新しいExcelファイルでスケジュールを再抽出
python extract_schedule.py
```

---

## 技術スタック

| 用途 | 技術 | 用途 |
|------|------|------|
| スケジュール解析 | openpyxl | Excelファイルの読み込み |
| スケジューリング | APScheduler | 定期実行管理 |
| HTTP通信 | requests | Alexa API呼び出し |
| 設定管理 | JSON, python-dotenv | 認証情報管理 |
| ログ出力 | logging | ログファイル管理 |

---

## セキュリティに関する注意

⚠️ **重要**: `config.json` には認証情報が含まれています

**してはいけないこと:**
- ❌ GitHub にアップロード
- ❌ メール添付で送信
- ❌ 共有フォルダに配置
- ❌ バージョン管理システムにコミット

**すべきこと:**
- ✅ ローカルPCのみに保存
- ✅ .gitignore に `config.json` を追加
- ✅ パスワードを共有しない
- ✅ トークンは定期的に更新

---

## よくある質問

**Q: 複数のゴミ種別が同じ日にある場合は?**
A: 全てのゴミを1つのメッセージにまとめて通知します。
```
「明日は燃やすごみ、かん、紙類の日です」
```

**Q: スケジュール情報は何年分保存されますか?**
A: デフォルトでは1年分（2026年）です。翌年の情報は新しいExcelファイルで更新してください。

**Q: 通知時刻を変更できますか?**
A: `main.py` の `for hour in [18, 19, 20, 21, 22, 23]:` の部分を編集して変更可能です。

**Q: 異なる地区に対応できますか?**
A: `extract_schedule.py` でシート番号を変更することで対応可能です。

---

## ライセンス

このプロジェクトはMITライセンスで公開されています。

---

## 開発情報

開発者向けのドキュメント: 👉 **[DEVELOPMENT.md](DEVELOPMENT.md)**

---

## サポート

問題が発生した場合:

1. ログファイル（`gomi_reminder.log`）を確認
2. トラブルシューティングセクションを参照
3. 各セットアップガイド（SETUP_*.md）を再確認

