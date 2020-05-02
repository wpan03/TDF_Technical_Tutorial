import streamlit as st
import pandas as pd 
import base64
import webbrowser
from PIL import Image

from search import search_duplicate
from transfer_created import ocp_transfer_created
from transfer_amended import transfer_amend
from merge import merge


selectbox = st.sidebar.selectbox(
    'What do you want to ?',
    ('Home Page','Transfer OCP Created Project', 'Transfer OCP Amended Project', 
    'Search Duplicate','Merge')
)

st.sidebar.info("View [source code](https://github.com/wpan03/TDF_Technical_Tutorial/tree/master/tdf_toolbox)")

if selectbox == 'Home Page':
  st.title("Welcome！")
  st.markdown("This websites contain some useful techniques for TUFF's work. ")
  st.markdown('**Please choose what you want to do in the side bar.**')
  image = Image.open('sunrise.png')
  st.image(image, use_column_width=True)

elif selectbox == 'Transfer OCP Created Project':
  ocp_transfer_created()
  
elif selectbox == "Transfer OCP Amended Project":
  transfer_amend()

elif selectbox == 'Search Duplicate':
  search_duplicate()

elif selectbox == "Merge":
  merge()

