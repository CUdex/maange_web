from fastapi.responses import PlainTextResponse
from fastapi import APIRouter
import os

router = APIRouter(prefix='/test')

@router.get("", response_class=PlainTextResponse)
async def return_version():


    version = os.environ.get('POD_VERSION')
    version = version.split('=')

    host_name = os.environ.get('HOSTNAME')
    result = f"""-----------------------------------------------
container name: {host_name}
container version: {version[1]}
-----------------------------------------------"""
    
    return result