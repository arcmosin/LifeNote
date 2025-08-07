# 使用官方 Node 镜像作为构建阶段
FROM node:20 AS build

WORKDIR /app

# 复制 package.json 和 package-lock.json（或 yarn.lock）
COPY package*.json ./

# 安装依赖
RUN npm install


# 复制源代码
COPY . .

# 接收构建参数
ARG VITE_API_BASE_URL
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL

# 构建项目（会输出到 ./dist）
RUN npm run build

# ---- 构建 Nginx 镜像 ----
FROM nginx:alpine

# 删除默认 nginx 配置
RUN rm /etc/nginx/conf.d/default.conf

# 拷贝我们自定义的 nginx 配置
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 从上一步的 build 阶段复制 dist 到 nginx 目录下
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 5178

CMD ["nginx", "-g", "daemon off;"]

# 你可以在构建完成后写入 config.js（此为示例默认值）
RUN echo 'window.__APP_CONFIG__ = { VITE_API_BASE_URL: "http://localhost:8040" }' > /usr/share/nginx/html/config.js

