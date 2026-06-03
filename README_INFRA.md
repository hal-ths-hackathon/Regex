# Infra: 起動手順

1. ルートに `.env` を作成し、`.env.example` を参考に値を設定します。

2. コンテナ起動:

```bash
docker compose up -d --build
```

3. バックエンド API ドキュメント確認:

ブラウザで `http://localhost:8000/docs` を開いて Swagger UI を確認してください。

4. PostgreSQL に接続する場合（例）:

```bash
psql "postgresql://postgres:postgres@localhost:5432/regex"
```
