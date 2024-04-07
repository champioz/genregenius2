
import streamlit as st
import streamlit.components.v1 as components
from streamlit_extras.stylable_container import stylable_container

    
st.set_page_config(layout="wide")

if 'LABEL' not in st.session_state:
    st.switch_page('app.py')



col_main1, col_main2, col_main3 = st.columns([1, 2, 1])


with col_main2:

    st.image('./public/img/logo.png')
    hide_img_fs = '''
    <style>
    button[title="View fullscreen"]{
        visibility: hidden;}
    </style>
    '''

    st.markdown(hide_img_fs, unsafe_allow_html=True)

    st.write('''
    Genre Genius is an alternative view of readership trends using machine-learned labels built on state-of-the-art semantic clustering and text summarization techniques. Our genres were built using book descriptions from the <a href="https://mengtingwan.github.io/data/goodreads#datasets">large Goodreads dataset for recommender systems</a>. Submit your book's description below to gain insights about the popularity and thematic content of similar titles!
    ''', unsafe_allow_html=True)

    LABEL = st.session_state['LABEL']
    
    if st.button("Back"):
        st.switch_page("app.py")
        

cols = st.columns([1, 8, 1])

with cols[1]:
    st.markdown(f''' <style> iframe{{ display:block; }} </style> ''', unsafe_allow_html=True)
    components.iframe('''https://app.powerbi.com/view?r=eyJrIjoiMzNiYjdhNTQtMjk5Ny00OWZiLTkwNTctNGRmMjQ5ZjdiZGI3IiwidCI6Ijg1OTY4ZGRmLTkzYTQtNDRmZS1iYzhmLTBkNzhiYjhlZjRjZSIsImMiOjN9
    ''', height=900, width=1200, scrolling=True)



cols2 = st.columns([1, 2, 1])

with cols2[1]:
    st.write("<br><br><br><em>Part of a project by Cyndi Campbell, Zach Champion, Paul Kim, and Thuy Nguyen at Georgia Tech</em>",
         unsafe_allow_html=True)