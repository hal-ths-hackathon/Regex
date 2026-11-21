# =============================================================================
# frontend/Dockerfile
#   - target "dev"  : Vite 開発サーバー（ローカル開発専用。公開しないこと）
#   - target "prod" : ビルド済みの静的ファイルを nginx（非root）で配信
# =============================================================================

# --- 依存インストール ---
FROM node:22.23.5-alpine3.24 AS deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci

# --- 開発用（docker-compose.override.yml から使用） ---
FROM deps AS dev
COPY . .
RUN chown -R node:node /app
USER node
EXPOSE 5173
CMD ["npm", "run", "dev", "--", "--host"]

# --- ビルド ---
FROM deps AS build
# API の URL はビルド時に JS へ埋め込まれるため build arg で受け取る
ARG VITE_API_BASE_URL=http://localhost:8090
ENV VITE_API_BASE_URL=${VITE_API_BASE_URL}
COPY . .
RUN npm run build

# --- 本番用 ---
FROM nginxinc/nginx-unprivileged:1.30.6-alpine AS prod
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 8080
