Issueタイトル: `[Fullstack](6): アーケードランキング機能の実装`

### 背景
リプレイ性を高めるには、クリア後にスコアを保存し、ランキングとして見せる仕組みが必要になる。ゲームとしての達成感と継続利用の導線を作るために、フルスタックでのランキング機能を実装する。

### 実施内容
- [ ] スコア登録用 API の作成
- [ ] ランキング取得用 API の作成
- [ ] 3 文字ネーム入力 UI の作成
- [ ] 登録後にランキングを表示する UI の作成
- [ ] DB への保存と取得の接続確認

### 完了条件
- [ ] 登録したスコアが DB に保存されること
- [ ] ランキング画面で上位順に表示されること
- [ ] クリア後のネーム入力から登録まで一連の流れが動くこと

### 影響範囲
- バックエンドのスコア API
- PostgreSQL のスコアテーブル
- フロントエンドのリザルト画面
- ランキング表示 UI

### 開発フェーズ
- マイルストーン0「基盤構築」
- Phase 4: アーケードランキング機能の実装

### 参考資料
- [docs/DEVELOPMENT_PLAN.md](docs/DEVELOPMENT_PLAN.md)
- [docs/issue-4_problem_generation.md](docs/issue-4_problem_generation.md)
- [docs/issue-5_play_screen_logic.md](docs/issue-5_play_screen_logic.md)

### 見積もり工数
- スコア登録 API: 1.0h
- ランキング取得 API: 1.0h
- ネーム入力 UI: 0.5h
- ランキング表示 UI: 1.0h
- DB 接続確認: 0.5h
- 合計目安: 4.0h
