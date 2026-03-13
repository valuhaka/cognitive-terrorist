from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

#-- initialization --#

app = FastAPI()

base_dir = Path(__file__).resolve().parent
files_dir = base_dir / "files"
static_dir = base_dir / "static"

#-- api endpoints --#

@app.get("/list")
def list_files():
    if not files_dir.exists():
        return []

    files = []
    for file_item in files_dir.iterdir():
        if file_item.is_file():
            files.append(file_item.name)

    return files

@app.get("/files/{name}")
def get_file(name: str):
    path = (files_dir / name).resolve()

    # prevent path traversal outside files directory
    if not str(path).startswith(str(files_dir.resolve())):
        raise HTTPException(status_code=403)

    if not path.exists() or not path.is_file():
        raise HTTPException(status_code=404)

    return FileResponse(path)

#-- static mounts --#

app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")