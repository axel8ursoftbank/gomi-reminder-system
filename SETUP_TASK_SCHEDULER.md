# Windows Task Scheduler セットアップガイド

このガイドでは、ゴミ出し日程Alexa通知システムを Windows Task Scheduler で自動起動する方法を説明します。

---

## ステップ1: requirements.txt のインストール

まず、必要なPythonパッケージをインストールします。

1. コマンドプロンプトを開く
2. 以下を実行:

```bash
cd C:\Users\user\gomi_reminder_system
pip install -r requirements.txt
```

**requirements.txt の内容:**

```
openpyxl>=3.10.0
apscheduler>=3.10.0
requests>=2.31.0
python-dotenv>=1.0.0
```

---

## ステップ2: バッチファイルの作成

1. `C:\Users\user\gomi_reminder_system` ディレクトリを開く

2. テキストエディタ（メモ帳）で以下を入力:

```batch
@echo off
REM ゴミ出し日程Alexa通知システム 自動起動スクリプト

cd /d C:\Users\user\gomi_reminder_system

REM Pythonが見つからない場合のエラーハンドリング
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo エラー: Pythonがインストールされていないか、PATHに登録されていません
    pause
    exit /b 1
)

REM メインプログラムを実行（real モードで実際の通知を送信）
python main.py --mode real

REM エラーの場合
if %errorlevel% neq 0 (
    echo ゴミ出し日程Alexa通知システムでエラーが発生しました
    timeout /t 5
)
```

3. 「ファイル → 名前をつけて保存」で `start_gomi_reminder.bat` として保存

4. 文字コード: **UTF-8 (BOM あり)** を選択

---

## ステップ3: Windows Task Scheduler での自動実行設定

### 方法1: GUI（推奨）

1. **タスクスケジューラーを起動:**
   - キーボード: `Win + R` → `taskschd.msc` → Enter
   - または: 「スタート」→ 「Windows 管理ツール」→ 「タスクスケジューラー」

2. **左パネルから「タスク スケジューラー ライブラリ」を選択**

3. **右パネルで「基本タスクの作成」をクリック**

4. **名前と説明を入力:**
   - 名前: `Gomi Reminder System`
   - 説明: `ゴミ出し日程Alexa通知システム`
   - 「次へ」

5. **トリガーを設定:**
   - 「毎日」を選択
   - 開始日時: 今日の日付
   - 時刻: `08:00:00`（毎日朝8時に起動）
   - 「次へ」

6. **操作を設定:**
   - 「プログラムの開始」を選択
   - プログラム/スクリプト: `C:\Users\user\gomi_reminder_system\start_gomi_reminder.bat`
   - 「次へ」

7. **条件を設定（任意）:**
   - 「コンピューターがAC電源で動作している場合のみ実行」: チェック
   - 「次へ」

8. **設定を確認:**
   - 内容を確認して「完了」をクリック

---

### 方法2: PowerShell（コマンドライン）

管理者権限でPowerShellを開いて実行:

```powershell
$taskName = "Gomi Reminder System"
$taskDescription = "ゴミ出し日程Alexa通知システム"
$scriptPath = "C:\Users\user\gomi_reminder_system\start_gomi_reminder.bat"
$action = New-ScheduledTaskAction -Execute $scriptPath
$trigger = New-ScheduledTaskTrigger -Daily -At 08:00AM
$principal = New-ScheduledTaskPrincipal -UserId "$env:USERDOMAIN\$env:USERNAME" -RunLevel Highest

Register-ScheduledTask `
    -TaskName $taskName `
    -Description $taskDescription `
    -Action $action `
    -Trigger $trigger `
    -Principal $principal `
    -Force
```

---

## ステップ4: 自動起動テスト

1. **タスクスケジューラーで確認:**
   - タスク一覧から「Gomi Reminder System」を探す
   - 右クリック → 「実行」

2. **動作確認:**
   - コマンドプロンプトウィンドウが起動
   - ログファイル（`gomi_reminder.log`）に実行結果が記録される

3. **ログ確認:**
   ```bash
   type gomi_reminder.log
   ```

---

## ステップ5: スケジューラーオプションの調整

### より頻繁に起動させたい場合:

1. タスクスケジューラーでタスクを右クリック → 「プロパティ」

2. 「トリガー」タブで設定を編集:
   - 「毎日」の時刻を変更（例: 朝6時に変更）
   - または複数のトリガーを追加（朝と夕方など）

### PCが常時起動していない場合:

- タスク トリガーを「コンピューター起動時」に設定
- または「ユーザーログイン時」に設定

---

## トラブルシューティング

### タスクが実行されない

1. **実行権限を確認:**
   ```bash
   whoami
   ```
   
2. **バッチファイルの実行テスト:**
   - `start_gomi_reminder.bat` を直接実行して動作確認

3. **ログファイルの確認:**
   ```bash
   tail -f gomi_reminder.log
   ```

### Pythonスクリプトが起動しない

1. **Pythonパスの確認:**
   ```bash
   where python
   ```

2. **フルパスでの実行に変更:**
   - バッチファイルの `python` を `C:\Users\user\AppData\Local\Programs\Python\Python311\python.exe` に置き換え

### 通知が送信されない

1. **config.json を確認:**
   - ファイルが存在するか
   - 認証情報が正しいか

2. **ネットワーク接続を確認:**
   - インターネット接続が正常か
   - ファイアウォールで Alexa API への通信をブロックしていないか

---

## ログモニタリング

システムの動作状況をモニタリングするには:

```bash
# PowerShellでリアルタイムログ監視
Get-Content -Path C:\Users\user\gomi_reminder_system\gomi_reminder.log -Wait -Tail 10

# または
tail -f gomi_reminder.log  # WSL/Git Bash
```

---

## 自動タスクの無効化

タスクを一時的に停止する場合:

1. タスクスケジューラーで「Gomi Reminder System」を選択
2. 右クリック → 「無効化」

---

## 参考

- [Windows Task Scheduler Documentation](https://docs.microsoft.com/en-us/windows/win32/taskschd/task-scheduler-start-page)
- [PowerShell ScheduledTask Commands](https://docs.microsoft.com/en-us/powershell/module/scheduledtasks/)

