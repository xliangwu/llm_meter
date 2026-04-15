from datetime import datetime
import json
import os
import uuid
from werkzeug.utils import secure_filename

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from config import Config
from models import Task, Dataset, db
from tasks import async_run_perf_benchmark

app = Flask(__name__)
app.config.from_object(Config)

CORS(app)
db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    name = request.args.get("name", "")
    status = request.args.get("status", "")
    page = int(request.args.get("page", 1))
    page_size = int(request.args.get("page_size", 10))

    query = Task.query

    if name:
        query = query.filter(Task.name.ilike(f"%{name}%"))
    if status:
        query = query.filter(Task.status == status)

    total = query.count()
    tasks = (
        query.order_by(Task.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    return jsonify(
        {
            "data": [task.to_dict() for task in tasks],
            "total": total,
            "page": page,
            "page_size": page_size,
        }
    )


@app.route("/api/tasks/<task_id>", methods=["GET"])
def get_task(task_id):
    task = Task.query.get(task_id)

    if not task:
        return jsonify({"error": "Task not found"}), 404

    task_dict = task.to_dict()

    if task.output_path and os.path.exists(task.output_path):
        summary_file = os.path.join(task.output_path, "benchmark_summary.json")
        if os.path.exists(summary_file):
            with open(summary_file, "r") as f:
                task_dict["summary"] = json.load(f)

    return jsonify(task_dict)


@app.route("/api/tasks/<task_id>/log", methods=["GET"])
def get_task_log(task_id):
    task = Task.query.get(task_id)

    if not task:
        return jsonify({"error": "Task not found"}), 404

    if not task.output_path or not os.path.exists(task.output_path):
        return jsonify({"data": "任务输出目录不存在"})

    log_file = os.path.join(task.output_path, "benchmark.log")
    print(f"log_file: {log_file}")
    if os.path.exists(log_file):
        with open(log_file, "r") as f:
            log_content = f.read()
        return jsonify({"data": log_content})
    else:
        return jsonify({"data": "日志文件不存在"})


@app.route("/api/tasks/<task_id>/summaryLog", methods=["GET"])
def get_task_summary_log(task_id):
    task = Task.query.get(task_id)

    if not task:
        return jsonify({"error": "Task not found"}), 404

    if not task.output_path or not os.path.exists(task.output_path):
        return jsonify({"data": "任务输出目录不存在"})

    log_file = os.path.join(task.output_path, "performance_summary.txt")

    if os.path.exists(log_file):
        with open(log_file, "r") as f:
            log_content = f.read()
        return jsonify({"data": log_content})
    else:
        return jsonify({"data": "日志文件不存在"})


@app.route("/api/tasks/<task_id>/stats", methods=["GET"])
def get_task_stats(task_id):
    task = Task.query.get(task_id)

    if not task:
        return jsonify({"error": "Task not found"}), 404

    if not task.output_path or not os.path.exists(task.output_path):
        return jsonify({"data": ""})

    html_file = os.path.join(task.output_path, "perf_report.html")

    if os.path.exists(html_file):
        with open(html_file, "r") as f:
            html_content = f.read()
        return jsonify({"data": html_content})
    else:
        return jsonify({"data": ""})


# submit one task
@app.route("/api/tasks", methods=["POST"])
def create_task():
    data = request.json
    task_id = str(uuid.uuid4())

    required_fields = ["model", "dataset", "url"]
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({"error": f"{field} is required"}), 400

    extra_args = {}
    exclude_fields = [
        "model",
        "dataset",
        "url",
        "parallel",
        "number",
        "max_tokens",
        "name",
    ]
    for key, value in data.items():
        if key not in exclude_fields and value is not None:
            extra_args[key] = value

    task = Task(
        id=task_id,
        name=data.get("name"),
        model=data["model"],
        dataset=data["dataset"],
        url=data["url"],
        parallel=data.get("parallel", 1),
        number=data.get("number", 10),
        max_tokens=data.get("max_tokens", 1024),
        extra_args=json.dumps(extra_args) if extra_args else None,
        status="pending",
    )

    db.session.add(task)
    db.session.commit()

    async_run_perf_benchmark(task_id, task.to_dict())

    return jsonify(task.to_dict()), 201


@app.route("/api/tasks/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = Task.query.get(task_id)

    if not task:
        return jsonify({"error": "Task not found"}), 404

    db.session.delete(task)
    db.session.commit()

    return jsonify({"message": "Task deleted successfully"})


@app.route("/api/datasets/upload", methods=["POST"])
def upload_dataset():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    dataset_name = request.form.get("dataset_name")
    dataset_desc = request.form.get("dataset_desc")

    if not dataset_name:
        return jsonify({"error": "dataset_name is required"}), 400

    datasets_dir = os.path.join(Config.OUTPUTS_DIR)
    os.makedirs(datasets_dir, exist_ok=True)

    filename = secure_filename(file.filename)
    file_path = os.path.join(datasets_dir, filename)

    if os.path.exists(file_path):
        return jsonify({"error": "File already exists"}), 400

    file.save(file_path)

    dataset_id = str(uuid.uuid4())
    dataset = Dataset(
        id=dataset_id,
        dataset_name=dataset_name,
        dataset_desc=dataset_desc,
        dataset_path=file_path,
    )

    db.session.add(dataset)
    db.session.commit()

    return jsonify(dataset.to_dict()), 201


@app.route("/api/datasets", methods=["GET"])
def get_datasets():
    page = int(request.args.get("page", 1))
    page_size = int(request.args.get("page_size", 10))
    
    query = Dataset.query
    
    total = query.count()
    datasets = (
        query.order_by(Dataset.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )
    
    return jsonify(
        {
            "data": [dataset.to_dict() for dataset in datasets],
            "total": total,
            "page": page,
            "page_size": page_size,
        }
    )


@app.route("/api/datasets/<dataset_id>", methods=["DELETE"])
def delete_dataset(dataset_id):
    dataset = Dataset.query.get(dataset_id)

    if not dataset:
        return jsonify({"error": "Dataset not found"}), 404

    if dataset.dataset_path and os.path.exists(dataset.dataset_path):
        os.remove(dataset.dataset_path)

    db.session.delete(dataset)
    db.session.commit()

    return jsonify({"message": "Dataset deleted successfully"})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=15001)
