import os
import pandas as pd
import tiktoken
import openai
from openai.embeddings_utils import distances_from_embeddings
import numpy as np
from openai.embeddings_utils import distances_from_embeddings, cosine_similarity
from crawler import crawl_single_site
from openai_embedding import answer_question, create_context, split_into_many

openai.api_key = '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'
max_tokens = 500
# # Regex pattern to match a URL
# HTTP_URL_PATTERN = r'^http[s]*://.+'

# Define root domain to crawl
# domain = "www.fullerton.edu"
# full_url = "https://www.fullerton.edu/ecs/future/graduate-admission.php"


# crawl_single_site(full_url)
# crawl_single_site("http://www.fullerton.edu/graduate/admissions/applying.php")


def remove_newlines(serie):
    serie = serie.str.replace('\n', ' ')
    serie = serie.str.replace('\\n', ' ')
    serie = serie.str.replace('  ', ' ')
    serie = serie.str.replace('  ', ' ')
    return serie


def write_txt_into_csv(domain):
    texts=[]

    # Get all the text files in the text directory
    for file in os.listdir("text/" + domain + "/"):

        with open("text/" + domain + "/" + file, "r", encoding="UTF-8") as f:
            text = f.read()

            # Omit the first 11 lines and the last 4 lines, then replace -, _, and #update with spaces.
            texts.append((file[11:-4].replace('-',' ').replace('_', ' ').replace('#update',''), text))

    # Create a dataframe from the list of texts
    df = pd.DataFrame(texts, columns = ['fname', 'text'])

    # Set the text column to be the raw text with the newlines removed
    df['text'] = df.fname + ". " + remove_newlines(df.text)
    df.to_csv('processed/' + domain + '/scraped.csv')
    df.head()


def create_openai_embedding(domain):
    # Load the cl100k_base tokenizer which is designed to work with the ada-002 model
    tokenizer = tiktoken.get_encoding("cl100k_base")

    df = pd.read_csv('processed/' + domain + '/scraped.csv', index_col=0)
    df.columns = ['title', 'text']

    # Tokenize the text and save the number of tokens to a new column
    df['n_tokens'] = df.text.apply(lambda x: len(tokenizer.encode(x)))

    # Visualize the distribution of the number of tokens per row using a histogram
    # df.n_tokens.hist()

    shortened = []

    # Loop through the dataframe
    for row in df.iterrows():

        # If the text is None, go to the next row
        if row[1]['text'] is None:
            continue

        # If the number of tokens is greater than the max number of tokens, split the text into chunks
        if row[1]['n_tokens'] > max_tokens:
            shortened += split_into_many(row[1]['text'], tokenizer, max_tokens)
        
        # Otherwise, add the text to the list of shortened texts
        else:
            shortened.append( row[1]['text'] )

    df = pd.DataFrame(shortened, columns = ['text'])
    df['n_tokens'] = df.text.apply(lambda x: len(tokenizer.encode(x)))
    # df.n_tokens.hist()

    df['embeddings'] = df.text.apply(lambda x: openai.Embedding.create(input=x, engine='text-embedding-ada-002')['data'][0]['embedding'])
    df.to_csv('processed/' + domain + '/embeddings.csv')
    df.head()

# write_txt_into_csv()
# create_openai_embedding()

# print(answer_question(question="Minimum requirements for admission?", debug=False))
# print(answer_question(question="What is the requirement to complete 4 years bachelor course?"))
# print(answer_question(question="How to SUBMIT OFFICIAL TRANSCRIPTS?"))

