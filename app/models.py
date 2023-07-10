from pydantic import BaseModel

class instanceOperBody(BaseModel):
    oper: str
    instanceId: str