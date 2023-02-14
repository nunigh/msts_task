
from dataclasses import asdict
from infra.payload import  TaskPayload
from infra.payload import Status


class BaseTask():
    def __init__(self, payload_cls: TaskPayload):
        self.payload_cls = payload_cls
        self.payload_data = payload_cls()
    
    def getStatus(self)->Status:
        return self.payload_data.status

    def updatePayload(self, payload):
        self.payload_data = payload
    
    def update(self, *args,**kwargs):
        self.payload_data = self.payload_cls(*args,**kwargs)

    def get(self):
        return asdict(self.payload_data)

    def __str__(self):
        return f"Task({self.payload_cls}:{self.payload_data})"