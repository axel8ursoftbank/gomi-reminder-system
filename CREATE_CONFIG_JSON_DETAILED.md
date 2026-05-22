# ⚙️ config.json を作成する - 超詳細ガイド

**このガイドは、config.json ファイルを作成する手順を、スクリーンショット付きで説明しています。**

---

## 前提条件

以下の4つの認証情報が揃っていることを確認してください：

```
✅ Device ID: amzn1.ask.device.ABC...
✅ Client ID: amzn1.application.6c8d...
✅ Client Secret: 8d1f2a9b...
✅ Refresh Token: Atzr|IwEBIE...
```

揃っていない場合：
- Device ID → GET_DEVICE_ID_DETAILED.md を参照
- その他 → GET_AMAZON_CREDENTIALS_DETAILED.md を参照

---

# 【ステップ1】config.json.template ファイルを確認

### 1-1. ファイルエクスプローラーを開く

1. **Windows キー + E を押す**

2. **ファイルエクスプローラーが開きます**

### 1-2. 正しいフォルダに移動

1. **以下のアドレスバーに入力**

   ```
   C:\Users\user\gomi_reminder_system
   ```

2. **Enter キーを押す**

3. **gomi_reminder_system フォルダが開きます**

### 1-3. config.json.template を確認

```
フォルダ内容:
┌────────────────────────────────┐
│ 📄 config.json.template ← これ │
│ 📄 schedule_cache.json         │
│ 📄 extract_schedule.py         │
│ 📄 check_schedule.py           │
│ 📄 alexa_notifier.py           │
│ 📄 main.py                     │
│ 📄 README.md                   │
│ ...                            │
└────────────────────────────────┘
```

✅ config.json.template が見えたら OK

---

# 【ステップ2】config.json.template をテンプレートとしてコピー

### 2-1. config.json.template を開く

1. **config.json.template を右クリック**

2. **「プログラムから開く」をクリック**

```
右クリックメニュー:
┌──────────────────────┐
│ 開く                 │
│ プログラムから開く → │
│ 送る                 │
│ ...                  │
└──────────────────────┘
```

### 2-2. メモ帳を選択

1. **「メモ帳」をクリック**

```
プログラム選択:
┌──────────────────────┐
│ メモ帳               │ ← クリック
│ Word                 │
│ その他プログラム...  │
└──────────────────────┘
```

2. **メモ帳でファイルが開きます**

### 2-3. ファイルの内容を確認

```
config.json.template の内容:

{
  "device_id": "YOUR_DEVICE_ID",
  "refresh_token": "YOUR_REFRESH_TOKEN",
  "client_id": "YOUR_CLIENT_ID",
  "client_secret": "YOUR_CLIENT_SECRET"
}
```

---

# 【ステップ3】4つの情報を入力

### 3-1. Device ID を入力

1. **「YOUR_DEVICE_ID」を選択**
   - YOUR_DEVICE_ID をダブルクリック

2. **以下を置き換え**

   例（入力前）：
   ```json
   {
     "device_id": "YOUR_DEVICE_ID",
   ```

   例（入力後）：
   ```json
   {
     "device_id": "amzn1.ask.device.ABC123...",
   ```

### 3-2. Refresh Token を入力

1. **「YOUR_REFRESH_TOKEN」を選択**

2. **以下を置き換え**

   ```json
   "refresh_token": "Atzr|IwEBIE...",
   ```

### 3-3. Client ID を入力

1. **「YOUR_CLIENT_ID」を選択**

2. **以下を置き換え**

   ```json
   "client_id": "amzn1.application.6c8d...",
   ```

### 3-4. Client Secret を入力

1. **「YOUR_CLIENT_SECRET」を選択**

2. **以下を置き換え**

   ```json
   "client_secret": "8d1f2a9b..."
   ```

### 3-5. 最終的な形

完成した config.json の例：

```json
{
  "device_id": "amzn1.ask.device.ABC123456789DEFGHIJKLMNOPQRST",
  "refresh_token": "Atzr|IwEBIHZkx2q3gxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "client_id": "amzn1.application.6c8d8f1a2b3c4d5e6f7g8h9i0j",
  "client_secret": "8d1f2a9b7c4e6f3h5i2j8k1l9m6n3o4p"
}
```

---

# 【ステップ4】ファイルを保存

### ⚠️ 重要: ファイル名と場所を間違えないでください

### 4-1. 「ファイル」メニューを開く

1. **メモ帳左上の「ファイル」をクリック**

```
メニュー:
┌──────────────────────┐
│ ファイル(F) ← クリック │
│ 編集(E)              │
│ 書式(O)              │
│ 表示(V)              │
│ ヘルプ(H)            │
└──────────────────────┘
```

### 4-2. 「名前を付けて保存」をクリック

```
ファイルメニュー:
┌──────────────────────┐
│ 新規作成             │
│ 開く                 │
│ 保存                 │
│ 名前を付けて保存 ← │
│ ページ設定           │
│ 印刷                 │
│ 終了                 │
└──────────────────────┘
```

### 4-3. 保存ダイアログが開きます

