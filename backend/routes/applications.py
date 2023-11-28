from flask import Request, jsonify
from backend.utils.userIdFromtoken import getUseridFromtoken
from backend.utils.dbUtils import  get_new_application_id
import json 

def getApplications(request:Request, Users):
    """
    Gets user's applications data from the database

    :return: JSON object with application data
    """
    try:
        userid = getUseridFromtoken(request)
        user = Users.objects(id=userid).first()
        applications = user["applications"]
        return jsonify(applications)
    except:
        return jsonify({"error": "Internal server error"}), 500




def addApplication(request: Request,Users):
    """
    Add a new job application for the user

    :return: JSON object with status and message
    """
    try:
        userid = getUseridFromtoken(request)
        try:
            request_data = json.loads(request.data)["application"]
            _ = request_data["jobTitle"]
            _ = request_data["companyName"]
        except:
            return jsonify({"error": "Missing fields in input"}), 400

        user = Users.objects(id=userid).first()
        current_application = {
            "id": get_new_application_id(userid,Users),
            "jobTitle": request_data["jobTitle"],
            "companyName": request_data["companyName"],
            "date": request_data.get("date"),
            "jobLink": request_data.get("jobLink"),
            "location": request_data.get("location"),
            "status": request_data.get("status", "1"),
        }
        applications = user["applications"] + [current_application]

        user.update(applications=applications)
        return jsonify(current_application), 200
    except:
        return jsonify({"error": "Internal server error"}), 500



def updateApplication(request: Request, application_id:str,Users):
    """
    Updates the existing job application for the user

    :param application_id: Application id to be modified
    :return: JSON object with status and message
    """
    try:
        userid = getUseridFromtoken(request)
        try:
            request_data = json.loads(request.data)["application"]
        except:
            return jsonify({"error": "No fields found in input"}), 400

        user = Users.objects(id=userid).first()
        current_applications = user["applications"]

        if len(current_applications) == 0:
            return jsonify({"error": "No applications found"}), 400
        else:
            updated_applications = []
            app_to_update = None
            application_updated_flag = False
            for application in current_applications:
                if application["id"] == application_id:
                    app_to_update = application
                    application_updated_flag = True
                    for key, value in request_data.items():
                        application[key] = value
                updated_applications += [application]
            if not application_updated_flag:
                return jsonify({"error": "Application not found"}), 400
            user.update(applications=updated_applications)

        return jsonify(app_to_update), 200
    except:
        return jsonify({"error": "Internal server error"}), 500

def deleteApplication(request:Request, application_id:str, Users):
    """
    Deletes the given job application for the user

    :param application_id: Application id to be modified
    :return: JSON object with status and message
    """
    try:
        userid = getUseridFromtoken(request)
        user = Users.objects(id=userid).first()

        current_applications = user["applications"]

        application_deleted_flag = False
        updated_applications = []
        app_to_delete = None
        for application in current_applications:
            if application["id"] != application_id:
                updated_applications += [application]
            else:
                app_to_delete = application
                application_deleted_flag = True

        if not application_deleted_flag:
            return jsonify({"error": "Application not found"}), 400
        user.update(applications=updated_applications)
        return jsonify(app_to_delete), 200
    except exception as error:
        print(error)
        return jsonify({"error": "Internal server error"}), 500


