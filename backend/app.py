from flask import Flask, request
from flask_mongoengine import MongoEngine
from flask_cors import CORS,cross_origin
import yaml
from backend.utils.jsonResponse import jsonResponse
from backend.routes.login import loginRoute
from backend.routes.logout import logoutRoute
from backend.routes.signup import signupRoute
from backend.middleware.beforeRequest import beforeRequestMiddleware
from backend.routes.applications import getApplications,addApplication,updateApplication,deleteApplication
from backend.routes.search import searchRoute
from backend.routes.recommend import recommendRoute 
from backend.routes.resume import getResumeRoute,uploadResumeRoute
from backend.routes.share import shareApplications
from dotenv import load_dotenv

load_dotenv()

existing_endpoints = ["applications", "resume","recommend"]


def create_app():
    app = Flask(__name__)

    # make flask support CORS
    CORS(app,origins=['*'],methods=['*'])

    @app.errorhandler(404)
    def page_not_found(e):
        return jsonResponse("Page not Found",404)

    @app.errorhandler(405)
    def page_not_allowed(e):
        return jsonResponse("Method not allowed",405)
   
    @app.errorhandler(500)
    def internal_server_error(e):
        print("error",e)
        return jsonResponse("server error",500)

    @app.route("/")
    def health_check():
        return jsonResponse("Server up and running",200)

    @app.before_request
    def middleware():
        returnValue = beforeRequestMiddleware(request,existing_endpoints,Users)
        print(returnValue, "checking return value here")
        return returnValue

    @app.route("/users/signup", methods=["POST"])
    @cross_origin()
    def sign_up():
        return signupRoute(request,Users)
       
    @app.route("/users/login", methods=["POST"])
    @cross_origin()
    def login():
       return loginRoute(request,Users)


    @app.route("/users/logout", methods=["POST"])
    def logout():
        return logoutRoute(request ,Users)

    # get data from the CSV file for rendering root page
    @app.route("/application-tracking-system/applications", methods=["GET"])
    @app.route("/applications",methods=["GET"])
    def get_data():
        return getApplications(request,Users)


    @app.route("/applications", methods=["POST"])
    def add_application():
        return addApplication(request,Users)

    @app.route("/application-tracking-system/applications/<int:application_id>", methods=["PUT"])
    def update_application(application_id):
        return updateApplication(request,application_id,Users)
        

    @app.route("/application-tracking-system/applications/<int:application_id>", methods=["DELETE"])
    def delete_application(application_id):
        return deleteApplication(request,application_id,Users)

    @app.route("/search")
    def search():
        return searchRoute(request)
          
    @app.route("/recommend", methods=["GET"])
    def recommend_resume():
        return recommendRoute(request,Users)
        
    @app.route("/resume", methods=["POST"])
    def upload_resume():
        return uploadResumeRoute(request,Users)

    @app.route("/resume", methods=["GET"])
    def get_resume():
        return getResumeRoute(request,Users)
    
    @app.route("/share",methods=["POST"])
    def share_applications():
        return shareApplications(request,Users)
    
    return app


app = create_app()
with open("application.yml") as f:
    info = yaml.load(f, Loader=yaml.FullLoader)
    username = info["username"]
    password = info["password"]
    app.config["MONGODB_SETTINGS"] = {
        "db": "sefall23",
        "host":f"mongodb+srv://{username}:{password}@sefall23proj3.wwrtycq.mongodb.net/"
    }
    print(app.config["MONGODB_SETTINGS"],"mongodb settings ")

db = MongoEngine()
db.init_app(app)


class Users(db.Document):
    """
    Users class. Holds full name, username, password, as well as applications and resumes
    """

    id = db.IntField(primary_key=True)
    fullName = db.StringField()
    username = db.StringField()
    password = db.StringField()
    authTokens = db.ListField()
    applications = db.ListField()
    resume = db.FileField()

    def to_json(self):
        """
        Returns the user details in JSON object

        :return: JSON object
        """
        return {"id": self.id, "fullName": self.fullName, "username": self.username}


if __name__ == "__main__":
    app.run(debug=True)
