from flask import Request,jsonify
import json
from backend.utils.userIdFromtoken import getUseridFromtoken
from backend.utils.email import email
from tabulate import tabulate


def shareApplications(request:Request,Users):
    """
    the request body has the list of emails to share the 
    data with
    """
    data = json.loads(request.data)
    emails:list[str]= data["email"]
    applicationType:str= data["type"]

    userid = getUseridFromtoken(request)
    user = Users.objects(id=userid).first()
    applications= user["applications"]
    returnArray = [['Company','job title','Date','Location']]
    for app in applications:
        if app['status'] == applicationType:
            returnArray.append([app['companyName'],app['jobTitle'],app['date'],app['location']])
    returnString = tabulate(returnArray,headers="firstrow",tablefmt="html",numalign="right")
    email.send(','.join(emails),returnString)
    print(emails,applicationType)
    return jsonify({"status":"ok"}),200