```
保存ダイアログ:
┌──────────────────────────────────┐
│ 名前を付けて保存                   │
│                                  │
│ ファイル名(N):                    │
│ [config.json.template________]  │ ← 編集
│                                  │
│ ファイルの種類(T):                │
│ [テキスト ファイル (*.txt)]       │
│                                  │
│ エンコード(E):                    │
│ [ANSI ▼]                        │
│                                  │
│ [保存]  [キャンセル]              │
└──────────────────────────────────┘
```

### 4-4. ファイル名を変更

1. **ファイル名の部分を全て選択**
   - 現在: `config.json.template`

2. **以下に変更**
   ```
   config.json
   ```
   
   （`.template` を削除）

### 4-5. ファイルの種類を設定

1. **「ファイルの種類」を確認**

2. **「テキスト ファイル (*.txt)」から変更が必要です**

3. **ドロップダウンをクリック**

```
ドロップダウンメニュー:
┌──────────────────────────────────┐
│ ▼ テキスト ファイル (*.txt)      │
│  すべてのファイル (*.*)          │ ← 選択
│  Python ファイル (*.py)          │
│  JSON ファイル (*.json) ← これが│
│  ...                             │
└──────────────────────────────────┘
```

⚠️ **問題: JSON ファイルが見当たらない場合**

その場合は「すべてのファイル (*.*)」を選択してください

### 4-6. エンコードを変更

1. **「エンコード(E)」を確認**

2. **現在: ANSI になっていないか確認**

3. **ドロップダウンをクリック**

```
エンコーディングメニュー:
┌──────────────────────────────────┐
│ ▼ ANSI                          │
│  Unicode                        │
│  Unicode (Big-endian)           │
│  UTF-8 ← 選択                   │
│  ...                             │
└──────────────────────────────────┘
```

**必ず「UTF-8」を選択してください**

### 4-7. 保存先を確認

1. **ダイアログ上部を確認**

2. **保存先が以下になっているか確認**
   ```
   C:\Users\user\gomi_reminder_system
   ```

   異なる場合：
   - アドレスバーをクリック
   - 上記のパスに変更
   - Enter キー

### 4-8. 最終確認

以下が正しいか確認：

```
ファイル名: config.json ← .template は不要
ファイルの種類: すべてのファイル or JSON ファイル
エンコード: UTF-8
保存先: C:\Users\user\gomi_reminder_system
```

### 4-9. 「保存」をクリック

1. **「保存」ボタンをクリック**

2. **ダイアログが閉じます** ✅

---

# 【ステップ5】作成した config.json を確認

### 5-1. ファイルエクスプローラーを確認

1. **ファイルエクスプローラーを見る**

2. **新しく「config.json」が見えているか確認**

```
フォルダ内容（新）:
┌────────────────────────────────┐
│ 📄 config.json ← 新規作成      │
│ 📄 config.json.template        │
│ 📄 schedule_cache.json         │
│ 📄 extract_schedule.py         │
│ ...                            │
└────────────────────────────────┘
```

### 5-2. config.json を開いて確認

1. **config.json をメモ帳で開く**

2. **内容を確認**

   ```json
   {
     "device_id": "amzn1.ask.device.ABC...",
     "refresh_token": "Atzr|IwEBIE...",
     "client_id": "amzn1.application.6c8d...",
     "client_secret": "8d1f2a9b..."
   }
   ```

3. **4つのキーと値がすべて入っているか確認**

✅ すべて正しければ完成です！

---

# ✨ config.json 作成完了！

これで認証ファイルが完成しました。

**次のステップ:**

1. **テスト実行**
   ```bash
   python main.py --mode test --once
   ```

2. **Windows Task Scheduler で自動実行設定**
   - DETAILED_SETUP_GUIDE.md「ステップ10」を参照

3. **本番運用開始**

---

## 🆘 トラブルシューティング

### 問題: config.json.template のままになっている

**原因**: ファイル名の変更に失敗

**解決方法**:
1. config.json.template を削除
2. このガイドのステップ4を再実行

### 問題: エンコードが ANSI になっていた

**原因**: ステップ4-6で UTF-8 を選択しなかった

**解決方法**:
1. config.json をメモ帳で開く
2. 「ファイル」→「名前を付けて保存」
3. エンコードを UTF-8 に変更
4. 保存

### 問題: JSON の形式が間違っている

**特徴:**
- 開き括弧と閉じ括弧が対応していない
- カンマが足りない
- ダブルクォートが正しくない

**確認方法:**
1. メモ帳で開く
2. 以下の形を確認：
   ```json
   {
     "キー1": "値1",
     "キー2": "値2",
     "キー3": "値3",
     "キー4": "値4"
   }
   ```

3. 余分なスペースや改行がないか確認

---

## ✅ 完了チェックリスト

- [ ] config.json が作成されている
- [ ] ファイル名が「config.json」（template なし）
- [ ] エンコードが UTF-8
- [ ] 4つの認証情報がすべて入っている
- [ ] JSON の形式が正しい
- [ ] 保存先が C:\Users\user\gomi_reminder_system

すべてチェックできたら、次のステップに進んでください！

---

**これで導入準備が完了です！ 🎉**

次は **テスト実行** → **自動実行設定** の順で進めます。

