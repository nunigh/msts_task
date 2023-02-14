from collections import OrderedDict
from typing import Optional
from infra.tasks import BaseTask, Status
from infra.payload import Status

class Step():
    def __init__(self, tasks:OrderedDict):
        self.tasks:BaseTask = OrderedDict((name,BaseTask(payload)) for name,payload in tasks.items())
    
    def getStatus(self)->bool:
        tasks_statuses = [task.getStatus() for _name, task in self.tasks.items()]
        if all([status==Status.ACCEPTED for status in tasks_statuses]):
            return Status.ACCEPTED
        if any(status == Status.REJECTED for status in tasks_statuses):
            return Status.REJECTED
        elif any(status == Status.IN_PROGRESS for status in tasks_statuses):
            return Status.IN_PROGRESS
        else: # should not reach here
            raise Exception ("Internal Error. could not dedcue status")
    
    def find_task(self, task_name:str)->Optional[BaseTask]:
        return self.tasks.get(task_name)

    def get_current_task(self)->Optional[str]:
        for name,task in self.tasks.items():
            if task.getStatus()==Status.IN_PROGRESS:
                return name
        return None
