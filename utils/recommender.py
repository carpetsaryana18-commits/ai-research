import streamlit as st
import requests
import xml.etree.ElementTree as ET

@st.cache_data(ttl=3600)
def recommend_papers(query_text: str):
    """
    Recommends similar research papers using the ArXiv API.
    Results are cached to prevent hitting API rate limits.
    """
    try:
        # Use the ArXiv API for searching papers
        base_url = 'http://export.arxiv.org/api/query?'
        search_query = f'search_query=all:{requests.utils.quote(query_text)}&start=0&max_results=5'
        
        response = requests.get(base_url + search_query)
        response.raise_for_status()  # Raise an exception for bad status codes

        # Parse the XML response
        root = ET.fromstring(response.content)
        
        papers = []
        for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
            title = entry.find('{http://www.w3.org/2005/Atom}title').text.strip()
            
            authors = [
                author.find('{http://www.w3.org/2005/Atom}name').text
                for author in entry.findall('{http://www.w3.org/2005/Atom}author')
            ]
            
            # The 'id' tag often contains the URL to the paper
            url = entry.find('{http://www.w3.org/2005/Atom}id').text.strip()

            papers.append({
                "title": title,
                "authors": authors,
                "url": url
            })
        
        return papers

    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching recommendations from ArXiv. This could be a network issue or an API problem. (Details: {e})")
        return []
    except ET.ParseError:
        st.error("Error parsing the response from the ArXiv API. The API might have returned an invalid format.")
        return []