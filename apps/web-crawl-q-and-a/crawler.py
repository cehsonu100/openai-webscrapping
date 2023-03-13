from collections import deque
from urllib.parse import urlparse
import os
from crawler_helper import extract_all_text, get_domain_hyperlinks, get_domain_name


def crawl_single_site(url): 
    # Parse the URL and get the domain
    local_domain = get_domain_name(url)
    create_folders_if_not_exists(local_domain)
    # Save text from the url to a <url>.txt file
    with open('text/'+local_domain+'/'+url[8:].replace("/", "_") + ".txt", "w", encoding="UTF-8") as f:

        text = extract_all_text(url)

        # If the crawler gets to a page that requires JavaScript, it will stop the crawl
        if ("You need to enable JavaScript to run this app." in text):
            print("Unable to parse page " + url + " due to JavaScript being required")
        
        f.write(text)


def crawl_entire_site_bfs(url, max_urls_to_crawl=100, max_depth=100):
    local_domain = get_domain_name(url)
    create_folders_if_not_exists(local_domain)
    queue = deque([url])
    visited = set([url])

    # Keep track of the depth of the current URL
    depth = 0
    num_urls_crawled = 0

    while queue and num_urls_crawled < max_urls_to_crawl:

        url = queue.pop()
        print(url)

        # Save text from the url to a <url>.txt file
        with open('text/'+local_domain+'/'+url[8:].replace("/", "_") + ".txt", "w", encoding="UTF-8") as f:

            text = extract_all_text(url)
            # If the crawler gets to a page that requires JavaScript, it will stop the crawl
            if ("You need to enable JavaScript to run this app." in text):
                print("Unable to parse page " + url + " due to JavaScript being required")
            
            f.write(text)

        # Get the hyperlinks from the URL and add them to the queue
        for link in get_domain_hyperlinks(local_domain, url):
            if link not in visited:
                queue.append(link)
                visited.add(link)

        num_urls_crawled += 1

def create_folders_if_not_exists(local_domain):
    # Create a directory to store the text files
    if not os.path.exists("text/"):
            os.mkdir("text/")

    if not os.path.exists("text/"+local_domain+"/"):
            os.mkdir("text/" + local_domain + "/")

    # Create a directory to store the csv files
    if not os.path.exists("processed/"):
            os.mkdir("processed/")
    if not os.path.exists("processed/"+local_domain+"/"):
            os.mkdir("processed/"+local_domain+"/")
