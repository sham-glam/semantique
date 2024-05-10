# bartamanpatrika.py
from bs4 import BeautifulSoup
import os
import regex


def clean(text):
    text = regex.sub(r'\s+', ' ', text)
    text = regex.sub(r'\n+', ' ', text)
    text = regex.sub(r'\n\s*\n', '\n', text)
    text = regex.sub(r' {2,}', ' ', text)
    text = regex.sub(r'[^\u0980-\u09FF ]', '', text)     # take only bengali characters
    text = regex.sub(r'^\s*\w+\s*$', '', text)
    text = regex.sub(r'\s*বিশদ\s*|\s*বিশদ...\s*', '', text, flags=regex.MULTILINE)
    text = regex.sub(r'^\n*$', '', text, flags=regex.MULTILINE)
    text = regex.sub(r'^\s+', '', text, flags=regex.MULTILINE)     # delete if line begins with space
    date_regex = regex.compile(r'^\b(?:কলকাতা|দিল্লী|\w+)\s*(?:শুক্রবার|শনিবার|বৃহস্পতিবার|বুধবার|মঙ্গলবার|সোমবার|রবিবার)\s*\d{1,2}\s*(ডিসেম্বর|নভেম্বর|অক্টোবর|সেপ্টেম্বর|আগস্ট|জুলাই|জুন|মে|অপ্রিল|মার্চ|ফেব্রুয়ারী|জানুয়ারী)\s*\d{4}\s*\d{1,2}\s*(অগ্রহায়ণ|কর্ত্তিক|বৈশাখ|জ্যৈষ্ঠ|আষাঢ়|শ্রাবণ|ভাদ্র|শ্রাবণ|আশ্বিন|কার্তিক|অগ্রহায়ণ|পৌষ)$')

    text = regex.sub(date_regex, '', text)
   
    return text
    

def read_html(html_file):   
    with open(html_file, 'rb') as f:
        try:
            soup = BeautifulSoup(f, 'lxml')
            paragraphs = soup.find_all('p')
            for encoding in ['utf-8', 'latin-1', 'iso-8859-1']:
                for paragraph in paragraphs:
                    text = clean(paragraph.text)
                    if all([text != x for x in ['', ' ', '\n', '\t', None]]) and not text.isspace():
                        with open('../corpus/txtFiles/bartamanpatrika.txt', 'a', encoding=encoding) as out_file:
                            try:
                                out_file.write(text+'\n')
                            except UnicodeEncodeError:
                                pass
        except Exception as e:
            print('Error in reading file:', e)
                

def extract_from_html(html_directory):
    text = []
    for root, dirs, files in os.walk(html_directory):
        for filename in files:
            if filename.endswith('.html') or filename.endswith('.htm'):
                file_path = os.path.join(root, filename)
                read_html(file_path)

def main():
    html_directory = '../corpus/bartamanpatrika/'
    extract_from_html(html_directory)

if __name__ == "__main__":
    main()