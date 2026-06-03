# アーキテクチャと開発ルール (Architecture)

今週末での最速リリースと、今後の拡張（ランキング等）を両立するため、以下の堅牢な初期基盤を構築する。

## 1. ディレクトリ構成（モノレポ想定）
* `/frontend`: React (TS)
* `/backend`: FastAPI (Python)
* `docker-compose.yml`

## 2. 必須の初期設定（落とし穴対策）
* **環境変数の管理**:
  * フロントエンドとバックエンドで `.env` を分離。
  * バックエンドのDB接続情報等は `pydantic-settings` などを用いて型安全に管理する。
* **CORS設定**:
  * FastAPIの `CORSMiddleware` を使用し、フロントエンドのオリジン（開発時は `http://localhost:3000` など）からのリクエストを厳格に許可する。
* **DBの永続化とマイグレーション**:
  * **Docker Volume**: PostgreSQLのデータは `volumes` をマウントし、コンテナ再起動時のデータ消失を防ぐ。
  * **マイグレーション**: `Alembic` を導入。初期化時に「アーケードランキング用の `scores` テーブル」を作成する。
* **静的解析（Lint/Format）**:
  * **Frontend**: ESLint + Prettier を設定し、彼女のコード品質を自動担保。
  * **Backend**: Ruff + mypy を導入し、保存時に自動フォーマットされる環境を構築。