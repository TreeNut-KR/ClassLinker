from fastapi import FastAPI, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory="D:\\Joffice\\ClassLinker\\ESP_QR_READ\\SER\\SER_FAST_api")

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("FAST_index.html", {"request": request})

@app.post("/QR")
def post_qrcode(request: Request, qrcode):
    return templates.TemplateResponse("FAST_index.html", {"request": request, "qrcode": qrcode})

if __name__ == "__main__":
    uvicorn.run(app, host='192.168.0.20', port=5100)
