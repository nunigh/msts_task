
from dataclasses import dataclass, fields
from datetime import datetime
import logging
import traceback
from uuid import UUID
from enum import Enum

StudentId=UUID

class Status(str,Enum): 
    IN_PROGRESS="In Progress"
    ACCEPTED = "Accepted"
    REJECTED = "Rejected"

class PayloadValidationError(Exception):
    pass

@dataclass
class TaskPayload():
    status:Status = Status.IN_PROGRESS
    def __post_init__(self):
        self._validate()
        if not self._is_payload_completed():
            self.status = Status.IN_PROGRESS
        else:
            self.status = Status.ACCEPTED if self._has_passed() else Status.REJECTED
    
    def _validate(self)->None:
    # those are only partial vaildatoins. ideally need to valiate email, ID's ect
        for field in fields(self):
            attr = getattr(self, field.name)
            if attr is None:
                continue
            if field.type==datetime:
                attr = str2time(attr)
            if not isinstance(attr, field.type):
                 msg = f"Field {field.name} is of type {type(attr)}, should be {field.type}"
                 raise PayloadValidationError(msg)

    def _has_passed(self)->bool:
        return True

    def _is_payload_completed(self)->bool:
        all_fields = fields(self)
        all_values = [getattr(self,field.name)!=None for field in all_fields]
        return all (all_values)

def str2time(s_time:str)->datetime:
    format= "%Y-%m-%d %H:%M"
    try:
        return datetime.strptime(s_time, format)
    except Exception as ex:
        logging.error(ex)
        traceback.print_exc()
        raise PayloadValidationError(f"invalid date variable. date should be at format:{format}")
