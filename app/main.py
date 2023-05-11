from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import mysql.connector
import tools

# fastapi 객체 생성
app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def read_root():

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
    mycursor.execute("SELECT * FROM vm_list")

    # 쿼리 결과 출력
    result = "<table class='styled-table'>"
    result += "<thead>"
    result += "<tr>"
    for x in mycursor.description:
        result += "<th>" + str(x[0]) + "</th>"
    result += "</tr>"
    result += "</thead>"
    result += "<tbody>"
    for x in mycursor:
        result += "<tr>"
        for i, value in enumerate(x):
            if i == 0:
                result += "<td>" + str(value[:-4]) + "</td>"
            elif i == 5:
                #자동 종료 예외 vm의 경우 exception으로 출력되도록 수정
                result_except_value = tools.check_except_auto_shutdown(value, x[0], db_info['ignore_vm'])
                result += "<td>" + str(result_except_value) + "</td>"
            else:
                result += "<td>" + str(value) + "</td>"
        result += "</tr>"
    result += "</tbody>"
    result += "</table>"

    
    # MySQL 연결 종료
    mycursor.close()
    mydb.close()

    style = """
        <style>
            .styled-table {
                border-collapse: collapse;
                margin: 25px 0;
                font-size: 0.9em;
                font-family: sans-serif;
                min-width: 400px;
                box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
            }

            .styled-table thead tr {
                background-color: #009879;
                color: #ffffff;
                text-align: center;
            }

            .styled-table th,
            .styled-table td {
                padding: 12px 15px;
            }

            .styled-table tbody tr {
                border-bottom: 1px solid #dddddd;
            }

            .styled-table tbody tr:nth-of-type(even) {
                background-color: #f3f3f3;
            }

            .styled-table tbody tr:last-of-type {
                border-bottom: 2px solid #009879;
            }

            .styled-table tbody td {
                text-align: center;
            }
        </style>
    """

    return style + result

