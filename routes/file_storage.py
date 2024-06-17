from fastapi import APIRouter
from fastapi import Path, HTTPException
from fastapi.responses import FileResponse
import os
import mimetypes




file_storage = APIRouter()


# API FOR FETCHING FILE
@file_storage.get('/file/download/{subpath:path}')
async def download_file(subpath: str = Path(..., description="The path to the file")):
    path = subpath
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="File not found")
    
    mime_type, _ = mimetypes.guess_type(path)
    if mime_type is None:
        mime_type = "application/octet-stream"
    headers = {"Content-Disposition": f'inline; filename="{path}"'}
    
    # Return the file as a response
    return FileResponse(path=path, media_type=mime_type, headers=headers)