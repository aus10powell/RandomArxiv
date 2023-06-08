import streamlit as st
import streamlit.components.v1 as components
import requests
import random
from bs4 import BeautifulSoup

def display_paper(link, title, pdf_link):
    st.title(f"Random Arxiv Paper: A randomly selected paper from Arxiv's newest published papers - {title}")  
    st.markdown(f"[Link to Paper]({link})")
    iframe_tag = f'<iframe src="{pdf_link}" width="1100" height="1000" scrolling="yes" seamless></iframe>'
    st.markdown(iframe_tag, unsafe_allow_html=True)

def main():
    with st.spinner("Wait for it..."):
        url = "https://arxiv.org/list/cs/new"

        response = requests.get(url)

        soup = BeautifulSoup(response.content, "html.parser")

        identifier_spans = soup.find_all("span", class_="list-identifier")

        links = []
        pdfs = []
        for span in identifier_spans:
            link = span.find("a")["href"]
            try:
                pdf_link = span.find("a", title="Download PDF")["href"]
                if link.startswith("/abs/"):
                    links.append("https://arxiv.org" + link)
                if pdf_link.startswith("/pdf/"):
                    pdfs.append("https://arxiv.org" + pdf_link + ".pdf")
            except:
                continue

        s = soup.find_all("div", class_="list-title mathjax")
        titles = [t.text for t in s]

        papers = list(zip(links, titles, pdfs))
        random_paper = random.choice(papers)
        paper_link, paper_title, paper_pdf = random_paper

    display_paper(paper_link, paper_title, paper_pdf)

if __name__ == "__main__":
    main()
