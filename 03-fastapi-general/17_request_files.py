from typing import Annotated

import uvicorn
from fastapi import FastAPI, File, UploadFile
from starlette.responses import HTMLResponse

app = FastAPI()


# <UploadFile 클래스로 파일 업로드하기>

@app.post("/files/")
async def create_file(file: bytes = File()):
    return {"file_size": len(file)}


# <file 매개변수를 bytes 타입 대신 UploadFile 로 선언 시 장점>
# - 'Spooled File' 을 사용한다. 즉, 최대 크기 제한 까지만 메모리에 저장되고 이후 데이터는 디스크에 저장된다.
# - 대용량 이미지, 비디오 들이 메모리를 다 잡아먹으면서 업로드 되지 않는다는 뜻이다.
# - 업로드된 파일은 메타 데이터를 가지고 있다.
# - file-like async interface 를 가지고 있어서 .read(), .write(), .seek() 등 file operation 을 할 수 있다.
#   (모두 async function 이므로 사용 시 await 키워드 붙여 주어야 함)
# - 파이썬에서 SpooledTemporaryFile 객체로 다뤄지기 때문에 해당 객체를 사용하는 다른 라이브러리에 넘길 수 있다.
@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"file_name": file.filename, "file_size": file.size, "file_headers": file.headers}


# <multiple files>
@app.post("/multiple/files/")
async def create_file(files: Annotated[list[bytes], File(description="파일을 업로드하면 bytes 형태로 읽힌다.")] = None):
    return {"file_size": [len(file) for file in files]}


@app.post("/multiple/uploadfiles/")
async def create_upload_file(
        files: Annotated[list[UploadFile], File(description="파일을 업로드 하면 UploadFile 형태로 읽힌다.")] = None):
    return {"file_names": [file.filename for file in files], "file_sizes": [file.size for file in files]}


@app.get("/")
async def main():
    content = """
<body>
<form action="/multiple/files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>

<form action="/multiple/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)


if __name__ == "__main__":
    uvicorn.run("17_request_files:app", host="localhost", port=8000, reload=True)
