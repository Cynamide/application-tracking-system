from flask import Flask, jsonify, request, send_file
from flask_mongoengine import MongoEngine
from flask_cors import CORS, cross_origin
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from itertools import islice
from webdriver_manager.chrome import ChromeDriverManager
from bson.json_util import dumps
from datetime import datetime, timedelta
import yaml,uuid,io,os,openai,PyPDF2,hashlib,json, pandas as pd
from backend.utils.jsonResponse import jsonResponse
from backend.utils.tokenFromHeader import tokenFromHeader
from backend.utils.userIdFromtoken import getUseridFromtoken 
from backend.routes.login import loginRoute
from backend.routes.logout import logoutRoute
from backend.routes.signup import signupRoute
from backend.middleware.beforeRequest import beforeRequestMiddleware
from backend.routes.applications import getApplications

from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

existing_endpoints = ["/applications", "/resume","/recommend"]


def create_app():
    app = Flask(__name__)

    # make flask support CORS
    CORS(app)
    app.config["CORS_HEADERS"] = "Content-Type"

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
    @cross_origin()
    def health_check():
        return jsonResponse("Server up and running",200)

    @app.before_request
    def middleware():
        return beforeRequestMiddleware(request,existing_endpoints,Users) 

    def get_token_from_header():
        return tokenFromHeader(request)


    def get_userid_from_header():
        return getUseridFromtoken(request)

    @app.route("/users/signup", methods=["POST"])
    def sign_up():
        return signupRoute(request,Users)
       
    @app.route("/users/login", methods=["POST"])
    def login():
       return loginRoute(request,Users)


    @app.route("/users/logout", methods=["POST"])
    def logout():
        return logoutRoute(request ,Users)


    # search function
    # params:
    #   -keywords: string
    @app.route("/search")
    def search():
        """
        Searches the web and returns the job postings for the given search filters

        :return: JSON object with job results
        """
        keywords = (
            request.args.get("keywords")
            if request.args.get("keywords")
            else "random_test_keyword"
        )
        salary = request.args.get("salary") if request.args.get("salary") else ""
        keywords = keywords.replace(" ", "+")
        if keywords == "random_test_keyword":
            return json.dumps({"label": str("successful test search")})
        # create a url for a crawler to fetch job information
        if salary:
            url = (
                "https://www.google.com/search?q="
                + keywords
                + "%20salary%20"
                + salary
                + "&ibp=htl;jobs"
            )
        else:
            url = "https://www.google.com/search?q=" + keywords + "&ibp=htl;jobs"

        # webdriver can run the javascript and then render the page first.
        # This prevent websites don't provide Server-side rendering
        # leading to crawlers cannot fetch the page
        chrome_options = Options()
        # chrome_options.add_argument("--no-sandbox") # linux only
        chrome_options.add_argument("--headless")
        user_agent = (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/71.0.3578.98 Safari/537.36 "
        )
        chrome_options.add_argument(f"user-agent={user_agent}")
        driver = webdriver.Chrome(
            ChromeDriverManager().install(), chrome_options=chrome_options
        )
        driver.get(url)
        content = driver.page_source
        driver.close()
        soup = BeautifulSoup(content)

        # parsing searching results to DataFrame and return
        df = pd.DataFrame(columns=["jobTitle", "companyName", "location"])
        mydivs = soup.find_all("div", {"class": "PwjeAc"})
        for i, div in enumerate(mydivs):
            df.at[i, "jobTitle"] = div.find("div", {"class": "BjJfJf PUpOsf"}).text
            df.at[i, "companyName"] = div.find("div", {"class": "vNEEBe"}).text
            df.at[i, "location"] = div.find("div", {"class": "Qk80Jf"}).text
            df.at[i, "date"] = div.find_all("span", class_="SuWscb", limit=1)[0].text
        return jsonify(df.to_dict("records"))

    # get data from the CSV file for rendering root page
    @app.route("/applications", methods=["GET"])
    def get_data():
        return getApplications(request,Users,userId)


    @app.route("/applications", methods=["POST"])
    def add_application():
        """
        Add a new job application for the user

        :return: JSON object with status and message
        """
        try:
            userid = get_userid_from_header()
            try:
                request_data = json.loads(request.data)["application"]
                _ = request_data["jobTitle"]
                _ = request_data["companyName"]
            except:
                return jsonify({"error": "Missing fields in input"}), 400

            user = Users.objects(id=userid).first()
            current_application = {
                "id": get_new_application_id(userid),
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

    @app.route("/applications/<int:application_id>", methods=["PUT"])
    def update_application(application_id):
        """
        Updates the existing job application for the user

        :param application_id: Application id to be modified
        :return: JSON object with status and message
        """
        try:
            userid = get_userid_from_header()
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

    @app.route("/applications/<int:application_id>", methods=["DELETE"])
    def delete_application(application_id):
        """
        Deletes the given job application for the user

        :param application_id: Application id to be modified
        :return: JSON object with status and message
        """
        try:
            userid = get_userid_from_header()
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
        except:
            return jsonify({"error": "Internal server error"}), 500

    @app.route("/recommend", methods=["GET"])
    def recommend_resume():
        """
        Recommends a list of jobs in fortune 500 companies based on the user's resume using pdf parsing and ChatGPT
        """
        try:
            userid = get_userid_from_header()
            try:
                user = Users.objects(id=userid).first()
                if len(user.resume.read()) == 0:
                    raise FileNotFoundError
                else:
                    user.resume.seek(0)
            except:
                return jsonify({"error": "resume could not be found"}), 400
            
            pdf_content = io.BytesIO(user.resume.read())
            load_pdf = PyPDF2.PdfReader(pdf_content)
            page_content = load_pdf.pages[0].extract_text()
            prompt = "Analyse the resume below and recommend a list of 6 jobs for the user. All the comapanies should be among the fortune 500. The recommendations should be in a json format with company name, job title, and a link to the company career page.Only display the json. Json structure is {jobs: [{job_title:xx,company_name:xx,career_page:xx}]\n\nResume:\n\n" + page_content + "\n\nRecommendation JSON:"
            message = [ {"role": "system", "content": prompt} ]
            chat = openai.ChatCompletion.create( 
            model="gpt-3.5-turbo", messages=message
            ) 
            reply = chat.choices[0].message.content 
            return jsonify(reply), 200
        except:
            return jsonify({"error": "Internal server error"}), 500



    @app.route("/resume", methods=["POST"])
    def upload_resume():
        """
        Uploads resume file or updates an existing resume for the user

        :return: JSON object with status and message
        """
        try:
            userid = get_userid_from_header()
            try:
                file = request.files["file"].read()
            except:
                return jsonify({"error": "No resume file found in the input"}), 400

            user = Users.objects(id=userid).first()
            if not user.resume.read():
                # There is no file
                user.resume.put(file)
                user.save()
                return jsonify({"message": "resume successfully uploaded"}), 200
            else:
                # There is a file, we are replacing it
                user.resume.replace(file)
                user.save()
                return jsonify({"message": "resume successfully replaced"}), 200
        except Exception as e:
            print(e)
            return jsonify({"error": "Internal server error"}), 500

    @app.route("/resume", methods=["GET"])
    def get_resume():
        """
        Retrieves the resume file for the user

        :return: response with file
        """
        try:
            userid = get_userid_from_header()
            try:
                user = Users.objects(id=userid).first()
                if len(user.resume.read()) == 0:
                    raise FileNotFoundError
                else:
                    user.resume.seek(0)
            except:
                return jsonify({"error": "resume could not be found"}), 400

            response = send_file(
                user.resume,
                mimetype="application/pdf",
                attachment_filename="resume.pdf",
                as_attachment=True,
            )
            response.headers["x-filename"] = "resume.pdf"
            response.headers["Access-Control-Expose-Headers"] = "x-filename"
            return response, 200
        except:
            return jsonify({"error": "Internal server error"}), 500

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
