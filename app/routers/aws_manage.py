from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter
import awsTools

router = APIRouter(prefix='/cloud_list')

#jinja templates
templates = Jinja2Templates(directory="templates")

@router.get("", response_class=HTMLResponse)
async def cloud_list(request: Request):

    instance_data = awsTools.getInstance()
    vpc_name = awsTools.getVpc()

    items = {}
    for key, value in vpc_name.items():
        items[value] = []
        for instance in instance_data:
            if key == instance['InstanceVPC']:
                items[value].append(instance)   

    return templates.TemplateResponse("cloud_status.html", {"request": request, "instance_data": items})

@router.put("/power", response_class=RedirectResponse)
async def cloud_list(request: Request):
    return RedirectResponse("")