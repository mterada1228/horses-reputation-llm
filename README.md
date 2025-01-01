# horses-reputation-llm
出走馬の評判を検索して LLM が回答してくれるアプリケーション

## 開発環境のセットアップ（初回）

1. python の仮想環境を作成する

```console
❯ python3 -m venv env
```

2. 環境変数を設定する

```console
❯ cp .env.example .env
```

.env を編集して OPEN_AI_API_KEY に発行した API KEY を設定

3. 必要なパッケージをインストールする

```console
❯ pip install -r requirements.txt
```

##　開発環境の立ち上げ

1. 仮想環境をアクティベートする

```console
❯ source env/bin/activate
```

## 開発環境の立ち下げ

```console
❯ deactivate
```