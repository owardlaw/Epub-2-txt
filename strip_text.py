import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup

def extract_toc_from_epub(epub_path):
    book = epub.read_epub(epub_path)
    toc_items = []
    
    # Search for the NCX file
    ncx_item = None
    for item in book.items:
        if item.get_type() == ebooklib.ITEM_NAVIGATION:
            ncx_item = item
            break

    if ncx_item:
        soup = BeautifulSoup(ncx_item.content, 'html.parser')
        nav_points = soup.find_all('navpoint')
        for nav in nav_points:
            toc_items.append(nav.navlabel.text.strip())

    return toc_items


def extract_text_from_epub(epub_path):
    book = epub.read_epub(epub_path)
    texts = []
    titles = []

    for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
        soup = BeautifulSoup(item.content, 'html.parser')
        
        # Extract titles (headers)
        headers = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        for header in headers:
            titles.append(header.get_text().strip())
            header.extract()  # Remove the header to avoid duplication

        # Extract the rest of the text
        texts.append(soup.get_text())

    return texts, titles


def get_text_of_chapter_by_title(epub_path, chapter_title):
    book = epub.read_epub(epub_path)
    
    # Search for the NCX file
    ncx_item = None
    for item in book.items:
        if item.get_type() == ebooklib.ITEM_NAVIGATION:
            ncx_item = item
            break

    if not ncx_item:
        return None

    soup = BeautifulSoup(ncx_item.content, 'html.parser')
    
    # Search for the navpoint corresponding to the chapter title
    nav_points = soup.find_all('navpoint')
    content_id = None
    for nav in nav_points:
        if nav.navlabel.text.strip() == chapter_title:
            # Get the content id associated with this navpoint
            content_id = nav.content['src'].split("#")[0]
            break

    if not content_id:
        return None

    # Find the content item by matching its file_name
    content_item = None
    for item in book.items:
        if item.file_name == content_id:
            content_item = item
            break

    if not content_item:
        return None

    # Extract and return the text from the associated content document
    content_soup = BeautifulSoup(content_item.content, 'html.parser')
    return content_soup.get_text()


epub_file = 's.epub'
chapter_name = 'Chapter 30'
text = get_text_of_chapter_by_title(epub_file, chapter_name)

if text:
    print(text)
else:
    print(f"Chapter titled '{chapter_name}' not found.")

# epub_file = 's.epub'
# toc = extract_toc_from_epub(epub_file)
# texts, titles = extract_text_from_epub(epub_file)

# print("Table of Contents:")
# for item in toc:
#     print(item)

# print("\nTitles in the Book:")
# for title in titles:
#     print(title)

# print("\nText Content:")
# for text in texts:
#     print(text)
