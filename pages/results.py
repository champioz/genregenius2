import polars as pl
import streamlit as st
import streamlit.components.v1 as components
from streamlit_extras.stylable_container import stylable_container
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def read_data(lab):
    
    datasheet = pl.read_csv('../public/data/datasheet.csv')
    label_desc = pl.read_csv('../public/data/label_desc.csv')
    sentences = pl.read_csv('../public/data/sentences.csv')
    timedata = pl.read_csv('../public/data/timedata.csv')
    words = pl.read_csv('../public/data/words.csv')
    
    datasheet = datasheet.filter(pl.col('Group') == lab)
    label_desc = label_desc.filter(pl.col('Group') == lab)
    sentences = sentences.filter(pl.col('Group') == lab)
    words = words.filter(pl.col('Group') == lab)
    
    timedata = timedata.join(
        datasheet, on='Work', how='inner').select(['Month', 'Work', 'Action', 'Count'])
    timedata = timedata.with_columns(
        pl.col('Month').str.to_date("%m/%d/%Y").dt.strftime("%b-%Y")
    )
    timedata = timedata.pivot(values='Count', index=['Work', 'Month'], columns='Action')
    
    ratings = datasheet.rename({
    '1_rating':'1 Star',
    '2_rating':'2 Star',
    '3_rating':'3 Star',
    '4_rating':'4 Star',
    '5_rating':'5 Star'
    })
    ratings = ratings.select(
        ['Group', 'Work', '1 Star', '2 Star', '3 Star', '4 Star', '5 Star']).melt(
            id_vars=['Group', 'Work'], value_vars=['1 Star', '2 Star', '3 Star', '4 Star', '5 Star'], variable_name='Rating', value_name='Count')
    ratings.group_by(by=['Group', 'Rating']).sum().drop('Work')
    
    datasheet = datasheet.with_columns(
        avg_rating=(
            pl.col('1_rating') + 2*pl.col('2_rating') + 3*pl.col('3_rating') + 4*pl.col('4_rating') + 5*pl.col('5_rating'))/(
                pl.col('1_rating') + pl.col('2_rating') + pl.col('3_rating') + pl.col('4_rating') + pl.col('5_rating')
            ).alias('Avg Rating')
    )
    datasheet = datasheet.rename({'avg_rating':'Avg Rating'})  
    
    return datasheet, label_desc, sentences, timedata, words, ratings

    
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
    st.switch_page('app.py')
    
LABEL = st.session_state['LABEL']
if LABEL not in [0, 1, 2, 3, 4]:
        LABEL = 'g3'
        
datasheet, label_desc, sentences, timedata, words, ratings = read_data(LABEL)


## HEADER ##

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
     

## BODY ##

cols = st.columns([1, 8, 1])

with cols[1]:
    if st.button("Back"):
        st.switch_page("app.py")
    

cols = st.columns([1, 4, 2, 1])


## RIGHT COL ##

with cols[2]:
    
    st.write('Your genre is...')
    st.title(label_desc['Label'].item())
    st.write('<h4>Description</h4>', unsafe_allow_html=True)
    with stylable_container(
    "codeblock",
    """
    code {
        white-space: pre-wrap !important;
    }
    """,
    ):
        st.code(label_desc['Description'].item(), language=None)
    st.write('<h4>Most Typical Description Sentences</h4>', unsafe_allow_html=True)
    st.dataframe(sentences.select(['Sentences']), hide_index=True)
    st.write('<h4>Most Frequent Unique Words</h4>', unsafe_allow_html=True)
    text = ', '.join(words['Word'].to_list())
    wordcloud = WordCloud(background_color="white", colormap="Purples", width=800, height=400).generate(text)
    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig)
    
    
## LEFT COL ##
    
with cols[1]:
    st.write('<h4>Genre Popularity</h4>', unsafe_allow_html=True)
    st.line_chart(timedata, x="Month", y=['read', 'review', 'shelf'], color=['#2A0C4E', '#9071CE', '#EEB6DB'])
    st.write('<h4>Rating Distribution</h4>', unsafe_allow_html=True)
    st.bar_chart(ratings, x='Rating', y='Count', color='#9071CE')


cols2 = st.columns([1, 6, 1])

with cols2[1]:
    
    st.write('<h4>Top Five Similar Books by Readership</h4>', unsafe_allow_html=True)
    st.dataframe(
        datasheet.select(['Title', 'URL', 'Author', 'Pub date', 'Readers', 'Avg Rating']).sort(by='Readers', descending=True).limit(5),
        hide_index=True,
        use_container_width=True,
        column_config={
            "URL": st.column_config.LinkColumn()
        }
    )
    
    st.write("<br><br><br><em>Part of a project by Cyndi Campbell, Zach Champion, Paul Kim, and Thuy Nguyen at Georgia Tech</em>",
         unsafe_allow_html=True)
