# 快速启动指南

## 1. 配置数据库

创建 `.env` 文件（在项目根目录）：

```bash
cp .env.example .env
```

编辑 `.env` 文件，修改数据库配置：

```bash
MYSQL_HOST=your_mysql_host
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DB=llm_benchmark
```

## 2. 验证配置

```bash
cd src
python test_config.py
```

## 3. 初始化数据库

```bash
cd src
python init_db.py
```

## 4. 启动后端服务

```bash
cd src
python server.py
```

后端服务将运行在: http://localhost:15001

## 5. 启动前端服务

```bash
cd web
npm install
npm run dev
```

前端服务将运行在: http://localhost:3000

## 常见问题

### 1. 数据库连接失败

检查：
- MySQL 服务是否启动
- `.env` 文件中的配置是否正确
- 数据库是否已创建

### 2. .env 文件未被读取

确保：
- `.env` 文件在项目根目录（与 `src` 同级）
- 已安装 `python-dotenv` 包

### 3. 端口被占用

修改端口：
- 后端：编辑 `src/server.py` 最后一行的 `port=15001`
- 前端：编辑 `web/vite.config.js` 中的 `server.port`
