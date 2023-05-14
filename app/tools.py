import re

#app.conf 파일에 있는 db정보를 가져오는 함수
def readAppInfo() -> dict:
    """
    app.conf 파일에서 동작에 필요한 설정들을 가져온다.
    """
    app_info = {}
    #정규식을 이용하여 필요한 정보만 dictionary array에 저장하기 위해 정규식 설정
    db_match = re.compile('^db|^limit')
    server_match = re.compile('^server|ignore')
    f = open('/etc/app.conf')
    readText = f.readlines()
    f.close()

    for line in readText:
        #db나 boot의 경우 string으로 ignore, serverip는 list로 저장해야 함
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
