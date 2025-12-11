import streamlit as st
import pandas as pd
import numpy as np   
import pickle
import requests


def get_recommendations(selected_movie):
    url=f'http://localhost:8000/recommendation/{selected_movie}'
    response=requests.get(url).json()
    recs=[]
    for rec in response['recommendations']:
        recs.append(rec['title'])
    return recs
    

movies=pd.read_pickle('movies.pkl')
st.set_page_config("Movie Recommendation System")


st.title("Movie Recommendation System")
selected_movie=st.selectbox("Search for a movie",movies['title'].values)

if st.button("recommend"):
    recs=get_recommendations(selected_movie)
    st.subheader("Top 5 recommendations")
    # st.write(recs)
    for idx,r in enumerate(recs):
        st.write(idx+1," ", r)
