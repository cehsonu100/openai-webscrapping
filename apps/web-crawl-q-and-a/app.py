from flask import Flask, request
from crawler import crawl_single_site
from crawler_helper import get_domain_name

from openai_embedding import answer_question
from web_qa import create_openai_embedding, write_txt_into_csv

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello, World! I am a Web Crawler and with help of ChatGPT I will answer to your Questions from your sites."


@app.route('/crawl', methods=['GET', 'POST'])
def crawl():
    try:
      data = request.get_json()
      url = data["full_url"]
      local_domain = get_domain_name(url)
      crawl_single_site(url)
      write_txt_into_csv(local_domain)
      create_openai_embedding(local_domain)
      return {"result": "Crawling done", "status": 200}
    except Exception as e:
      print(e)
      return {"result": "Crawling failed", "status": 500}


@app.route('/answer', methods=['GET', 'POST'])
def answer():
    try:
        data = request.get_json()
        question = data["question"]
        domain = data["domain"]
        result = {
            "answer": answer_question(domain=domain, question=question),
            "status": 200
        }
        return result
    except Exception as e:
        print(e)
        result = {
            "answer": "",
            "status": 500,
            "error": str(e)

        }
        return result
