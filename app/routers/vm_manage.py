from fastapi import Request
from fastapi.responses import HTMLResponse
import mysql.connector
import tools
from fastapi.templating import Jinja2Templates
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from fastapi import APIRouter

router = APIRouter(prefix='/vm_list')

#jinja templates
templates = Jinja2Templates(directory="templates")

@router.get("", response_class=HTMLResponse)
async def search_vm(request: Request, vm_name: str = ""):
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
    if not vm_name == "":
        mycursor.execute("SELECT * FROM vm_list where vm_name like \'%" + vm_name + "%\'")
    else:
        mycursor.execute("SELECT * FROM vm_list")

    # 쿼리 결과 출력
    title = []
    vm_list = []
    for x in mycursor.description:
        title.append(str(x[0]))
    for x in mycursor:
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

    # MySQL 연결 종료
    mycursor.close()
    mydb.close()

    return templates.TemplateResponse("all_vm.html", {"request": request, "title": title, "vm_list": vm_list})

@router.get("/server_status", response_class=HTMLResponse)
async def server_status(request: Request):
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
    mycursor.execute("SELECT * FROM vm_server")

    #데이터 조회
    server_list = {}
    for x in mycursor:
        server_ip = ""
        individual_server = []
        for i, value in enumerate(x):
            if i == 0:
                server_ip = str(value)
            else:
                individual_server.append(int(value))
        server_list[server_ip] = individual_server 

    # x축 데이터 생성
    x = ["cpu", "memory", "disk"]

    # 플로팅 대시보드 생성
    fig = make_subplots(rows=1, cols=2, subplot_titles=("200 server", "203 server"))
    fig.add_trace(go.Bar(x=x, y=server_list['172.29.100.200'], name='first_server'), row=1, col=1)
    fig.add_trace(go.Bar(x=x, y=server_list['172.29.100.203'], name='second_server'), row=1, col=2)
    
    # 레이아웃 설정
    fig.update_layout(title='Server Status')
    fig.update_yaxes(range=[0, 100])

    # 템플릿 렌더링
    return templates.TemplateResponse("server_status.html", {"request": request, "dashboard": fig.to_html(full_html=False)})