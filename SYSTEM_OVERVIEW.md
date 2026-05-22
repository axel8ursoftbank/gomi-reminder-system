# ゴミ出し日程Alexa通知システム - システム概要

**実装完了日**: 2026年5月9日

---

## 📊 システム構成図

```
加古川市Excelファイル (R8gabcal_JPex.xlsx)
        ↓
[Phase 1: extract_schedule.py]
        ↓
schedule_cache.json (2026年全スケジュール)
        ↓
[Phase 2: check_schedule.py]
        ↓
明日のゴミ種別を判定
        ↓
[Phase 3: alexa_notifier.py]
        ↓
Amazon Notifications API
        ↓
Alexaデバイス画面に通知表示
```

---

## 📁 実装済みモジュール

### 1. **extract_schedule.py** ✅
**目的**: Excelファイルからゴミ出し日程を抽出

**機能:**
- シート2（鳩里１）のデータを読み込み
- 8種類のゴミを識別
- 燃やすごみ（毎週月・木）の固定スケジュール生成
- 月別スケジュールの抽出
- JSON形式で年間スケジュール情報を保存

**入力**: `R8gabcal_JPex.xlsx`（加古川市公開データ）
**出力**: `schedule_cache.json`

**実行例:**
```bash
python extract_schedule.py
```

**抽出対象ゴミ種別:**
- 燃やすごみ（毎週月・木曜日）
- 燃やさないごみ
- かん（缶）
- びん（瓶）
- 剪定枝・草
- ペットボトル
- 紙類
- 蛍光灯・電池

---

### 2. **check_schedule.py** ✅
**目的**: 指定日付のゴミ出し情報を判定

**機能:**
- JSONキャッシュから日程情報を読み込み
- 明日（または指定日）のゴミを判定
- ゴミの種類を特定
- 通知メッセージを生成

**実行例:**
```bash
python check_schedule.py
```

**出力:**
```
今日: 2026年05月09日（Saturday）
明日: 2026年05月10日（Sunday）
✗ 明日はゴミ出し日ではありません
```

---

### 3. **alexa_notifier.py** ✅
**目的**: Alexa画面にメッセージを送信

**機能:**
- Amazon Notifications APIに接続
- Refresh TokenからAccess Tokenを取得
- メッセージを指定デバイスに送信
- テストモード対応

**使用API:**
- `https://api.amazon.com/auth/o2/token` (認証)
- `https://api.amazonalexa.com/v1/notifications/reminder-notifications` (通知)

**実行例:**
```bash
python alexa_notifier.py  # テストモード
```

---

### 4. **main.py** ✅
**目的**: 各モジュールの統合とスケジューリング

**機能:**
- APSchedulerで毎日18:00-23:00の自動実行
- check_schedule.pyで日程判定
- alexa_notifier.pyで通知送信
- ロギング機能
- テストモード/本番モード切り替え

**実行モード:**
```bash
# テスト実行（1回のみ、通知画面表示のみ）
python main.py --mode test --once

# テスト実行（常時、自動スケジューリング）
python main.py --mode test

# 本番実行（実際に通知を送信）
python main.py --mode real
```

**スケジュール:**
- 毎日 18:00, 19:00, 20:00, 21:00, 22:00, 23:00 に自動実行
- 明日がゴミ出し日の場合のみ通知送信

---

## 📄 設定ファイル

### config.json （ユーザー作成）
**必須項目:**

```json
{
  "device_id": "amzn1.ask.device.XXXXX",
  "refresh_token": "Atzr|IwEBIHZ...",
  "client_id": "amzn1.application.XXXXX",
  "client_secret": "your_secret_here"
}
```

**取得方法:** SETUP_ALEXA.md を参照

---

## 📋 データフロー例

**例: 2026年5月11日（月）のゴミ出し日**

### 朝（8:00）
- PCが起動
- main.py が自動実行開始
- ログファイルを初期化

### 前日（5月10日）の18:00
```
[18:00 実行開始]
  ↓ check_schedule.py
  ↓ 明日（5月11日）をチェック
  ↓ 「燃やすごみ、かん」を検出
  ↓ alexa_notifier.py
  ↓ Alexa通知API送信
  ↓ Alexaデバイスに表示
  ✓ 「明日は燃やすごみ、かんの日です」
```

