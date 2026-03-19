from .celery_app import celery_app
from services.text_analyzer import TextAnalyzer
from infrastructure.excel_writer import ExcelWriter

import aiofiles
import asyncio


@celery_app.task
def process_file_task(input_path: str, output_path: str):
    asyncio.run(process_file(input_path, output_path))
    return {"output": output_path}


async def process_file(input_path: str, output_path: str):
    analyzer = TextAnalyzer()

    async with aiofiles.open(input_path, "r") as f:
        line_index = 0

        async for line in f:
            analyzer.process_line(line, line_index)
            line_index += 1

    writer = ExcelWriter()
    writer.write_streaming(output_path, analyzer)