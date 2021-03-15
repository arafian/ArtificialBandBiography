from bs4 import BeautifulSoup
import sys
import requests
import re

def parse_albums(soup):
    album_names = []
    try:
        for album in soup.find("span", id="Discography").find_parent("h2").find_next_sibling("ul").find_all("i"):
            album_names.append(album.text)
    except:
        pass
    return album_names
