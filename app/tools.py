import re
import asyncio
import json

#app.conf 파일에 있는 db정보를 가져오는 함수
def readAppInfo() -> dict:
    """
    app.conf 파일에서 동작에 필요한 설정들을 가져온다.
    """
    app_info = {}
    db_match = re.compile('^db|^limit|^socket|^server_pass')
    server_match = re.compile('^server|^ignore')
    f = open('/etc/app.conf')
    readText = f.readlines()
    f.close()

    for line in readText:
        #db나 boot 등의 경우 string으로 ignore, serverip는 list로 저장해야 함
        if db_match.match(line):
            split_text = line.split("=")
            app_info[split_text[0]] = split_text[1].strip('\n')

        elif server_match.match(line):
            split_text = line.split("=")
            server_ip = split_text[1].split(',')
            app_info[split_text[0]] = server_ip
            app_info[split_text[0]][-1] = app_info[split_text[0]][-1].strip('\n')

    return app_info

#except된 vm의 경우 boottime이 exception으로 나오도록 처리
def check_except_auto_shutdown(boot_time, vm_name, except_list):
    return "exception" if vm_name in except_list else boot_time

#socket client 함수
async def send_socket_message(vm_id, server, oper, server_pass, socket_server):
    reader, writer = await asyncio.open_connection(
        socket_server, 20000)
    
    message = {'vm_id': vm_id, 'server': server, 'oper': oper, 'server_pass': server_pass}

    writer.write(json.dumps(message).encode())
    await writer.drain()

    data = await reader.read(1024)
    response = data.decode()
    print(f'Received from server: {response}')

    writer.close()
    await writer.wait_closed()

    return response