# 論文投稿 Slack BOT

arXiv から特定のキーワード、特定の著者の論文を検索し、それを Slack に投稿する BOT です。

特徴としては、以下二つがあります。

## 論文を読む入り口の体験の向上

自分みたいな研究者でない人でも読みやすいように論文の abstract をもとにした要約や、なぜその論文は魅力的なのかをわかりやすく解説してもらうことで、論文を読んでみようかな思えるようにしています。

これだけでは論文の内容を把握することは難しいですが、ざっくりどのようなテーマなのかを把握したり、読もうかなと興味を持てるようにするということに焦点を当てています。

<img src="./static/bot_1.png" style="width:80%">

<img src="./static/bot_2.png" style="width:80%">

## 論文を読む体験の向上

いきなり英語の論文を読むのは難しいですよね。ということで私は以下二つのアプローチをとっています。

### 1. ChatPDF を使った対話形式で疑問を解消していく

[ChatPDF](https://www.chatpdf.com/) は論文の PDF を読み込ませると、その論文内容に基づいて会話ができるサービスです。

論文に書いてないことは、書いてないとある程度明記した上で解答をしてくれるので、比較的 hallucination のリスクは低いのかなと思っています（完全ではないと思いますが）。

この対話形式で論文の内容を把握していくと、この論文の起点となった課題感や新規性、今後の課題、手法の詳細についてなどを一通り質問しておくとざっくり内容が理解できます。また論文の内容を受けた自分の解釈が合っているかのすり合わせができたり、専門用語を噛み砕いて教えてもらったりできるので有用です。

Slack 投稿の下部に ChatPDF の URL と、論文 PDF の URL を載せています。この論文 PDF の URL をコピーして、ChatPDF の Find a URL に貼り付けるとすぐ会話ができるような体験となっています。

![output](https://user-images.githubusercontent.com/100386872/233752104-d2433b95-db50-46c4-99ee-58ce73a47303.gif)




### 2. Readable を使って PDF 翻訳をして読む

ステップ 1 が完了した頃には、論文の全体像や詳細なども少し掴めてきているはずです。このタイミングで [Readble の Chrome 拡張機能](https://chrome.google.com/webstore/detail/readable/pmhcplemclcflofgnjfhoilpkclnjnfh?hl=ja)を使って PDF を翻訳し、実際の原文を読み進めていきます。この [Readble](https://readable.jp/) は PDF のフォーマットを保った状態で翻訳してくれる神ツールです。使わない手はありません。

![output](https://user-images.githubusercontent.com/100386872/233751901-630cf40b-c9be-4f44-9fb8-33d5ffa74c9b.gif)

