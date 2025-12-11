from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pickle 
import pandas as pd
import numpy as np
import uvicorn
import gdown
import os

app=FastAPI()

similarity_url = 'https://drive.google.com/uc?export=download&id=1yqE-7lNvtBO7m0zuvO81Ec8PQpNnoj4c'
movies_url = 'https://drive.google.com/uc?export=download&id=1zT4we4qZo-Kih3YuRtTZfK5_nElbfbqM'

similarity_file = 'similarity.pkl'
movies_file = 'movies.pkl'

# Download files if they don't exist
if not os.path.exists(similarity_file):
    gdown.download(similarity_url, similarity_file, quiet=False)

if not os.path.exists(movies_file):
    gdown.download(movies_url, movies_file, quiet=False)


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*']
)

movies=pd.read_pickle('movies.pkl')


with open('similarity.pkl','rb') as f:
    similarity=pickle.load(f)



print("Similarity matrix loaded successfully!")

def get_recommendation(title):
    index=movies[movies['title'].str.contains(title, case=False, na=False)].index[0]

    scores=list(enumerate(similarity[index]))

    top_scores=sorted(scores, key=lambda x:x[1], reverse=True)[1:6]

    result=[]

    for idx,score in top_scores:
        result.append({
            "title":movies.iloc[idx].title,
            score:float(score)
        })

    return result


@app.get('/')
def home():
    return {"msg":"Movie Recommendation System"}


@app.get('/recommendation/{title}')
def recommend(title: str):
    try:
        print(title)
        recommendations=get_recommendation(title)
        return {"input_movie":title, "recommendations":recommendations}
    except:
        return {"error":"Movie not found"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=10000)

