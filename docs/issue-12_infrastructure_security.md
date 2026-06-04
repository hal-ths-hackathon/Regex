Issueタイトル: `[Infra](12): Cloudflare Tunnelsを用いた安全な外部公開基盤の構築`

### 背景
現在、バックエンドおよびフロントエンドがローカルのDocker環境で稼働している。最終的には自宅ネットワーク内に配置したRaspberry Piから外部（インターネット）へサービスを公開する構成（ラズパイ + Cloudflare）を予定している。
しかし、過去の温湿度計アプリ等と同様の簡易的なポートフォワーディング（ポート開放）を行うと、自宅ネットワーク全体がサイバー攻撃の脅威（DDoS攻撃や不正アクセス）に晒される危険性が高い。
特に本アプリケーションはユーザー入力を扱う（ReDoSリスク等はフロントエンドで軽減するが）ため、インフラレベルでのWAF（Web Application Firewall）やDDoS保護、IP秘匿化が必須である。

### 実施内容
- [ ] Cloudflare Tunnels (`cloudflared`) の導入検討・検証
  - 自宅ルーターのポートを一切開放せずに外部からのアクセスを受け付ける仕組みの構築
- [ ] Cloudflare側でのDNSおよびSSL/TLS証明書（HTTPS化）の設定
- [ ] Raspberry Pi上のDocker Composeネットワークと `cloudflared` コンテナの統合設定
- [ ] （必要に応じて）Cloudflare WAFでの基本的なボット対策・レート制限の設定
- [ ] 本番環境（ラズパイ）用 `.env.production` の分離と機密情報の管理方針の策定

### 完了条件
- [ ] ルーターのポートフォワーディング（静的マスカレード等）を無効化した状態で、外部インターネットから本サービスにHTTPSでアクセスできること
- [ ] オリジンサーバー（Raspberry Pi）のグローバルIPアドレスが外部に漏洩していないこと（Cloudflareのプロキシを通っていること）
- [ ] 構成手順がドキュメント化され、万が一ラズパイが壊れても再構築できる状態になっていること

### 影響範囲
- インフラストラクチャ全体 (Raspberry Pi, Cloudflare)
- `docker-compose.yml` (本番環境向けオーバーライドファイルの作成)

### 開発フェーズ
- マイルストーン1「本番公開基盤の構築」
- Phase 1: ゼロトラストネットワークの構成

### 参考資料
- [docs/README_INFRA.md](docs/README_INFRA.md)
- Cloudflare Zero Trust Documentation

### 見積もり工数
- Cloudflare設定・トンネル開通検証: 2.0h
- Docker Compose連携とプロキシ設定: 1.5h
- WAF・セキュリティルール設定: 1.0h
- ドキュメント化: 0.5h
- 合計目安: 5.0h
