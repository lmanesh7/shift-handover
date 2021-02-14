import base64
import os
import json
import pickle
import uuid
import re

import streamlit as st
import pandas as pd 
def download_link(object_to_download, download_filename, download_link_text):
    """
    Generates a link to download the given object_to_download.

    object_to_download (str, pd.DataFrame):  The object to be downloaded.
    download_filename (str): filename and extension of file. e.g. mydata.csv, some_txt_output.txt
    download_link_text (str): Text to display for download link.

    Examples:
    download_link(YOUR_DF, 'YOUR_DF.csv', 'Click here to download data!')
    download_link(YOUR_STRING, 'YOUR_STRING.txt', 'Click here to download your text!')

    """
    if isinstance(object_to_download,pd.DataFrame):
        object_to_download = object_to_download.to_csv(index=False)

    # some strings <-> bytes conversions necessary here
    b64 = base64.b64encode(object_to_download.encode()).decode()

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
    df.to_csv("https://raw.githubusercontent.com/lmanesh7/shift-handover/main/processed%20file.csv")
    
    if st.checkbox('Select a file to download'):
        

        # Upload file for testing
        #folder_path = st.text_input('Enter directory: default .', '.')
        filename = "processed file.csv"

        # Load selected file
        with open(filename, 'rb') as f:
            s = f.read()
       
        #download_button_str = download_button(s, filename, f'Click here to download {filename}')
        download_button_str = download_link(df,filename,f'Click here to download {filename}')
        st.markdown(download_button_str, unsafe_allow_html=True)

    

            
