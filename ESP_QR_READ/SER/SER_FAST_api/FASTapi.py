from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse
from pydantic import BaseModel
import uvicorn

app = FastAPI()

templates = Jinja2Templates(directory="./")

class Item(BaseModel):
    qrcode: str

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("FAST_index.html", {"request": request})

@app.post("/QR")
async def api(item: Item):
    qr_code_value = item.qrcode
    return JSONResponse(content=item.dict(), status_code=200)

if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port=5100)
