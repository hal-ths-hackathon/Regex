FROM node:20-alpine

WORKDIR /app

# ライブラリの定義ファイルをコピー
COPY package*.json ./

# ライブラリをインストール
RUN npm install

# ソースコードをすべてコピー
COPY . .

# Viteのデフォルトポートを指定
EXPOSE 5173

# Dockerの外からアクセスできるように `--host` をつけてReactを起動
CMD ["npm", "run", "dev", "--", "--host"]