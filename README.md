# 📚 論文投稿 Slack BOT

## 📕概要

**arXiv** から特定のキーワードや著者に関連する論文を定期的に検索し、Slack にわかりやすく投稿する BOT です。  
1時間ごとに指定したチャンネルへ最新論文の要約付きで投稿します。   

元（fork先）とのソースコードの変更点として以下3点を行います。
- **OpenAI**のAPIを用いたLLM（GPT-4o）を利用していましたが、ここでは**ollama**を用いたローカルLLM（llama）を用いて要約等の処理を行わせます。これによってAPI料金を気にすることなく、言語modelを制限されることなく利用することができます。
- 上記のツールの他にarXivの論文URLを貼ると、その論文の要約を投稿します。
- バージョン管理ツールを**Poetry**に変更します。

カスタマイズ
- LLMの実行についてollama, GPTを利用していますが、transformersのpiplineAPIを用いて実行することも可能です。その場合は自分で書き換えてください。

注意点（大事！！）
- **GPUを利用する前提の設計です。**(使用しないとLLMの処理速度が格段に長くなります。)
- **ollamaを使用する際はRAMの容量を必ず確認すること。**(ローカル環境にインストールしたモデルを呼び出すには少なくともモデルの容量を超えていないと呼び出すことができません。)
- API版の利用の際は料金に注意してください。読み込む論文のtoken数が決して少なくはない量ではあるので。
- LLMを利用しているので当然ですが、ハルシネーションがある前提で利用すること。


## 🚀 主な特徴

### 🧠 読みやすい要約・解説

- Abstract をもとに簡潔な要約を生成  
- 「なぜその論文が面白いのか？」を簡単に解説  
- 研究者でない人でも論文に興味を持てるようサポート

### 💬 ChatPDF を活用した対話的な読解

- ChatPDF を使い、論文内容について自由に質問可能  
- 投稿内に ChatPDF リンクを自動付与  
- 「何が新しいのか？」「手法のポイントは？」などを対話形式で理解

### 🌐 Readable による高精度な翻訳体験

- [Readable Chrome 拡張](https://chrome.google.com/webstore/detail/readable/pmhcplemclcflofgnjfhoilpkclnjnfh?hl=ja) に対応  
- PDF フォーマットを維持したまま翻訳可能  
- 日本語でスムーズに論文を読解

---

## 📷 使用イメージ

### Slack 投稿例  
![bot_1](./static/bot_1.png)

### ChatPDF との対話例  
![chatpdf_gif](https://user-images.githubusercontent.com/100386872/233752104-d2433b95-db50-46c4-99ee-58ce73a47303.gif)

---

## 🛠️ セットアップ手順

### 🔧 事前準備

以下の準備をあらかじめ行ってください（リンク参照）：

- Slack Bot の作成（`SLACK_BOT_TOKEN`, `SLACK_CHANNEL_ID` の取得）  
  👉 [Slack App の作成方法](https://www.pci-sol.com/business/service/product/blog/lets-make-slack-app/)
- [Railway](https://railway.app) のアカウント作成と CLI インストール  
  👉 [Railway CLI ドキュメント](https://docs.railway.app/develop/cli)

---

### 📦 インストール手順

Python 環境で以下のコマンドを実行してください：

```
pip install -r requirements.txt
```

推奨環境：

- Python 3.10.6  
- pip 23.0.1  
- railwayapp 3.0.21

---

### 🧪 ローカル環境での動作確認

`.env.example` を `.env` にコピーし、以下の環境変数を設定：

- `SLACK_BOT_TOKEN`：Slack Bot のトークン  
- `SLACK_CHANNEL`：投稿先チャンネルの ID  
- ~~`OPENAI_API_KEY`：OpenAI API キー~~ # OpenAIのAPIを使用しないので利用しない

設定後、以下のコマンドで起動できます：

```
make run
```

※ PC がスリープになると停止するため、常時稼働したい場合は次のデプロイ手順を参照してください。

---

## ☁️ Railway にデプロイする

まず Railway CLI をログイン＆リンク：

```
railway login  
railway link
```

次に以下を実行してデプロイ：

```
make deploy
```

---

## 🎉 Enjoy Your Paper Reading Life!

Slack で気軽に論文をチェックし、要約・翻訳・対話ですばやくキャッチアップしましょう！

---

## 📄 ライセンス

このプロジェクトは [MIT License](./LICENSE) のもとで公開されています。
