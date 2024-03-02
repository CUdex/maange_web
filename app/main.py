from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
from routers import vm_manage
from routers import aws_manage
from routers import test_curl

# fastapi 객체 생성
app = FastAPI()
app.include_router(vm_manage.router)
app.include_router(aws_manage.router)
app.include_router(test_curl.router)
#jinja templates
templates = Jinja2Templates(directory="templates")
app.mount("/css", StaticFiles(directory="css"), name="css")
app.mount("/js", StaticFiles(directory="js"), name="js")

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})

if __name__=='__main__':
    uvicorn.run(app, host='0.0.0.0', port = 80)

