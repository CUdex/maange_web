from fastapi import Request
from fastapi.responses import HTMLResponse, PlainTextResponse, FileResponse
import mysql.connector
import tools
from fastapi.templating import Jinja2Templates
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from fastapi import APIRouter
import models

router = APIRouter(prefix='/vm_list')

#jinja templates
templates = Jinja2Templates(directory="templates")

def db_query(query, function_name = 'etc'):
    db_info = tools.readAppInfo()
    # MySQL 연결 설정
    mydb = mysql.connector.connect(
      host=db_info['db_host'],
      user=db_info['db_user'],
      password=db_info['db_passwd'],
      database=db_info['db_database']
    )

    # 쿼리 실행
    mycursor = mydb.cursor()
    mycursor.execute(query)
    
    if function_name == 'search_vm':
        excute_result = {}
        excute_result['column_names'] = [col[0] for col in mycursor.description]
        excute_result['rows'] = mycursor.fetchall()
    else :
        excute_result = mycursor.fetchall()

    # MySQL 연결 종료
    mycursor.close()
    mydb.close()

    return excute_result

@router.get("", response_class=HTMLResponse)
async def search_vm(request: Request, vm_name: str = ""):
    db_info = tools.readAppInfo()
    
    if not vm_name == "":
        query_result = db_query("SELECT * FROM vm_list where vm_name like \'%" + vm_name + "%\'", 'search_vm')
    else:
        query_result = db_query("SELECT * FROM vm_list", 'search_vm')

    # 쿼리 결과 출력
    title = query_result['column_names']
    
    vm_list = []
    for x in query_result['rows']:
        individual_vm = []
        for i, value in enumerate(x):
            if i == 0:
                individual_vm.append(str(value[:-4]))
            elif i == 5:
                #자동 종료 예외 vm의 경우 exception으로 출력되도록 수정
                result_except_value = tools.check_except_auto_shutdown(value, x[0], db_info['ignore_vm'])
                individual_vm.append(str(result_except_value))
            else:
                individual_vm.append(str(value))
        vm_list.append(individual_vm)

    return templates.TemplateResponse("all_vm.html", {"request": request, "title": title, "vm_list": vm_list})

@router.get("/server_status", response_class=HTMLResponse)
async def server_status(request: Request):

    # grafana로 dashborad 변경
    # server_status = db_query('SELECT * FROM vm_server')

    # #데이터 조회
    # server_list = {}
    # for x in server_status:
    #     server_ip = ""
    #     individual_server = []
    #     for i, value in enumerate(x):
    #         if i == 0:
    #             server_ip = str(value)
    #         else:
    #             individual_server.append(int(value))
    #     server_list[server_ip] = individual_server 

    # # x축 데이터 생성
    # x = ["cpu", "memory", "disk"]

    # # 플로팅 대시보드 생성
    # fig = make_subplots(rows=1, cols=2, subplot_titles=("200 server", "203 server"))
    # fig.add_trace(go.Bar(x=x, y=server_list['172.29.100.200'], name='first_server'), row=1, col=1)
    # fig.add_trace(go.Bar(x=x, y=server_list['172.29.100.203'], name='second_server'), row=1, col=2)
    
    # # 레이아웃 설정
    # fig.update_layout(title='Server Status')
    # fig.update_yaxes(range=[0, 100])

    # 템플릿 렌더링
    return templates.TemplateResponse("server_status.html")

@router.put("/on_off", response_class=PlainTextResponse)
async def on_off_vm(body: models.VmOperBody):
    
    if not bool(body):
        return 'fail oper because empty property'
    
    # vm 전원 명령에 필요한 변수
    vm_id = body.vm_id
    vm_host = body.vm_host
    oper = body.oper
    
    # socket 정보를 app.conf 파일에서 read
    info_socket = tools.readAppInfo()
    vm_pass = info_socket['server_pass']
    socket_server = info_socket['socket_server']

    send_oper_result = await tools.send_socket_message(vm_id, vm_host, oper, vm_pass, socket_server)

    return send_oper_result

@router.get("/check_power")
def check_vm_powered(vm_id: str, vm_host: str):

    vm_power_status = db_query(f"select vm_powered, vm_boot_time from vm_list where vm_host_server = '{vm_host}' and vm_idx = '{vm_id}'")

    return {'powered': vm_power_status[0][0], 'boot_time': vm_power_status[0][1]}

@router.get("/vmrc", response_class=FileResponse)
async def get_vmrc_file():

    exe_file_path = './asset/VMware-VMRC-12.0.4-21740317.exe'

    return FileResponse(exe_file_path, filename='vmrc.exe')

@router.get("/asset/{image_name}", response_class=FileResponse)
async def get_image_file(image_name: str):
    image_file_path = f'./asset/{image_name}'

    return FileResponse(image_file_path, media_type = 'img/png')