from bs4 import Tag, NavigableString, BeautifulSoup
from pprint import pprint
import urllib


def get_info_from_cell(cell):
    
    # if the cell contains a <ul> tag then extracting the info as an array is simple
    if cell.find('ul'):
        return list(map(lambda e: e.text, cell.find('ul').find_all('li')))
    
    # if the cell does not contain a <ul> tag, then do the following
    
    # split the text in the cell by <br/> tags
    cell_info = ['']
    for element in cell.contents:
        if isinstance(element, NavigableString):
            cell_info[-1] += str(element)
        elif element.name == 'br':
            cell_info.append('')
        else:
            cell_info[-1] += str(element.text)        
    
    # further split the text by newline characters
    cell_info_2 = []
    for string in cell_info:
        cell_info_2 += string.split('\n')
    
    # remove any empty strings
    cell_info_3 = [s for s in cell_info_2 if s != '']
    
    return cell_info_3


def parse_infobox(soup):
    
    infobox = soup.find("table", {"class": "infobox"})
    infobox_dict = {}
    
    if not infobox:
        return infobox_dict

    infobox_rows = infobox.tbody.contents
    for row in infobox_rows:
        if not isinstance(row, Tag) or len(row.contents) != 2:
            continue
        cell_1 = row.contents[0]
        cell_2 = row.contents[1]
        if cell_1.name != "th" or cell_2.name != "td":
            continue

        infobox_dict[cell_1.text] = get_info_from_cell(cell_2)
    
    return infobox_dict