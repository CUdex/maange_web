from fastapi import Request
from fastapi.responses import HTMLResponse, PlainTextResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Response
import awsTools
import models

router = APIRouter(prefix='/cloud_list')

#jinja templates
templates = Jinja2Templates(directory="templates")

@router.get("", response_class=HTMLResponse)
async def cloud_list(request: Request):
    return templates.TemplateResponse("cloud_status.html", {"request": request})

@router.get("/new", response_class=HTMLResponse)
async def cloud_list(request: Request):
    return templates.TemplateResponse("new_status.html", {"request": request})

@router.get("/instance")
async def cloud_list(request: Request, question: bool = False):
    
    if question:
        instance_data = awsTools.getInstance()
        return JSONResponse(content={"instance_data": instance_data})

    instance_data = awsTools.getInstance()
    vpc_name = awsTools.getVpc()

    items = {}
    for key, value in vpc_name.items():
        items[value] = []
        for instance in instance_data:
            if key == instance['InstanceVPC']:
                items[value].append(instance)       

    return templates.TemplateResponse("cloud_status.html", {"request": request, "instance_data": items})

@router.put("/power", response_class=PlainTextResponse)
async def power_oper(body: models.instanceOperBody):
    oper = body.oper
    id = body.instanceId
    print(id)

    if oper == 'start':
        awsTools.startInstance(id)
    else:
        awsTools.stopInstance(id)

    return f"{id} {oper} 명령 완료"

@router.put("/tag", response_class=Response)
async def power_oper(body: models.TagChangeData):
    id = body.instance_id
    tag_key = body.tag_key
    state = body.state

    result = awsTools.updateTag(id, tag_key, state)
    # AWS 응답에서 HTTP 상태 코드 추출
    http_status_code = result.get('ResponseMetadata', {}).get('HTTPStatusCode', 500)  # 기본값으로 500 설정
    
    if http_status_code == 200:
        return Response(content="Success Update Tag", status_code=http_status_code)
    else:
        # 실패한 경우, 실패 메시지와 함께 상태 코드 반환
        return Response(content="Failed Update Tag", status_code=http_status_code)