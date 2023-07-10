from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn
from routers import vm_manage
from routers import aws_manage

# fastapi 객체 생성
app = FastAPI()
app.include_router(vm_manage.router)
app.include_router(aws_manage.router)
#jinja templates
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})

if __name__=='__main__':
    uvicorn.run(app, host='0.0.0.0', port = 80)

