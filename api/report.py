import uuid

from fastapi import APIRouter, UploadFile, File
import tempfile
import aiofiles
from fastapi.responses import FileResponse

from workers.celery_app import celery_app
from workers.tasks import process_file_task

router = APIRouter()


@router.post("/public/report/export")
async def export_report(file: UploadFile = File(...)):
    input_path = f"/data/{uuid.uuid4()}.txt"
    output_path = f"{input_path}.xlsx"

    async with aiofiles.open(input_path, "wb") as f:
        while chunk := await file.read(1024 * 1024):
            await f.write(chunk)

    task = process_file_task.delay(input_path, output_path)

    return {
        "task_id": task.id,
        "status": "processing"
    }


@router.get("/tasks/{task_id}/download")
def download_result(task_id: str):
    result = celery_app.AsyncResult(task_id)

    if result.status != "SUCCESS":
        return {
            "status": result.status,
            "message": "File not ready"
        }

    file_path = result.result.get("output")

    return FileResponse(
        path=file_path,
        filename="report.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


@router.get("/tasks/{task_id}")
def get_status(task_id: str):
    result = celery_app.AsyncResult(task_id)

    return {
        "status": result.status,
        "result": str(result.result),
        "traceback": result.traceback
    }