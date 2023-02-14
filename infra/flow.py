import logging
from typing import Optional, OrderedDict,Any, Tuple
from infra.tasks import BaseTask
from infra.payload import Status

class ResouceNotFoundException():
    pass

class Flow():
    steps: OrderedDict

    def __init__(self, steps:OrderedDict):
        self.steps= steps

    def getStatus(self)-> Status:
        step_statuses = [step.getStatus() for step in  self.steps.values()]
        if Status.REJECTED in step_statuses:
            return Status.REJECTED
        elif all(status==Status.ACCEPTED for status in step_statuses):
            return Status.ACCEPTED
        elif Status.IN_PROGRESS in step_statuses:
            return Status.IN_PROGRESS
        else: # should not reach here
            raise Exception ("Internal Error. could not dedcue status")


    def find_task(self,task_name:str)->BaseTask:
        steps_containing_task = {name:step for name,step in self.steps.items() if step.find_task(task_name)}
        if not steps_containing_task:
            logging.warning("No such task: {task_name}")
            return None
        if len(steps_containing_task)!=1:
            logging.warning("found {len(steps_containing_task)} matches for task {task_name}. steps:{steps_containing_task.keys()")
            return None
        else:
            return list(steps_containing_task.values())[0].find_task(task_name)

    def get_current_task(self)->Tuple[Optional[str],Optional[str]]:
        for step_name,step in self.steps.items():
            if step.getStatus()== Status.IN_PROGRESS:
                return step_name,step.get_current_task()
        return None,None

    def describe(self)->OrderedDict[str,Any]:
        flow_desc = OrderedDict()
        for step_name,step in self.steps.items():
            flow_desc[step_name]=OrderedDict()
            for task_name,task in step.tasks.items():
                flow_desc[step_name][task_name]=task.getStatus()
        res = {}
        res["required_tasks"]=flow_desc
        res["status"] = self.getStatus()
        res["current_task"]=self.get_current_task()
        return res

