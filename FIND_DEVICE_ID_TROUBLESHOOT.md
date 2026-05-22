# 🔍 Device ID が見つからない時の対処法

**シリアル番号やMACアドレスは見つかったけど、Device IDが見つからない場合の対処方法です。**

---

## 📱 よくある誤解

### ❌ これらは Device ID ではありません

```
シリアル番号:
G8E6Q2ABC1234

MACアドレス:
00:1A:2B:3C:4D:5E

WiFi情報:
Alexa_Home_2.4GHz
```

### ✅ これが Device ID です

```
amzn1.ask.device.ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890ABCD
```

**特徴:**
- 「amzn1.ask.device.」で始まる
- その後ろに50文字以上のランダムな英数字
- 非常に長い文字列

---

## 🔎 Device ID の見つけ方（複数の方法）

### 方法1️⃣: Alexa App で探す（最も簡単）

#### iPhone の場合

**ステップA: デバイス詳細ページまで到達**

1. Alexa App を開く
2. 左上の「≡」をタップ
3. 「デバイス」をタップ
4. デバイスをタップ（例：リビングのEcho）

**ここでシリアル番号やMACアドレスを見ているはずです**

**ステップB: 下にスクロール**

```
現在見ている場所:
┌───────────────────────────┐
│ リビングのEcho             │
│                           │
│ デバイス名: ...           │
│ シリアル番号: G8E6Q2...  │
│ MACアドレス: 00:1A...    │
│ WiFi: Alexa_Home...      │
│   ↑ ここまで見えている
│
│ スクロール↓
│
│ ソフトウェアバージョン     │
│ Device ID: amzn1...  ← これ！
│                           │
└───────────────────────────┘
```

**重要: 画面を下にスワイプしてください**

1. 現在見えている画面から**下にスワイプ**
2. さらに下にスクロール
3. 「Device ID:」を見つけてください

#### Android の場合

同じく下にスクロールしてください

1. Alexa App を開く
2. 左上の「≡」をタップ
3. 「デバイス」をタップ
4. デバイスをタップ
5. **下にスクロール** ← 重要！
6. 「Device ID:」を見つけてください

---

### 方法2️⃣: Web Console から探す

**Alexa App で見つからない場合はこれを試してください**

#### ステップ1: Amazon Alexa ウェブサイトにアクセス

1. ブラウザを開く
2. 以下にアクセス

```
https://alexa.amazon.co.jp
```

#### ステップ2: ログイン

1. Amazonアカウントでログイン
2. 左側のメニューから「デバイス」を選択

#### ステップ3: デバイスを選択

1. デバイス一覧が表示されます
2. 対象のデバイス（例：Echo）をクリック

#### ステップ4: デバイスの詳細を表示

1. デバイス情報が表示されます
2. 「デバイス情報」セクションを探す
3. 「Device ID」を見つけてください

```
デバイスの詳細ページ:
┌─────────────────────────┐
│ リビングのEcho          │
│                         │
│ 【デバイス情報】        │
│                         │
│ デバイス名              │
│ リビングのEcho          │
│                         │
│ Device ID               │
│ amzn1.ask.device.ABC... │ ← これです！
│                         │
│ シリアル番号            │
│ G8E6Q2ABC1234          │
│                         │
│ ソフトウェアバージョン  │
│ 123.456                │
│                         │
└─────────────────────────┘
```

---

### 方法3️⃣: AWS マネジメントコンソールから探す（上級）

**Alexa App と Web でも見つからない場合**

#### ステップ1: AWS コンソールにアクセス

```
https://console.aws.amazon.com/
```

#### ステップ2: Systems Manager を検索

1. 上部の検索ボックスに「Systems Manager」と入力
2. 検索結果から「Systems Manager」をクリック

#### ステップ3: Parameter Store を開く

1. 左側メニューから「Parameter Store」を選択
2. 検索ボックスに「alexa」と入力
3. 検索結果に Device ID が表示されます

