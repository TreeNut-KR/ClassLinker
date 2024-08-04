from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()

class Item(BaseModel):
    content: str = None

@app.post("/")
async def read_root(item: Item):
    return {"message": "Hello, FastAPI!!!"}

@app.get("/")
async def get_root():
    return {"message": "This is a GET request."}


# uvicorn 실행 코드 추가
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
