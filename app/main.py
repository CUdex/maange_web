from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import mysql.connector
import tools
from fastapi.templating import Jinja2Templates
import uvicorn

# fastapi 객체 생성
app = FastAPI()
#jinja templates
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):

    return templates.TemplateResponse("main.html", {"request": request})

@app.get("/vm_list", response_class=HTMLResponse)
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

if __name__=='__main__':
    uvicorn.run(app, host='0.0.0.0', port = 80)