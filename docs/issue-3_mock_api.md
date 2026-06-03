Issueタイトル: `[Backend/Frontend](3): モックAPIの実装と連携確認`

### 背景
フロントエンドが UI 実装を先行できるように、まずは固定レスポンスのモック API を用意する必要がある。API スキーマを先に合意しておけば、ハイライトや入力判定の実装をバックエンドの完成を待たずに進められる。

### 実施内容
- [x] `GET /api/v1/stages/generate` のモックエンドポイント作成
- [x] Phase 2 で合意した JSON スキーマの固定レスポンス実装
- [x] フロントエンドから API を呼び出して表示確認する接続処理の作成
- [x] `hint` と `noise_text` の表示確認用の簡易画面または検証手順の整備

### 完了条件
- [x] `GET /api/v1/stages/generate?level=hard` に対して固定 JSON が返ること
- [x] フロントエンド画面に `hint` と `noise_text` が表示されること
- [x] 開発中の連携確認が手動または簡易確認で行えること

### 影響範囲
- バックエンドのステージ生成 API
- フロントエンドの API 呼び出し処理
- UI のデータ表示領域

### 開発フェーズ
- マイルストーン0「基盤構築」
- Phase 2: APIスキーマの合意とモック作成

### 参考資料
- [docs/DEVELOPMENT_PLAN.md](docs/DEVELOPMENT_PLAN.md)
- [docs/issue-2_backend_migration_cors_env.md](docs/issue-2_backend_migration_cors_env.md)

### 見積もり工数
- モック API 実装: 1.5h
- 固定 JSON スキーマ反映: 0.5h
- フロントエンド連携確認: 1.0h
- 表示確認用の調整: 0.5h
- 合計目安: 3.5h
