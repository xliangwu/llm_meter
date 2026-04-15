import os
import json
import multiprocessing
from datetime import datetime
from evalscope.perf.main import run_perf_benchmark
from evalscope.perf.arguments import Arguments
from models import db, Task
from config import Config


def run_benchmark_task(task_id, task_data):
    from server import app

    with app.app_context():
        task = None
        try:
            task = Task.query.get(task_id)
            if not task:
                print(f"Task {task_id} not found")
                return

            print(f"[{task_id}] Starting benchmark task...")

            task.status = "running"
            task.updated_at = datetime.utcnow()
            db.session.commit()

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            task_name = task.name
            output_path = os.path.join(Config.OUTPUTS_DIR, timestamp, task_name)
            output_dir = os.path.join(Config.OUTPUTS_DIR, timestamp)

            extra_args = {}
            if task.extra_args:
                try:
                    extra_args = json.loads(task.extra_args)
                except:
                    extra_args = {}

            parallel_list = (
                [int(x) for x in task.parallel.split()]
                if isinstance(task.parallel, str)
                else task.parallel
            )
            number_list = (
                [int(x) for x in task.number.split()]
                if isinstance(task.number, str)
                else task.number
            )

            task_cfg = Arguments(
                no_timestamp=True,
                parallel=parallel_list,
                number=number_list,
                model=task.model,
                url=task.url,
                api="openai",
                dataset=task.dataset,
                min_tokens=task.max_tokens,
                max_tokens=task.max_tokens,
                max_prompt_length=extra_args.get("max_prompt_length", 131072),
                min_prompt_length=extra_args.get("min_prompt_length", 0),
                prefix_length=extra_args.get("prefix_length", 0),
                prompt=extra_args.get("prompt"),
                query_template=extra_args.get("query_template"),
                image_width=extra_args.get("image_width", 224),
                image_height=extra_args.get("image_height", 224),
                image_format=extra_args.get("image_format", "RGB"),
                image_num=extra_args.get("image_num", 1),
                outputs_dir=output_dir,
                tokenizer_path="Qwen/Qwen2.5-0.5B-Instruct",
                name=task_name,
                **{
                    k: v
                    for k, v in extra_args.items()
                    if k
                    not in [
                        "max_prompt_length",
                        "min_prompt_length",
                        "prefix_length",
                        "prompt",
                        "query_template",
                        "image_width",
                        "image_height",
                        "image_format",
                        "image_num",
                    ]
                },
            )

            print(
                f"[{task_id}] Running benchmark with config: parallel={parallel_list}, number={number_list}"
            )
            print(f"[{task_id}] Output directory: {output_path}")

            bench_mark_result = run_perf_benchmark(task_cfg)

            task.status = "completed"
            task.output_path = output_path
            task.completed_at = datetime.utcnow()
            task.updated_at = datetime.utcnow()
            db.session.commit()

            print(f"[{task_id}] Task completed successfully")
            print(f"[{task_id}] Benchmark result: {bench_mark_result}")

        except Exception as e:
            error_msg = f"{type(e).__name__}: {str(e)}"
            print(f"[{task_id}] Task failed with error: {error_msg}")

            if task:
                task.status = "failed"
                task.completed_at = datetime.utcnow()
                task.updated_at = datetime.utcnow()
                db.session.commit()

            import traceback

            traceback.print_exc()


def async_run_perf_benchmark(task_id, task_data):
    process = multiprocessing.Process(
        target=run_benchmark_task,
        args=(task_id, task_data),
        name=f"Task-{task_id}",
    )
    process.daemon = True
    process.start()
    print(f"Task {task_id} submitted and started in background process")
    return process
