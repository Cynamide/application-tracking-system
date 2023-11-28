from flask import Request,jsonify
from backend.utils.userIdFromtoken import getUseridFromtoken
import io,PyPDF2,os,openai

openai.api_key = os.getenv("OPENAI_API_KEY")
def recommendRoute(request: Request,Users):
    """
    Recommends a list of jobs in fortune 500 companies based on the user's resume using pdf parsing and ChatGPT
    """
    try:
        userid = getUseridFromtoken(request)
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



