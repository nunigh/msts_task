import json
import logging
import traceback
from flask import Flask,request
from infra.payload import Status,PayloadValidationError
from user_enrollment_mgr import UserEnrollmentMgr

app = Flask("Enrollment_Flow")


@app.route('/user/<user_id>/flow', methods=['GET'])
def get_user_flow(user_id):
    flow = UserEnrollmentMgr.get_flow(user_id)
    if flow:
        return json.dumps(flow.describe()),200
    else:
        return f"No such user_id: {user_id}",401

@app.route('/user/<user_id>/task/current', methods=['GET'])
def get_current_task(user_id):
    flow = UserEnrollmentMgr.get_flow(user_id)
    if not flow:
        return f"No such user_id: {user_id}",401
    if flow.getStatus() != Status.IN_PROGRESS:
        return "-1",200 # flow already completed
    step,task = flow.get_current_task()
    return json.dumps({"step":step,"task":task}),200
    

@app.route('/user/<user_id>/task/<task_name>', methods=['GET'])
def get_task(user_id, task_name):
    flow = UserEnrollmentMgr.get_flow(user_id)
    if not flow:
        return f"No such user_id: {user_id}",401
    task = flow.find_task(task_name)
    if not task:
        return f"No such task: {task_name} for user: {user_id}",401
    return json.dumps(task.get()),200

@app.route('/user/<user_id>/task/<task_name>', methods=['POST'])
def update_task(user_id, task_name):
    # ideally all of this logic is part of UserEnrollmentMgr (and same for rest of methods)
    # i.e: UserEnrollmentMgr.update_task(user_id, task_name, request.json)
    flow = UserEnrollmentMgr.get_flow(user_id)
    if not flow:
        return f"No such user_id: {user_id}",401
    task = flow.find_task(task_name)
    if not task:
        return f"No such task: {task_name} for user: {user_id}",401
    if not request:
        return "Missing Payload" , 400
    payload = request.json
    try:
        task.update(**payload)
        return "OK",200
    except (TypeError,PayloadValidationError) as ex: 
        return str(ex), 400 # not ideal
    except Exception as ex:
        logging.error(ex)
        traceback.print_exc()
        return "Internal Error",500

@app.route('/user/<user_id>/status', methods=['GET'])
def get_status(user_id):
    flow = UserEnrollmentMgr.get_flow(user_id)
    if flow:
        return flow.getStatus(),200
    else:
        return f"No such user_id: {user_id}",401

@app.route('/start_enroll', methods=['POST'])
def start_enroll():
    user_id = request.form.get('user_id')
    if not user_id:
        return "Missing Required Paramater user_id", 400
    if UserEnrollmentMgr.get_flow(user_id):
        return f"user_id {user_id} already exists.",400
    else:
        UserEnrollmentMgr.add_user(user_id)
        return '',204