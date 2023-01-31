import os

import requests

API_PORT = os.getenv("API_PORT", default=8000)

api_url = f"http://0.0.0.0:{API_PORT}"

author_url = f"{api_url}/v1/author/"
category_url = f"{api_url}/v1/category/"
tag_url = f"{api_url}/v1/tag/"
book_url = f"{api_url}/v1/book/"

requests.post(author_url, json={"name": "author_1"})
requests.post(author_url, json={"name": "author_2"})
authors = requests.get(author_url)
author_ids = [item["id"] for item in authors.json()]

requests.post(category_url, json={"name": "category_1"})
requests.post(category_url, json={"name": "category_2"})
categories = requests.get(category_url)
category_ids = [item["id"] for item in categories.json()]

requests.post(tag_url, json={"name": "tag_1"})
requests.post(tag_url, json={"name": "tag_2"})
tags = requests.get(tag_url)
tags = sorted([item["name"] for item in tags.json()])

book_1 = {
    "name": "book_1",
    "category_id": category_ids[0],
    "author_id": author_ids[0],
    "tags": tags
}

book_2 = {
    "name": "book_2",
    "category_id": category_ids[1],
    "author_id": author_ids[0],
    "tags": [tags[0]]
}

book_3 = {
    "name": "book_3",
    "category_id": category_ids[1],
    "author_id": author_ids[1],
    "tags": [tags[1]]
}

requests.post(book_url, json=book_1)
requests.post(book_url, json=book_2)
requests.post(book_url, json=book_3)
