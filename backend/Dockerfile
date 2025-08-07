# 使用轻量级 Python 镜像
FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 复制依赖文件并安装依赖
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com

# 复制整个后端代码
COPY . .

# 设置环境变量
ENV PYTHONUNBUFFERED=1

# 启动 FastAPI 应用
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8040"]
