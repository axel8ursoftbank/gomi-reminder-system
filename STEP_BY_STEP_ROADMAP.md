# 🗺️ ゴミ出し日程Alexa通知システム - 完全ロードマップ

**これは最もシンプルで、初心者向けの導入パスです。**
**このロードマップに従ってください。**

---

## 📌 全体の流れ

```
【準備】(PC)
  ↓
【認証情報取得】(スマートフォン + PC)
  ↓
【ファイル作成】(PC)
  ↓
【テスト】(PC)
  ↓
【自動実行設定】(PC)
  ↓
✅ 完成！
```

所要時間：**約1時間**

---

# 🎬 ステップごとの詳細ロードマップ

## 【準備】PC での最初の設定（5分）

### ✅ ステップ0: パッケージのインストール

**実行:**
```bash
cd C:\Users\user\gomi_reminder_system
pip install -r requirements.txt
python extract_schedule.py
```

**確認:**
- schedule_cache.json が生成されたか
- 「スケジュールを保存しました」と表示されたか

**参考ドキュメント:**
- DETAILED_SETUP_GUIDE.md「ステップ1-4」

---

## 【認証情報取得 - パート1】スマートフォン（5分）

### ✅ ステップ1: Device ID を取得

**所要時間:** 5分

**手順:**
1. スマートフォンで Alexa App を開く
2. メニューから「デバイス」を選択
3. 通知を受け取るデバイスをタップ
4. 「Device ID:」を見つけてコピー

**参考ドキュメント:**
- 📱 **GET_DEVICE_ID_DETAILED.md** ← 詳しくはこちら

**結果:**
```
Device ID をメモに保存
amzn1.ask.device.ABC123...
```

---

## 【認証情報取得 - パート2】PC のブラウザ（20分）

### ✅ ステップ2: Amazon Developer Console で設定

**所要時間:** 20分

**内容:**
1. スキルを作成（Gomi Reminder）
2. Security Profile を作成
3. Client ID をコピー
4. Client Secret をコピー
5. Web Settings を設定
6. Authorization Code を取得
7. Refresh Token を取得

**参考ドキュメント:**
- 🔐 **GET_AMAZON_CREDENTIALS_DETAILED.md** ← 詳しくはこちら

**結果:**
```
以下の4つの認証情報を取得
✓ Device ID
✓ Client ID
✓ Client Secret
✓ Refresh Token
```

---

## 【ファイル作成】config.json を作成（5分）

### ✅ ステップ3: config.json を作成

**所要時間:** 5分

**内容:**
1. config.json.template をテンプレートとして使用
2. 4つの認証情報を入力
3. ファイルを保存

**参考ドキュメント:**
- ⚙️ **CREATE_CONFIG_JSON_DETAILED.md** ← 詳しくはこちら

**結果:**
```
C:\Users\user\gomi_reminder_system\config.json
が作成される
```

---

## 【テスト】動作確認（5分）

### ✅ ステップ4: テスト実行

**所要時間:** 5分

**コマンド:**
```bash
cd C:\Users\user\gomi_reminder_system
python main.py --mode test --once
```

**確認:**
- コマンドプロンプトに「テスト実行完了」と表示される
- Alexaデバイスの画面に通知が表示される

**参考ドキュメント:**
- DETAILED_SETUP_GUIDE.md「ステップ9」

**結果:**
```
✅ Alexaデバイスに通知が表示される
✅ システムが正常に動作している
```

---

## 【自動実行設定】Windows Task Scheduler（10分）

### ✅ ステップ5: Windows Task Scheduler で自動実行設定

**所要時間:** 10分

**手順:**
1. Windows キー + R → tasksched.msc → Enter
2. 「基本タスクの作成」をクリック
3. タスク名: Gomi Reminder System
4. トリガー: 毎日 08:00
5. 操作: C:\Users\user\gomi_reminder_system\start_gomi_reminder.bat を実行
6. 完了

**参考ドキュメント:**
- DETAILED_SETUP_GUIDE.md「ステップ10」

**結果:**
```
✅ 毎日朝8:00にシステムが自動起動
✅ 毎日18:00-23:00に自動チェック実行
```

---

## ✨ 完成！🎉

```
これ以降、以下が自動実行されます：

毎日 08:00 ↓ システム起動
毎日 18:00 ↓ 明日のゴミをチェック（あれば通知）
毎日 19:00 ↓ 明日のゴミをチェック（あれば通知）
毎日 20:00 ↓ 明日のゴミをチェック（あれば通知）
毎日 21:00 ↓ 明日のゴミをチェック（あれば通知）
毎日 22:00 ↓ 明日のゴミをチェック（あれば通知）
毎日 23:00 ↓ 明日のゴミをチェック（あれば通知）

✅ Alexa 画面に「明日は○○ゴミの日です」と表示される
```

---

# 📚 ドキュメント一覧

