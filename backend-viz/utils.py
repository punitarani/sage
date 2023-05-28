import openai
import requests
import json
import os

openai.api_key = os.getenv("OPENAI_API_KEY")
gist_url="https://api.github.com/gists"
gist_headers = {'Authorization': f'token {os.getenv("API_TOKEN")}'}
gist_params={'scope':'gist'}

def str_to_embeddings(paragraph: str):
    response = openai.Embedding.create(
    input=paragraph,
    model="text-embedding-ada-002"
    )
    embeddings = response['data'][0]['embedding'] 
    return embeddings

def visualize(embeddings_vectors, metadataObj):
    feature_vecs = ""
    for embeddings_vector in embeddings_vectors:
        feature_vecs += "{}\n".format("\t".join([str(x) for x in embeddings_vector]))

    
    metadata = ("{}\t{}\t{}\t{}\t{}\t{}\n".format("Title", "URL", "Summary", "Authors", "DOI", "Date"))
    for i, paragraph in enumerate(metadataObj):
        metadata += "{}\t{}\t{}\t{}\t{}\t{}\n".format(paragraph.name, paragraph.url, paragraph.summary, paragraph.authors, paragraph.doi, paragraph.date)
        
    metadata_gist = upload_gist("metadata.tsv", metadata, "Metadata for vector visualization")
    feature_vecs_gist = upload_gist("feature_vec.tsv", feature_vecs, "Feature vectors for vector visualization")

    config = {
    'embeddings': [
        {
            'tensorName': 'embeddings',
            'tensorShape': [len(embeddings_vectors), len(embeddings_vectors[0])],
            'tensorPath': feature_vecs_gist,
            'metadataPath': metadata_gist,
        }
    ]   
    }
    config_gist = upload_gist("config.json", json.dumps(config), "Config for vector visualization")
    return f'https://projector.tensorflow.org/?config={config_gist}'

def upload_gist(title, content, description):

    payload={"description":description,"public":True,"files":{title:{"content":content}}}
    res=requests.post(gist_url,headers=gist_headers,params=gist_params,data=json.dumps(payload))
    res = res.json()
    return res['files'][title]['raw_url']