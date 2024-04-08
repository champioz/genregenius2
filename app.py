from model import classify_input
import streamlit as st
import streamlit.components.v1 as components
from streamlit_extras.stylable_container import stylable_container

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
st.markdown(
    """
    <style>
        [data-testid="collapsedControl"] {
            display:none
        }
    </style>
    """,
    unsafe_allow_html=True
)
if 'LABEL' not in st.session_state:
    st.session_state['LABEL'] = None

DESC = ""

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

    if not DESC:
        with st.form("desc", True, border=False) as desc_form:
            
            DESC = st.text_area("Enter your description:", height=200, key="desc")
            submitted = st.form_submit_button("Submit")

    st.write('''<br><br>
    Not an author but want to try? Use one of these (hover and click to copy):   
    ''', unsafe_allow_html=True)

    if DESC:
        LABEL = 'g' + str(classify_input(DESC))
        st.session_state['LABEL'] = LABEL
        st.switch_page('./pages/results.py')

with stylable_container(
    "codeblock",
    """
    code {
        white-space: pre-wrap !important;
    }
    """,
):
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.code('''

        Despite the tumor-shrinking medical miracle that has bought her a few years, Hazel has never been anything but terminal, her final chapter inscribed upon diagnosis. But when a gorgeous plot twist named Augustus Waters suddenly appears at Cancer Kid Support Group, Hazel's story is about to be completely rewritten.
        ''', language=None)
        st.write('-<em>The Fault In Our Stars</em>, John Green', unsafe_allow_html=True)
    
    with col2:
        st.code('''
        Six days ago, astronaut Mark Watney became one of the first people to walk on Mars. Now, he’s sure he’ll be the first person to die there. After a dust storm nearly kills him and forces his crew to evacuate while thinking him dead, Mark finds himself stranded and completely alone with no way to even signal Earth that he’s alive—and even if he could get word out, his supplies would be gone long before a rescue could arrive. Chances are, though, he won’t have time to starve to death.
        ''', language=None)
        st.write('-<em>The Martian</em>, Andy Weir', unsafe_allow_html=True)

    with col3:
        st.code('''
        Mankiw's "Macroeconomics" is popular, widely adopted and well-known for clearly communicating the principles of Macroeconomics in a concise and accessible way. The sixth edition maintains the core features that have made it a best-selling Macroeconomics text - a balance of coverage between short and long-run issues, an integration of Keynesian and classical ideas, a variety of simple models and the incorporation of real world issues and data through case studies and FYI boxes.
        ''', language=None)
        st.write('-<em>Macroeconomics</em>, Manciw', unsafe_allow_html=True)
        