## 【詳細ガイド】このロードマップと一緒に使用

| ステップ | ドキュメント | 内容 |
|---------|----------|------|
| ステップ0 | DETAILED_SETUP_GUIDE.md | パッケージのインストール |
| ステップ1 | **GET_DEVICE_ID_DETAILED.md** ⭐ | Device IDの詳細取得方法 |
| ステップ2 | **GET_AMAZON_CREDENTIALS_DETAILED.md** ⭐ | Amazon認証情報の詳細取得方法 |
| ステップ3 | **CREATE_CONFIG_JSON_DETAILED.md** ⭐ | config.jsonの詳細作成方法 |
| ステップ4 | DETAILED_SETUP_GUIDE.md「ステップ9」 | テスト実行方法 |
| ステップ5 | DETAILED_SETUP_GUIDE.md「ステップ10」 | 自動実行設定方法 |

⭐ = 特に詳しく説明されています

---

# 🎯 今すぐ始める

## 推奨される順序

```
1️⃣ ステップ0: パッケージインストール
   → DETAILED_SETUP_GUIDE.md を参照
   → コマンド実行（5分）

2️⃣ ステップ1: Device ID 取得
   → GET_DEVICE_ID_DETAILED.md を参照
   → スマートフォンで操作（5分）

3️⃣ ステップ2: Amazon 認証情報取得
   → GET_AMAZON_CREDENTIALS_DETAILED.md を参照
   → ブラウザで操作（20分）

4️⃣ ステップ3: config.json 作成
   → CREATE_CONFIG_JSON_DETAILED.md を参照
   → テキストエディタで作成（5分）

5️⃣ ステップ4: テスト実行
   → DETAILED_SETUP_GUIDE.md「ステップ9」を参照
   → コマンド実行（5分）

6️⃣ ステップ5: 自動実行設定
   → DETAILED_SETUP_GUIDE.md「ステップ10」を参照
   → Task Scheduler で設定（10分）
```

---

# ✅ チェックリスト

完成時のチェックリスト：

```
【ステップ0】パッケージインストール
□ pip install -r requirements.txt が完了
□ python extract_schedule.py が完了
□ schedule_cache.json が生成された

【ステップ1】Device ID 取得
□ Alexa App で Device ID を確認
□ Device ID をコピーしてメモに保存

【ステップ2】Amazon 認証情報取得
□ Amazon Developer Console でスキル作成
□ Security Profile を作成
□ Client ID をコピー
□ Client Secret をコピー
□ Authorization Code を取得
□ Refresh Token を取得
□ メモに4つの情報をすべて保存

【ステップ3】config.json 作成
□ config.json.template をテンプレートとして使用
□ 4つの認証情報を入力
□ ファイルを保存
□ config.json が C:\Users\user\gomi_reminder_system に存在

【ステップ4】テスト実行
□ python main.py --mode test --once を実行
□ Alexa デバイスに通知が表示される

【ステップ5】自動実行設定
□ Windows Task Scheduler を開く
□ 基本タスク「Gomi Reminder System」を作成
□ トリガーは「毎日 08:00」
□ 操作は「start_gomi_reminder.bat」を実行

【完成】
□ すべてのチェックボックスにチェック ✓
□ Alexa に通知が届く ✓
□ 自動実行されている ✓
```

---

# 🆘 困ったときの対応

## Q: どれから始めたらいい？

A: **このロードマップの順に進めてください**

1. ステップ0 → ステップ1 → ステップ2 → ステップ3 → ステップ4 → ステップ5

## Q: Device ID がわからない

A: **GET_DEVICE_ID_DETAILED.md を最初から最後まで読んでください**

スマートフォン別に詳しく説明されています

## Q: Amazon認証情報の取得が複雑

A: **GET_AMAZON_CREDENTIALS_DETAILED.md を参照**

7つのステップに分けて説明されています

## Q: config.json の作成がわからない

A: **CREATE_CONFIG_JSON_DETAILED.md を参照**

メモ帳での入力から保存まで詳しく説明されています

## Q: テスト実行で エラーが出た

A: **DETAILED_SETUP_GUIDE.md「トラブルシューティング」を参照**

よくあるエラーの解決方法が書いてあります

---

# 📞 サポート

各ステップのドキュメントには詳しい説明とトラブルシューティングが付いています。

**困ったときの流れ:**

```
ステップXで困った
  ↓
該当するドキュメントの「トラブルシューティング」を読む
  ↓
解決しない場合
  ↓
別のドキュメントを参照
  ↓
質問する
```

---

# 🚀 準備はいいですか？

このロードマップに従って、一つずつ進めてください。

**最初のステップ:**
```
ステップ0 を実行
参考ドキュメント: DETAILED_SETUP_GUIDE.md「ステップ1-4」
```

**頑張ってください！**

もし不明な点があれば、いつでもお気軽にお尋ねください！ 💪

