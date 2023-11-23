import aiofiles
from fastapi import HTTPException


async def save_files(files):
    i = 0
    for file in files:
        try:
            if file.content_type not in ["image/jpeg", "image/png"]:
                raise HTTPException(400, detail="Invalid document type")
            if file.content_type == "image/jpeg":
                ext=".jpg"
            elif file.content_type == "image/png":
                ext=".png"
            out_path = f'files/image_{i}{ext}'
            async with aiofiles.open(out_path, 'wb') as out_file:
                while content := await file.read(1024):
                    await out_file.write(content)
            i+=1
        except Exception:
            return {"message": "There was an error uploading the file(s)"}
        finally:
            file.file.close()