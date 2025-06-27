import os
from newsapi import NewsApiClient
from groq import Groq
from dotenv import load_dotenv

load_dotenv()  # Load the .env file

news_api_key = os.getenv('NEWS_API_KEY')
groq_api_key = os.getenv('GROQ_API_KEY')

newsapi = NewsApiClient(api_key=news_api_key)
groq_client = Groq(api_key=groq_api_key)

def get_news_articles(query):
    try:
        articles = newsapi.get_everything(q=query, language='en', sort_by='publishedAt')
        return articles['articles']
    except Exception as e:
        print(f"Error fetching news articles: {e}")
        return []

def get_summary(query, articles):
    if not articles:
        return f"No news articles found for '{query}'."
    article_summaries = []
    for article in articles[:5]:
        article_summaries.append(f"{article.get('title', '')}: {article.get('description', '')}")
    summary = '\n\n'.join(article_summaries)
    return summary