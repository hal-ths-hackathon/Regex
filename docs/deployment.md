# デプロイガイド: Raspberry Pi + Cloudflare Tunnels

本ドキュメントでは、Raspberry Pi 上で Regex Escape ゲームを Cloudflare Tunnels 経由で安全にインターネット公開する手順を説明します。

---

## 構成概要

```
[インターネット]
       │
  ┌────▼────┐
  │Cloudflare│  ← SSL終端・WAF・DDoS保護・IP秘匿
  │  Edge    │
  └────┬────┘
       │ (暗号化トンネル / Outbound only)
       │
  ┌────▼──────────────────────────────────┐
  │  Raspberry Pi (Docker)                │
  │                                       │
  │  ┌─────────────┐                      │
  │  │ cloudflared  │ ← Tunnel Agent      │
  │  └──┬──────┬───┘                      │
  │     │      │   Docker内部ネットワーク  │
  │  ┌──▼──┐ ┌─▼───────┐ ┌──────┐        │
  │  │front│ │ backend  │ │  db  │        │
  │  │:80  │ │ :8000    │ │:5432 │        │
  │  └─────┘ └──────────┘ └──────┘        │
  └───────────────────────────────────────┘
  ※ ルーターのポート開放は一切不要
```

**ポイント:**
- `cloudflared` はオリジンサーバーから Cloudflare へ **アウトバウンド接続** するため、ルーターのインバウンドポート開放が不要
- Cloudflare がリバースプロキシとなり、オリジンIPを完全に秘匿
- SSL/TLS 証明書は Cloudflare が自動管理

---

## 前提条件

- Raspberry Pi に Docker と Docker Compose がインストール済み
- Cloudflare アカウントを持っている
- 独自ドメインを Cloudflare に登録済み（ネームサーバー移管完了）
- Git でリポジトリをクローン済み

---

## 手順

### 1. Cloudflare Tunnel の作成

