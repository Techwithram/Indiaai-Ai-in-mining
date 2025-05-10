import streamlit as st
import base64

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = f"""
    <style>
    .stApp {{
    background-image: url("data:image/png;base64,{bin_str}");
    background-size: cover;
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)
st.set_page_config(
    page_title="IndiaAi: AI in Mining technologies"
)
set_background("C:\\Users\\krish\\Downloads\\aimin11.jpg")
st.title("Welcome")
st.sidebar.success("Select any one")
info = '''<p style="font-family:sans-serif;font-size:20px;color:black;">Greetings everyone ! We, Tatikonda Ramakrishna and Samiksha S of Chennai Institute of Technology have chosen the theme of Predicting an exploration map based on the shapefile given</p>'''
info1 = '''<p style="font-family:sans-serif;font-size:20px;color:black;">Our Web App contains two fields or options Generate and Predict to generate an exploration map and predict the mineral available based on the given input data or conditions respectively</p>'''
st.markdown(info,unsafe_allow_html=True)
st.markdown(info1,unsafe_allow_html=True)
st.title("Generate Exploration map")
exp = '''<p style="font-family:sans-serif;font-size:20px;color:black;">In this section you are asked to enter your shapefile location from your system storage and hit generate , you will be asked to select the aspect for generating the map from your shapefile provided and the exploration map will be automatically generated</p>'''
st.markdown(exp,unsafe_allow_html=True)
st.title("Predict")
pre = '''<p style="font-family:sans-serif;font-size:20px;color:black;">In this section you can predict the type of mineral or ore available by providing the AI model necessary information. </p>'''
st.markdown(pre,unsafe_allow_html=True)

