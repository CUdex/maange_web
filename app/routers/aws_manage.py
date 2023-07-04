from fastapi import Request
from fastapi.responses import HTMLResponse
import mysql.connector
import tools
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter

router = APIRouter(prefix='/cloud_list')

#jinja templates
templates = Jinja2Templates(directory="templates")

@router.get("", response_class=HTMLResponse)
async def search_vm(request: Request, vm_name: str = ""):
    
    return {'message': 'Hello'}