# horses-reputation-llm

出走馬の評判を検索して LLM が回答してくれるアプリケーション

## 開発環境のセットアップ（初回 or 開発環境の立ち上げ前に必要に応じて）

### API

1. python の仮想環境を作成する

```console
❯ python3 -m venv env
```

2. 必要なパッケージをインストールする

```console
❯ pip install -r requirements.txt

❯ cd llm-api
❯ pip install -e .
```

3. 環境変数を設定する

```console
❯ cp .env.example .env
```

.env を編集して OPEN_AI_API_KEY に発行した API KEY を設定

### フロントエンド

1. node のインストール

```console
❯ nodenv install
```

2. pnpm を有効化

```console
❯ corepack enable
❯ nodenv rehash
```

3. 依存ライブラリをインストールする

```console
❯ pnpm install
```

##　開発環境の立ち上げ

1. 仮想環境をアクティベートする

```console
❯ source env/bin/activate
```

2. アプリを立ち上げる

```console
❯ pnpm run dev
```

## 各種コマンド

1. netkeiba からデータを RAG に追加する

```console
❯ python add_document.py <取得したいニュース一覧のページナンバーの開始地点> <取得したいニュース一覧のページナンバーの終了地点>
```

## 開発環境の立ち下げ

```console
❯ deactivate
```
