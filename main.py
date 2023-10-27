import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import re

class SimpleEpubReader:

    def __init__(self, book_path, maxlines = 39, char_limit = 55):
        self.book = epub.read_epub(book_path)
        self.spine = [item[0] for item in self.book.spine if item[0]]
        self.chapter_map = {}
        self.get_chapter_titles()
        self.maxlines = maxlines
        self.char_limit = char_limit

    def get_chapter_titles(self):
        toc = self.book.get_items_of_type(ebooklib.ITEM_NAVIGATION)
        titles = []

        chap_counter = 0

        for item in toc:
            soup = BeautifulSoup(item.content, 'html.parser')
            for nav_point in soup.find_all('navpoint'):
                spine_idref = chap_counter
                chap_counter += 1
                chapter_title = nav_point.navlabel.text.strip()
                self.chapter_map[chapter_title] = spine_idref
                titles.append(chapter_title)
        return titles
    
    def jump_to_chapter(self, chapter_title):
        if chapter_title in self.chapter_map:
            spine_id = self.chapter_map[chapter_title]
            return self.display_content_from_spine(spine_id)
        else:
            return "Chapter not found"
        
    def jump_to_page(self, chapter_title):
        if chapter_title in self.chapter_map:
            spine_id = self.chapter_map[chapter_title]
            return self.display_content_from_spine(spine_id)
        else:
            return "Chapter not found"

    def display_content_from_spine(self, index):
        if 0 <= index < len(self.spine):
            item = self.book.get_item_with_id(self.spine[index])
            soup = BeautifulSoup(item.content, 'html.parser')
            return soup.prettify()
        else:
            return "Index out of bounds"

    def clean_chapter(self, content):
        texts = []
        soup = BeautifulSoup(content, 'html.parser')
        for tag in soup.find_all(['p', 'i', "title"]):
            text = tag.get_text()
            text = text.replace("\n", "").strip()
            text = re.sub(' +', ' ', text)
            if text == "" or text == 'OceanofPDF.com': 
                continue
            texts.append(text)
        return texts
   