---

## 🆘 Device ID が本当に見つからない場合

### 原因の確認

**Q: シリアル番号は見つかったが、Device IDは見つからない？**

**A: 以下を確認してください**

#### 確認1: ページ全体をスクロール

```
Alexa App:
─────────────────────
│ デバイス情報        │ ← 最初ここが見える
│ ・デバイス名        │
│ ・シリアル番号      │
│ ・MACアドレス       │
│ ・WiFi              │
│                     │
│ 下にスクロール↓    │
│                     │
│ ・ソフトウェア      │
│ ・Device ID ← ここ! │
│ ・その他の情報      │
─────────────────────
```

**→ 絶対にスクロール必須です**

#### 確認2: 別のデバイスがないか

複数の Echo がある場合：

```
デバイス一覧
┌─────────────┐
│ Echo 1      │ ← Device ID: amzn1.xxx
│ Echo 2      │ ← Device ID: amzn1.yyy
│ Echo Show 1 │ ← Device ID: amzn1.zzz
└─────────────┘
```

別のデバイスをタップすると、別の Device ID が見つかるかもしれません

#### 確認3: Alexa App が最新版か

古いバージョンの Alexa App では Device ID が表示されない場合があります

```
App Store（iPhone）または Google Play（Android）で
「Amazon Alexa」を検索して「アップデート」をクリック
```

#### 確認4: 別のブラウザで Web Console を試す

Alexa App が古い場合、Web Console ならDevice IDが見つかります

```
https://alexa.amazon.co.jp
```

---

## ✅ Device ID が見つかる場所（まとめ）

### 優先順位

1. **Alexa App が見つからない場合**
   → Web Console で探す

2. **Web Console でも見つからない場合**
   → AWS コンソール（Parameter Store）で探す

3. **すべてで見つからない場合**
   → Alexa App を最新版に更新してから再度試す

---

## 🎯 今すぐやることチェックリスト

### iPhone ユーザー

- [ ] Alexa App を開く
- [ ] 左上「≡」→「デバイス」をタップ
- [ ] デバイスをタップ
- [ ] **下にスワイプしてスクロール**
- [ ] 「Device ID: amzn1.ask.device.」を探す
- [ ] コピー

### Android ユーザー

- [ ] Alexa App を開く
- [ ] 左上「≡」をタップ
- [ ] 「デバイス」をタップ
- [ ] デバイスをタップ
- [ ] **下にスクロール**
- [ ] 「Device ID: amzn1.ask.device.」を探す
- [ ] コピー

### Web Console から探す

- [ ] https://alexa.amazon.co.jp にアクセス
- [ ] ログイン
- [ ] 「デバイス」を選択
- [ ] デバイスをクリック
- [ ] 「Device ID:」を探す
- [ ] コピー

---

## 🚨 最後の手段：Amazon サポートに問い合わせ

もしすべての方法で見つからない場合：

```
Amazon カスタマーサービス
https://www.amazon.co.jp/gp/help/customer/contact-us

問い合わせ内容:
「Alexa デバイスの Device ID が見つかりません」
```

---

## 💡 ヒント

**Device ID はこんな感じです：**

```
良い例:
✅ amzn1.ask.device.ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890AB

悪い例:
❌ G8E6Q2ABC1234 (これはシリアル番号)
❌ 00:1A:2B:3C:4D:5E (これはMACアドレス)
❌ Alexa_Home_2.4GHz (これはWiFi名)
```

**見つけるコツ:**
- 必ず「amzn1.ask.device.」で始まっています
- 非常に長い文字列です（50文字以上）
- ページの下の方にあります

---

## ✨ 見つかったら

Device ID をコピーしたら：

1. メモ帳に貼り付け
2. 次は「Client ID/Secret」を取得
3. 参照: GET_AMAZON_CREDENTIALS_DETAILED.md

---

**最も重要: Alexa App でスクロールして、ページの下を確認してください！**