### 19:00, 20:00, 21:00, 22:00, 23:00
```
同じメッセージを繰り返し送信
（ユーザーが見落とさないようにするため）
```

---

## 🔐 セキュリティ機能

✅ **認証情報の保護**
- config.json はローカルのみに保存
- .gitignore に登録（リポジトリ提出時）
- GitHub等への誤上架防止

✅ **トークン管理**
- Refresh Token から Access Token を動的に生成
- トークン有効期限の自動チェック

✅ **ログ記録**
- 全ての操作を gomi_reminder.log に記録
- エラーや警告も記録

---

## 📊 データ構造

### schedule_cache.json 例

```json
{
  "year": 2026,
  "generated_at": "2026-05-09T22:59:34.071472",
  "schedule": {
    "燃やすごみ": [
      "2026-01-05",
      "2026-01-08",
      ...
      "2026-05-11",  ← 例: 5月11日（月）
      "2026-05-14",  ← 例: 5月14日（木）
      ...
    ],
    "燃やさないごみ": {
      "1": [28],     ← 1月28日
      "2": [25],     ← 2月25日
      ...
      "5": [25],     ← 5月25日
      ...
    },
    "かん": {
      "1": [16],     ← 1月16日
      ...
      "5": [11],     ← 5月11日
      ...
    },
    ...
  }
}
```

---

## 🧪 テストステータス

| モジュール | テスト状況 | ステータス |
|----------|---------|----------|
| extract_schedule.py | スケジュール抽出 | ✅ 成功 |
| check_schedule.py | 日程判定 | ✅ 成功 |
| alexa_notifier.py | API通信テスト | ⏳ 認証情報待機 |
| main.py | スケジューラー | ✅ 正常起動確認 |

---

## 🚀 展開手順

### 初回セットアップ

1. ✅ **extract_schedule.py 実行**
   ```bash
   python extract_schedule.py
   ```

2. ✅ **schedule_cache.json 確認**
   - 2026年全スケジュール生成確認

3. ⏳ **config.json 作成**
   - SETUP_ALEXA.md を参照
   - Device ID, Token等を取得

4. ⏳ **テスト実行**
   ```bash
   python main.py --mode test --once
   ```

5. ⏳ **Windows Task Scheduler 設定**
   - SETUP_TASK_SCHEDULER.md を参照
   - 自動起動スケジュール設定

### 定期メンテナンス

- **毎月1日**: スケジュール情報確認
- **トークン更新**: 有効期限確認（年1-2回）
- **ログ確認**: 定期的にエラーをチェック

---

## 📚 ドキュメント一覧

| ファイル | 対象ユーザー | 内容 |
|---------|----------|------|
| README.md | 全員 | 全般的な説明と機能紹介 |
| QUICKSTART.md | 初期設定者 | 5分で開始できるガイド |
| SETUP_ALEXA.md | Alexa設定者 | Amazon API設定詳細 |
| SETUP_TASK_SCHEDULER.md | Windows設定者 | 自動実行設定詳細 |
| SYSTEM_OVERVIEW.md | このファイル | システムアーキテクチャ |

---

## 🔧 技術仕様

### 依存ライブラリ

```
openpyxl>=3.10.0       # Excel解析
apscheduler>=3.10.0    # スケジューリング
requests>=2.31.0       # HTTP通信
python-dotenv>=1.0.0   # 環境変数管理
```

### 対応OS

- ✅ Windows 10 / 11
- ✅ Windows Server 2019 / 2022
- ⚠️ Linux/Mac (Task Scheduler代わりにcron等が必要)

### 対応Python

- ✅ Python 3.9 以上

### Alexa API仕様

- **API名**: Amazon Alexa Notifications API
- **エンドポイント**: `https://api.amazonalexa.com/v1/notifications/reminder-notifications`
- **認証方法**: OAuth 2.0 (Refresh Token → Access Token)
- **送信形式**: JSON (REST POST)

---

## 💡 今後の拡張可能性

- [ ] 複数地区対応 (シート番号を変更)
- [ ] メール通知機能 (Gmail API統合)
- [ ] Line通知機能 (Line Notify連携)
- [ ] スマートスピーカー対応 (Google Home等)
- [ ] Webダッシュボード (Flask等で実装)
- [ ] Alexa音声スキル（実際にAlexaで話す）

---

**🎉 システム実装完了！**

セットアップの詳細は各ドキュメントをご参照ください。

