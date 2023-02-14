

from copy import deepcopy
from typing import Dict
from infra.flow import Flow
from flow_definition import enrollment_flow, user_id

user2flow: Dict[user_id,Flow] = {}

class UserEnrollmentMgr():
    @staticmethod
    def get_flow(user_id:user_id)->Flow:
        return user2flow.get(user_id)

    @staticmethod
    def add_user(user_id:user_id)->None:
        user2flow[user_id] = start_enrollment_flow()

    #ideally this class should handle the logic at app.py. 
    #i.e def update_task(user_id, task_name,payload)
    #           ...
    #   def get_status (user_id)
    #           ...

def start_enrollment_flow()->Flow:
    return deepcopy(enrollment_flow)