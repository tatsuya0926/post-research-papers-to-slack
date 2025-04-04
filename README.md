# 📚 論文投稿 Slack BOT

## 📕概要

**arXiv** から特定のキーワードや著者に関連する論文を定期的に検索し、Slack にわかりやすく投稿する BOT です。
一定時間ごとに指定したチャンネルへ最新論文の要約付きで投稿します。

元（fork先）とのソースコードの変更点として以下3点を行います。
- **GPT-4oをollamaによるローカルLLMに変更:** **OpenAI**のAPIを用いたLLM（GPT-4o）を利用していましたが、ここでは**ollama**を用いたローカルLLM（llama）を用いて要約等の処理を行わせます。これによってAPI料金を気にすることなく、言語modelを制限されることなく利用することができます。
- **自動化ツールをRailwayからcronに変更:** PaaSとしてRailwayを使用しているが、使用した分料金がかかってしまうのでこの自動化ツールを**cron**(Windowsならタスクスケジューラ)で置き換えます。
- **バージョン管理ツールとしてPoetryを利用:** pyenv等で管理していたパッケージを管理のしやすさを理由にバージョン管理ツールを**Poetry**に変更します。

カスタマイズ性について
- LLMの実行についてollama, ~~GPT~~を利用していますが、transformersのpiplineAPIを用いて実行することも可能です。その場合は自分で書き換えてください。
- 自動化ツールとして使えればなんでもいいのでcronに拘らず、RailwayでもGithub Actionsでもなんでもいいです。
- 現状論文検索APIをArXiv APIで行なっているのでArXivに登録されていない論文は検索できません。その場合別の論文検索APIを利用してください。

**注意点（大事！！）**
- **GPUを利用する前提の設計です。**(使用しないとLLMの処理速度が格段に長くなります。)
- **ollamaを使用する際はRAMの容量を必ず確認すること。**(ローカル環境にインストールしたモデルを呼び出すには少なくともモデルの容量を超えていないと呼び出すことができません。)
- API版の利用の際は料金に注意してください。読み込む論文のtoken数が決して少なくはない量ではあるので。
- LLMを利用しているので当然ですが、ハルシネーション前提で利用してください。


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
- ollama のインストールとLLMのダウンロード  
  👉 [ollamaの導入方法](https://zenn.dev/hellorusk/books/e56548029b391f/viewer/ollama)

### 📦 インストール手順

推奨環境：

- Python 3.10.6  

Poetryがインストールされている状態で以下のコマンドを実行してください：
```bash
poetry init
poetry install
```

一応テストとして使用するので、Python環境（または仮想環境）をJupyter NotebookやJupyter Labで使えるカーネルとして登録してください：
```bash
poetry shell
python -m ipykernel install --user --name=post-research-papers-to-slack-py3.10
```

もし`poetry shell`が効かない場合、Poetryのshellプラグインをインストールしたのち上記を実行してください：
```bash
poetry self add poetry-plugin-shell
```

次に、ollamaがインストールされている状態かつ起動している状態で以下のコマンドを実行してください：
```bash
ollama run schroneko/gemma-2-2b-jpn-it
```
なお使用しているLLMはgemma 2 2Bを日本語でfine tuningしたもので英語・日本語に対応しているものを使用しています。特段これを使用しなければならないわけではないので、以下のURLから検索して選ぶことが可能です。[ollama対応モデル一覧](https://ollama.com/search)


### 🧪 ローカル環境での動作確認

`.env.example` を `.env` にコピーし、以下の環境変数を設定：

- `SLACK_BOT_TOKEN`：Slack Bot のトークン  
- `SLACK_CHANNEL`：投稿先チャンネルの ID  
- ~~`OPENAI_API_KEY`：OpenAI API キー~~ # OpenAIのAPIを使用しないので利用しない。


## 🎉 Enjoy Your Paper Reading Life!

Slack で気軽に論文をチェックし、要約・翻訳・対話ですばやくキャッチアップしましょう！


## 📄 ライセンス

このプロジェクトは [MIT License](./LICENSE) のもとで公開されています。
