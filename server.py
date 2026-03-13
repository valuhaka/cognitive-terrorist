from fastapi import FastAPI, HTTPException, Request
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
    opt = {
        "verbose": True
    }
    
    if not files_dir.exists():
        return []

    files = []
    for file_item in files_dir.iterdir():
        if file_item.is_file():
            files.append(file_item.name)

    if opt["verbose"]:
        print("Listed files directory.")

    return files


@app.get("/files/{name}")
def get_file(name: str):
    opt = {
        "verbose": True
    }
    
    path = (files_dir / name).resolve()

    if not str(path).startswith(str(files_dir.resolve())):
        raise HTTPException(status_code=403)

    if not path.exists() or not path.is_file():
        raise HTTPException(status_code=404)

    if opt["verbose"]:
        print(f"Served file: {name}")

    return FileResponse(path)


@app.post("/files/{name}")
async def save_file(name: str, request: Request):
    opt = {
        "verbose": True
    }
    
    path = (files_dir / name).resolve()

    if not str(path).startswith(str(files_dir.resolve())):
        raise HTTPException(status_code=403)

    if not path.exists() or not path.is_file():
        raise HTTPException(status_code=404)

    # intercept raw binary stream
    body = await request.body()
    
    # overwrite existing file
    with open(path, "wb") as file_handle:
        file_handle.write(body)

    if opt["verbose"]:
        print(f"Overwrote file on disk: {name}")

    return {"status": "success"}

#-- static mounts --#

app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")