from pydantic import BaseModel

class instanceOperBody(BaseModel):
    oper: str
    instanceId: str

class VmOperBody(BaseModel):
    oper: str
    vm_id: str
    vm_host: str

    def __bool__(self):
        return bool(self.oper and self.vm_host and self.vm_id)

class TagChangeData(BaseModel):
    instance_id: str
    tag_key: str
    state: str