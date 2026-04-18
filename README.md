# LLM Benchmark - LLM Inference Performance Benchmark Platform

English | [中文](./README.zh-CN.md)

A professional LLM inference performance testing platform that enables comprehensive performance benchmarking and analysis for large language model inference services.

## Project Introduction

LLM Benchmark is a full-stack performance testing platform built with Vue 3 + Element Plus + Flask + MySQL, specifically designed for evaluating large language model inference services.

## Core Features

### 1. Task Management
- ✅ Create performance testing tasks
- ✅ Asynchronous task execution (multi-threading)
- ✅ Real-time task status monitoring
- ✅ Filter tasks by name and status
- ✅ Pagination for task list

### 2. Performance Testing
- ✅ Support multiple datasets (random, line_by_line, sharegpt, custom)
- ✅ Configurable concurrency and request count
- ✅ Support streaming output testing
- ✅ Customizable parameters like temperature, token count, etc.

### 3. Result Analysis
- ✅ View basic task information
- ✅ View performance report (text format)
- ✅ View detailed task logs
- ✅ View visualized statistical report (HTML format, style isolated)

### 4. Task Status
- pending: Pending execution
- running: Running
- completed: Completed
- failed: Failed

## Tech Stack

### Frontend
- Vue 3 (Composition API)
- Element Plus
- Vite
- Vue Router 4
- Axios

### Backend
- Flask
- Flask-SQLAlchemy
- MySQL
- Threading (asynchronous tasks)
- python-dotenv

### Performance Testing
- evalscope

## Project Structure

```
llm_meter/
├── src/                    # Backend source code
│   ├── server.py          # Flask main server
│   ├── models.py          # Database models
│   ├── tasks.py           # Asynchronous tasks
│   ├── config.py          # Configuration
│   └── init_db.py         # Database initialization
├── web/                    # Frontend source code
│   ├── src/
│   │   ├── views/         # Page components
│   │   ├── utils/         # Utility functions
│   │   └── router/        # Route configuration
│   ├── index.html
│   └── package.json
├── outputs/                # Task output directory
├── requirements.txt        # Python dependencies
└── .env                   # Environment variables
```

## Quick Start

### Requirements

- Python >= 3.7
- Node.js >= 16.0.0
- MySQL >= 5.7

### 1. Install Dependencies

```bash
# Python dependencies
pip install -r requirements.txt

# Frontend dependencies
cd web
npm install
```

### 2. Configure Database

```sql
CREATE DATABASE llm_benchmark CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Create `.env` file:

```bash
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DB=llm_benchmark
TASK_OUTPUT=outputs
```

### 3. Initialize Database

```bash
cd src
python init_db.py
```

### 4. Start Services

```bash
# Backend service
cd src
python server.py

# Frontend service (in another terminal)
cd web
npm run dev
```

### 5. Access the Application

Open your browser and visit: http://localhost:3000

## Usage Guide

### Create a Test Task

1. Click "Submit New Task"
2. Fill in task parameters (model, dataset, URL, concurrency, etc.)
3. Click "Submit Task"

### View Task Details

1. Click "View Details" in the task list
2. Three tabs available:
   - Performance Report: Text format performance summary
   - Task Log: Detailed execution logs
   - Statistics: Visual performance statistics report

## API Endpoints

- GET /api/tasks - Get task list
- GET /api/tasks/<id> - Get task details
- GET /api/tasks/<id>/log - Get task log
- GET /api/tasks/<id>/summaryLog - Get performance report
- GET /api/tasks/<id>/stats - Get statistics data
- POST /api/tasks - Create task
- DELETE /api/tasks/<id> - Delete task

## Production Deployment

### Using Gunicorn

```bash
pip install gunicorn
cd src
gunicorn -w 4 -b 0.0.0.0:15001 server:app
```

### Build Frontend

```bash
cd web
npm run build
```

## Notes

1. Ensure MySQL service is started
2. .env file must be placed in the project root directory
3. Ensure ports 3000 and 15001 are not occupied
4. Periodically clean up old task data in the outputs directory

## License

MIT License
