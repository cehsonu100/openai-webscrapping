import json
from openai_embedding import answer_question

from web_qa import create_openai_embedding

from web_qa import write_txt_into_csv

def lambda_handler(event, context):
    write_txt_into_csv()
    create_openai_embedding()

    print(answer_question(question="Minimum requirements for admission?", debug=False))
    print(answer_question(question="What is the requirement to complete 4 years bachelor course?"))
    print(answer_question(question="How to SUBMIT OFFICIAL TRANSCRIPTS?"))
    return {
        'statusCode': 200,
        'body': json.dumps(answer_question(question="How to SUBMIT OFFICIAL TRANSCRIPTS?"))
    }
