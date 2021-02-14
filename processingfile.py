import base64
import os
import json
import pickle
import uuid
import re


import pandas as pd 
import streamlit as st
def download_button(object_to_download, download_filename, button_text, pickle_it=False):

    if pickle_it:
        try:
            object_to_download = pickle.dumps(object_to_download)
        except pickle.PicklingError as e:
            st.write(e)
            return None

    else:
        if isinstance(object_to_download, bytes):
            object_to_download = object_to_download.to_csv(index=False)

        elif isinstance(object_to_download, pd.DataFrame):
            object_to_download = object_to_download.to_csv(index=False)

        # Try JSON encode for everything else
        else:
            object_to_download = json.dumps(object_to_download)

    try:
        # some strings <-> bytes conversions necessary here
        b64 = base64.b64encode(object_to_download.encode()).decode()

    except AttributeError as e:
        b64 = base64.b64encode(object_to_download).decode()

    button_uuid = str(uuid.uuid4()).replace('-', '')
    button_id = re.sub('\d+', '', button_uuid)

    custom_css = f""" 
        <style>
            #{button_id} {{
                background-color: rgb(255, 255, 255);
                color: rgb(38, 39, 48);
                padding: 0.25em 0.38em;
                position: relative;
                text-decoration: none;
                border-radius: 4px;
                border-width: 1px;
                border-style: solid;
                border-color: rgb(230, 234, 241);
                border-image: initial;

            }} 
            #{button_id}:hover {{
                border-color: rgb(246, 51, 102);
                color: rgb(246, 51, 102);
            }}
            #{button_id}:active {{
                box-shadow: none;
                background-color: rgb(246, 51, 102);
                color: white;
                }}
        </style> """

    dl_link = custom_css + f'<a download="{download_filename}" id="{button_id}" href="data:file/txt;base64,{b64}">{button_text}</a><br></br>'

    return dl_link
      
def file_selector(folder_path='.'):
    filenames = os.listdir(folder_path)
    selected_filename = st.selectbox('Select a file', filenames)
    return os.path.join(folder_path, selected_filename)

file = st.file_uploader("upload your file",type=['csv'])
if file is None:
    st.write("file not uploaded")
if file is not None:
    df = pd.read_csv(file)
    df['z'] = pd.to_datetime(df['Created Date'])
    l = []
    a = pd.Series([])
    df1 = pd.Series([])
    df['Date']=df['z'][0]
    df['y'] = pd.to_datetime(df['Date'], format="%d-%m-%Y %H:%M")
    df['Age'] = abs((df['y'] - df['z'])).dt.days

    for i in range(len(df)):
        if df["Age"][i] == 0:
            a[i] = "0-24hrs"

        elif 3 >= df["Age"][i] > 0:
            a[i] = "1-3days"

        else:
            a[i] = ">3days"
    df['Age>3'] = a
    df.to_csv("processed file.csv")
    
    if st.checkbox('Select a file to download'):
        

        # Upload file for testing
        folder_path = st.text_input('Enter directory: default .', '.')
        filename = "df"

        # Load selected file
       # with open(filename, 'rb') as f:
         #   s = f.read()
        s = df
        download_button_str = download_button(s, filename, f'Click here to download {filename}')
        st.markdown(download_button_str, unsafe_allow_html=True)

    

            
