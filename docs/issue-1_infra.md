Issueタイトル: `[Infra](1): 基盤環境と初期設定の構築`

### 背景
MVP の実装を最短で進めるには、フロントエンド、バックエンド、DB、マイグレーション、Lint/Format の基盤を最初に揃える必要がある。ここを先に固めることで、実装途中の環境差分や起動不備による手戻りを防ぎ、以後のタスクを 1 タスク 1 Issue で安全に進められる。

### 実施内容
- [ ] .gitignore / .dockerignore の作成
- [ ] docker-compose.yml の作成 (DBボリューム永続化設定を含む)
- [ ] Dockerfile の作成 (バックエンド/フロントエンド)
- [ ] .env.example の作成
- [ ] FastAPI側のCORS許可設定の雛形作成
- [ ] DBマイグレーションの初期化
- [ ] リンター/フォーマッターの初期設定ファイル作成

### 完了条件
- [ ] `docker compose up -d` で正常起動し、APIドキュメント等にアクセスできること

### 影響範囲
- フロントエンドの開発環境
- バックエンドの起動設定と API 通信
- PostgreSQL の永続化と初期スキーマ管理
- リポジトリ全体の設定ファイルと開発フロー

### 開発フェーズ
- マイルストーン0「基盤構築」
- Phase 1: 開発基盤と初期設定の完了

### 参考資料
- [docs/DEVELOPMENT_PLAN.md](docs/DEVELOPMENT_PLAN.md)
- [docs/architecture.md](docs/architecture.md)

### 見積もり工数
- .gitignore / .dockerignore の作成: 0.5h
- docker-compose.yml の作成: 1.5h
- Dockerfile の作成 (バックエンド/フロントエンド): 2.0h
- .env.example の作成: 0.5h
- FastAPI 側の CORS 設定雛形作成: 0.5h
- DB マイグレーションの初期化: 1.5h
- リンター/フォーマッターの初期設定ファイル作成: 1.0h
- 合計目安: 7.5h
