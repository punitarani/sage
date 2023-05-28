from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


import dotenv
dotenv.load_dotenv()

import utils

app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

feature_vectors = []
metadata = []

class Page(BaseModel):
    name: str
    url: str
    summary: str
    authors: str
    doi: str
    date: str
    
class SearchQuery(BaseModel):
    searchText: str

@app.get("/")
def read_root():
    return {"status": "ok"}

@app.post("/add")
def add(page: Page):
    embeddings = utils.str_to_embeddings(page.summary)
    feature_vectors.append(embeddings)
    metadata.append(page)
    return {"status": "ok"}

@app.post("/add-multiple")
def add_multiple(pages: list[Page]):
    for page in pages:
        embeddings = utils.str_to_embeddings(page.summary)
        feature_vectors.append(embeddings)
        metadata.append(page)
    return {"status": "ok"}

@app.get("/visualize")
def visualize():
    url = utils.visualize(feature_vectors, metadata)
    print({"url": url})
    return {"url": url}

@app.post("/relatedPapers")
def find_related_papers(query: SearchQuery):
    print(query)
    return [
        {
            "name": "Paper 1",
            "url": "https://www.google.com",
        },
        {
            "name": "Paper 2",
            "url": "https://www.google.com",
        },
        {
            "name": "Paper 3",
            "url": "https://www.google.com",
        },
        {
            "name": "Paper 4",
            "url": "https://www.google.com",
        },
        {
            "name": "Paper 5",
            "url": "https://www.google.com",
        }
    ]
    
@app.post("/abstract")
def get_abstract(query: SearchQuery):
    print(query)
    return {
        'abstract': "This is the abstract for the paper: Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec euismod, nisl eget aliquam ultricies, nunc nisl aliquet nunc, vitae aliquam nisl nunc sit amet nunc. Donec euismod, nisl eget aliquam ultricies, nunc nisl aliquet nunc, vitae aliquam nisl nunc sit amet nunc. Donec euismod, nisl eget aliquam ultricies, nunc nisl aliquet nunc, vitae aliquam nisl nunc sit amet nunc. Donec euismod, nisl eget aliquam ultricies, nunc nisl aliquet nunc, vitae aliquam nisl nunc sit amet nunc."
    }
    
    