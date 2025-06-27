import warnings
warnings.filterwarnings("ignore")
import streamlit as st
from langchain_config import get_summary, get_news_articles
from sentence_transformers import SentenceTransformer, util
import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

model = SentenceTransformer('all-MiniLM-L6-v2')

# Custom CSS styling
st.markdown("""
<style>
body {
    font-family: Arial, sans-serif;
}
header {
    background-color: #4682B4; /* Steel blue header */
    padding: 1em;
    text-align: center;
    border-radius: 10px;
    color: white;
    width: 100%; /* Added width: 100% */
    box-sizing: border-box; /* Added box-sizing */
}
.stButton>button {
    background-color: #4CAF50; /* Green button */
    color: white;
    padding: 0.5em 1em;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}
.stButton>button:hover {
    background-color: #3e8e41;
}
.block-container {
    background-color: #87CEEB; /* Light sky blue background */
    padding: 4rem 2rem 2rem 2rem; /* Added more padding to the top */
    border-radius: 10px; /* Added border-radius to the top and bottom */
}
</style>
""", unsafe_allow_html=True)

# Add header
st.markdown("<header><h1>Equity Research News Tool</h1></header>", unsafe_allow_html=True)

# Initialize session state
if 'history' not in st.session_state:
    st.session_state.history = []

st.markdown('*Enter your query to get the latest news articles summarized.*')
query = st.text_input('*QUERY:*', placeholder='Type your query here')

if st.button('*Get News*'):
    if query:
        try:
            with st.spinner("Fetching news articles..."):
                articles = get_news_articles(query)
                if articles:
                    summary = get_summary(query, articles)
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        st.write('### Summary:')
                        st.write(summary)
                    with col2:
                        st.write('### Relevant Articles:')
                        sorted_articles = sorted(articles, key=lambda x: x.get('publishedAt', ''), reverse=True)
                        if sorted_articles[:5]:
                            for article in sorted_articles[:5]:
                                st.write(f"[{article.get('title', '')}]({article.get('url', '')})")
                        else:
                            st.write("No relevant articles found.")
                    st.session_state.history.append(query)
                else:
                    st.write(f"No news articles found for '{query}'. Try a different query.")
                    st.session_state.history.append(query)
        except Exception as e:
            logger.error(f"Error fetching news articles: {e}")
            st.write("Error fetching news articles.")
    else:
        st.write('Please enter a query.')