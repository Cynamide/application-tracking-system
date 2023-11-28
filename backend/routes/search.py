from flask import Request,jsonify
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd

def searchRoute(request: Request):
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
    chromeOptions = Options()
    # chrome_options.add_argument("--no-sandbox") # linux only
    chromeOptions.add_argument("--headless")
    user_agent = (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/71.0.3578.98 Safari/537.36 "
    )
    chromeOptions.add_argument(f"user-agent={user_agent}")
    driver = webdriver.Chrome(
        ChromeDriverManager().install(), chrome_options=chromeOptions
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