1. [Cloudflare Zero Trust ダッシュボード](https://one.dash.cloudflare.com/) にログイン
2. **Networks** > **Tunnels** > **Create a tunnel** をクリック
3. **Cloudflared** を選択し **Next**
4. トンネル名を入力（例: `regex-escape-prod`）
5. **Docker** のインストール方法が表示されるので、表示された `TUNNEL_TOKEN` の値をコピー
6. **Public Hostnames** タブで以下のルーティングを設定:

| Subdomain | Domain | Service |
|-----------|--------|---------|
| (空 or www) | `<YOUR_DOMAIN>` | `http://frontend:80` |
| api | `<YOUR_DOMAIN>` | `http://backend:8000` |

> **Note:** Service URL にはコンテナ名を使います。`cloudflared` は同一 Docker ネットワーク内のサービスに名前解決できます。

7. **Save tunnel**

### 2. `.env.production` の作成

```bash
cd /path/to/Regex
cp .env.production.example .env.production
```

`.env.production` を編集し、以下の値を設定:

```ini
# 安全なパスワードを生成して設定
POSTGRES_USER=regex_prod
POSTGRES_PASSWORD=<ランダムな強力パスワード>
POSTGRES_DB=regex_prod
DATABASE_URL=postgresql+psycopg2://regex_prod:<上と同じパスワード>@db:5432/regex_prod

# 手順1でコピーしたトンネルトークン
CLOUDFLARE_TUNNEL_TOKEN=eyJ...（トークン全体を貼り付け）

# Cloudflare で公開するドメイン
CORS_ORIGINS=https://<YOUR_DOMAIN>
```

> **⚠️ このファイルは `.gitignore` で除外されます。Git にコミットしないでください。**

### 3. 本番環境の起動

```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml \
  --env-file .env.production up -d --build
```

#### 起動確認

```bash
# 全コンテナが running であることを確認
docker compose -f docker-compose.yml -f docker-compose.prod.yml \
  --env-file .env.production ps

# cloudflared のログでトンネル接続を確認
docker compose -f docker-compose.yml -f docker-compose.prod.yml \
  --env-file .env.production logs cloudflared
```

正常であれば、ログに以下のような出力が表示されます:
```
Connection registered connIndex=0 ...
```

### 4. Cloudflare SSL/TLS 設定

Cloudflare ダッシュボードで以下を設定:

1. **SSL/TLS** > **Overview** > **Full (strict)** を選択
   - Cloudflare ↔ オリジン間も暗号化される（cloudflared が自動処理）
2. **SSL/TLS** > **Edge Certificates** > **Always Use HTTPS** を ON
3. **SSL/TLS** > **Edge Certificates** > **Minimum TLS Version** を **TLS 1.2** に設定

### 5. WAF・セキュリティ設定（推奨）

#### レート制限

Cloudflare ダッシュボード > **Security** > **WAF** > **Rate limiting rules** で以下を作成:

| ルール名 | 条件 | アクション | 閾値 |
|---------|------|----------|------|
| API Rate Limit | URI Path starts with `/api/` | Block | 60 requests / 1 minute per IP |

#### ボット対策

**Security** > **Bots** > **Bot Fight Mode** を ON

#### マネージドルール

**Security** > **WAF** > **Managed rules** で **Cloudflare Managed Ruleset** を有効化

---

## 運用コマンド

### サービス停止

```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml \
  --env-file .env.production down
```

### ログの確認

```bash
# 全サービスのログ
docker compose -f docker-compose.yml -f docker-compose.prod.yml \
  --env-file .env.production logs -f

# 特定サービスのログ
docker compose -f docker-compose.yml -f docker-compose.prod.yml \
  --env-file .env.production logs -f backend
```

### アップデート（Git pull → 再ビルド）

```bash
git pull origin main
docker compose -f docker-compose.yml -f docker-compose.prod.yml \
  --env-file .env.production up -d --build
```

---

## トラブルシューティング

### cloudflared がトンネルに接続できない

```bash
# ログを確認
docker compose -f docker-compose.yml -f docker-compose.prod.yml \
  --env-file .env.production logs cloudflared

# よくある原因:
# - CLOUDFLARE_TUNNEL_TOKEN が間違っている → .env.production を確認
# - DNS解決ができない → Raspberry Pi のネットワーク設定を確認
# - 時刻がずれている → sudo timedatectl set-ntp true
```

### サイトにアクセスできるがAPIが404

- Cloudflare ダッシュボードの Public Hostnames 設定を再確認
- `api.<YOUR_DOMAIN>` → `http://backend:8000` のルーティングが正しいか確認

### DBデータの永続化確認

```bash
# Docker volume を確認
docker volume ls | grep pgdata
```

---

## 災害復旧手順（Raspberry Pi 障害時）

万が一 Raspberry Pi が故障した場合の再構築手順:

1. **新しい Raspberry Pi に Docker / Docker Compose をインストール**
2. **リポジトリをクローン**
   ```bash
   git clone https://github.com/hal-ths-hackathon/Regex.git
   cd Regex
   ```
3. **`.env.production` を再作成**（バックアップから復元、または手順2で新規作成）
4. **本番環境を起動**
   ```bash
   docker compose -f docker-compose.yml -f docker-compose.prod.yml \
     --env-file .env.production up -d --build
   ```
5. **Cloudflare ダッシュボードでトンネルが再接続されたことを確認**

> **⚠️ DBデータについて**: Docker Volume はホスト側に保存されるため、SDカード / ストレージが故障するとデータは失われます。重要なデータがある場合は定期的な `pg_dump` バックアップを検討してください。

---

## 開発環境との使い分け

| 環境 | コマンド | ポート公開 | トンネル |
|------|---------|----------|---------|
| **開発** | `docker compose up -d` | ✅ 8090, 3000, 5439 | なし |
| **本番** | `docker compose -f ... -f docker-compose.prod.yml ...` | ❌ なし | ✅ Cloudflare |

開発用の `docker-compose.yml` は一切変更していないため、ローカル開発は今まで通り動作します。
