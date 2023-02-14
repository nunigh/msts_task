
from collections import OrderedDict
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from infra.steps import Step
from infra.flow import Flow
from infra.payload import TaskPayload

user_id = int 
_id = int 

@dataclass
class PersonalFormPayload(TaskPayload):
    first_name:str = None 
    last_name:str= None 
    email:str= None 

@dataclass
class IQTestPayload(TaskPayload):
    test_id:_id = None
    score: int = None
    timestamp:datetime = None
    def _has_passed(self)->bool:
        return self.score>75

@dataclass
class SchedInterviewPayload(TaskPayload):
    date:datetime = None

@dataclass
class PerformInterviewPayload(TaskPayload):
    interviewer_id:_id = None 
    date:datetime = None
    decision:bool = None
    def _has_passed(self)->bool:
        return self.decision

@dataclass 
class UploadIdPayload (TaskPayload):
    passort_number: int = None 
    timestamp:datetime = None

@dataclass
class PaymentPayload(TaskPayload):
    payment_id:_id = None  
    timestamp:datetime = None

@dataclass
class SignContractPayload(TaskPayload):
    timestamp:datetime = None  

@dataclass
class JoinSlackPayment(TaskPayload):
    email:str= None 
    timestamp:datetime = None


interviewStep = Step(tasks={
    "interview_sched":SchedInterviewPayload, 
    "interview_perform":PerformInterviewPayload })
IqTestStep = Step (tasks={
    "iq_test":IQTestPayload})
signContractStep = Step (tasks={
    "upload_id_doc":UploadIdPayload,
    "sign_contract":SignContractPayload})
personalFormStep = Step(tasks=OrderedDict({
    "personal_form":PersonalFormPayload}))
paymentStep = Step(tasks=OrderedDict({
    "payment":PaymentPayload}))
joinSlackStep =Step (tasks={
    "join_slack":JoinSlackPayment})

enrollment_flow = Flow(OrderedDict({
    "personal_details_form":personalFormStep,
    "iq_test":  IqTestStep,
    "interview":interviewStep,
    "contract":signContractStep,
    "payment":  paymentStep,
    "slack":    joinSlackStep
        }))

