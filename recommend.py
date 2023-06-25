import streamlit as st
import pandas as pd
from build_chart import build_chart
import numpy as np
from PIL import Image
from io import BytesIO

#from IPython.display import Image, display
import requests
import warnings
warnings.filterwarnings("ignore")
st.set_page_config(
    page_title="Welcome to our shop",
    layout="wide",
    initial_sidebar_state="expanded")
st.header('Welcome to our shop')

import json

# open the file for reading
with open('categories.json', 'r') as f:
    # read the JSON-encoded dictionary from the file
    categories = json.load(f)
main_categories = [None]+list(categories.keys())

main_cat = st.selectbox(
    'Select Main Category',
    main_categories
)
st.write('Main Category:', main_cat)
if main_cat ==None:
    sub_cat=None
else:
    sub_categories=[None]+categories[main_cat]
    sub_cat = st.selectbox(
        'Select Sub Category',
        sub_categories)
    st.write('Sub Category:', sub_cat)

x=build_chart(main_cat,sub_cat).head(10)
x=x.reset_index()


# add some text
st.write('Browse our collection of products and find the perfect item for you!')
for i in range(len(x)):
    # print the other columns
    st.write('Name : ', x['name'][i])
    st.write('Ratings : ', x['ratings'][i])
    st.write('Number of Ratings : ', x['no_of_ratings'][i])
    st.write('Weighted Rating: ',x['wr'][i])
    st.write('Actual Price : ',x['actual_price'][i])
    st.write('Price After Discount : ',x['discount_price'][i])
    st.write('Link : ',x['link'][i])
    # display the image
    # download the image file from the URL
    response = requests.get(x['image'][i])

    # check if the request was successful
    if response.status_code == 200:
        # read the image data using PIL
        image = Image.open(BytesIO(response.content))

        # display the image in Streamlit
        st.image(image)
    else:
        st.write("Sorry, there is no image for this item")

    # print the remaining columns
    st.write('-----------------------------------------------')