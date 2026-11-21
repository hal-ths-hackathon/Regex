# Infra: 起動手順

1. ルートに `.env` を作成し、`.env.example` を参考に値（特にパスワード）を設定します。

```bash
cp .env.example .env
```

2. コンテナ起動（開発用。`docker-compose.override.yml` が自動で読み込まれ、ポートは localhost にのみ公開されます）:

```bash
docker compose up -d --build
```

3. バックエンド API ドキュメント確認（開発環境のみ有効）:

ブラウザで `http://localhost:8090/docs` を開いて Swagger UI を確認してください。

4. PostgreSQL に接続する場合（例。ユーザー名・パスワードは `.env` の値を使用）:

```bash
psql "postgresql://<POSTGRES_USER>:<POSTGRES_PASSWORD>@localhost:5439/<POSTGRES_DB>"
```

本番環境の手順は `docs/deployment.md` を参照してください。
