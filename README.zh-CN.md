# LLM Benchmark - 大模型推理性能压测平台

一个专业的 LLM 推理性能测试平台，支持对大模型推理服务进行全面的性能压测和分析。

## 项目简介

LLM Benchmark 是一个基于 Vue 3 + Element Plus + Flask + MySQL 构建的全栈性能测试平台，专为评估大语言模型推理服务而设计。

## 核心功能

### 1. 任务管理
- ✅ 创建性能测试任务
- ✅ 异步执行测试任务（多线程）
- ✅ 实时查看任务状态
- ✅ 按任务名称和状态过滤
- ✅ 分页显示任务列表

### 2. 性能测试
- ✅ 支持多种数据集（random、line_by_line、sharegpt、custom）
- ✅ 可配置并发数和请求数
- ✅ 支持流式输出测试
- ✅ 自定义温度、Token 数等参数

### 3. 结果分析
- ✅ 查看任务基本信息
- ✅ 查看性能报告（文本格式）
- ✅ 查看详细任务日志
- ✅ 查看可视化统计报告（HTML 格式，样式隔离）

### 4. 任务状态
- pending: 待执行
- running: 执行中
- completed: 已完成
- failed: 失败

## 技术栈

### 前端
- Vue 3 (Composition API)
- Element Plus
- Vite
- Vue Router 4
- Axios

### 后端
- Flask
- Flask-SQLAlchemy
- MySQL
- Threading（异步任务）
- python-dotenv

### 性能测试
- evalscope

## 项目结构

```
llm_meter/
├── src/                    # 后端源码
│   ├── server.py          # Flask 主服务
│   ├── models.py          # 数据库模型
│   ├── tasks.py           # 异步任务
│   ├── config.py          # 配置文件
│   └── init_db.py         # 数据库初始化
├── web/                    # 前端源码
│   ├── src/
│   │   ├── views/         # 页面组件
│   │   ├── utils/         # 工具函数
│   │   └── router/        # 路由配置
│   ├── index.html
│   └── package.json
├── outputs/                # 任务输出目录
├── requirements.txt        # Python 依赖
└── .env                   # 环境变量配置
```

## 快速开始

### 环境要求

- Python >= 3.7
- Node.js >= 16.0.0
- MySQL >= 5.7

### 1. 安装依赖

```bash
# Python 依赖
pip install -r requirements.txt

# 前端依赖
cd web
npm install
```

### 2. 配置数据库

```sql
CREATE DATABASE llm_benchmark CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

创建 `.env` 文件：

```bash
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DB=llm_benchmark
TASK_OUTPUT=outputs
```

### 3. 初始化数据库

```bash
cd src
python init_db.py
```

### 4. 启动服务

```bash
# 后端服务
cd src
python server.py

# 前端服务（另一个终端）
cd web
npm run dev
```

### 5. 访问应用

打开浏览器访问: http://localhost:3000

## 使用指南

### 创建测试任务

1. 点击"提交新任务"
2. 填写任务参数（模型、数据集、URL、并发数等）
3. 点击"提交任务"

### 查看任务详情

1. 在任务列表中点击"查看详情"
2. 查看三个标签页：
   - 性能报告：文本格式的性能摘要
   - 任务日志：详细的执行日志
   - 数据统计：可视化的性能统计报告

## API 接口

- GET /api/tasks - 获取任务列表
- GET /api/tasks/<id> - 获取任务详情
- GET /api/tasks/<id>/log - 获取任务日志
- GET /api/tasks/<id>/summaryLog - 获取性能报告
- GET /api/tasks/<id>/stats - 获取统计数据
- POST /api/tasks - 创建任务
- DELETE /api/tasks/<id> - 删除任务

## 生产部署

### 使用 Gunicorn

```bash
pip install gunicorn
cd src
gunicorn -w 4 -b 0.0.0.0:15001 server:app
```

### 构建前端

```bash
cd web
npm run build
```

## 注意事项

1. 确保 MySQL 服务已启动
2. .env 文件必须放在项目根目录
3. 确保端口 3000 和 15001 未被占用
4. 定期清理 outputs 目录下的旧任务数据

## 许可证

MIT License
