from bs4 import BeautifulSoup
import os
import regex

def clean(text):
    text = regex.sub(r'\s+', ' ', text)
    text = regex.sub(r'\n+', ' ', text)
    # take only bengali characters
    text = regex.sub(r'[^\u0980-\u09FF ]', '', text)
    # text = regex.sub(r'মেষ|বৃষ|মিথুন|কর্কট| সিংহ| কন্যা| তুলা|বৃশ্চিক|ধনু|মকর|কুম্ভ|মীন', '', text)
    # regex if line has single token or word then remove it
    text = regex.sub(r'^\s*\w+\s*$', '', text)
    # টি ছবি
    text = regex.sub(r'টি\s*ছবি\s*', '', text)
    # delte dates of this format : ১৯ \w ২০২১ ইপেপার
    text = regex.sub(r'\p{N}+\s+\w+\s+\p{N}+\s+ইপেপার', '', text)

    # delete আনন্দবাজার পত্রিকা
    text = regex.sub(r'আনন্দবাজার\s*পত্রিকা', '', text)
    text = regex.sub(r'সম্পাদকের\s*পাতা', '', text)
    # delete empty line
    text = regex.sub(r'^\s*$', '', text)
   
    return text


# def get_paragraphs(html_file):
#     with open(html_file, 'r') as f:
#         soup = BeautifulSoup(f.read(), 'html.parser')
#         paragraphs = soup.find_all('p')
#         for encoding in ['utf-8', 'latin-1', 'iso-8859-1']:
#             try:
#                 for paragraph in paragraphs:
#                     with open('../corpus/txtFiles/anandabazar_p.txt', 'a', encoding=encoding) as out_file:
#                         try:
#                             text = clean(paragraph.text)

#                             out_file.write(paragraph.text)
#                             out_file.write('\n')
#                             print(paragraph.text)
#                             print('\n')
#                         except UnicodeEncodeError:
#                             print('UnicodeEncodeError')
#             except UnicodeEncodeError:
#                 print('UnicodeEncodeError')
           

def get_paragraphs(html_file):
    with open(html_file, 'rb') as f:
        soup = BeautifulSoup(f, 'html.parser')
        paragraphs = soup.find_all('p')
        for encoding in ['utf-8', 'latin-1', 'iso-8859-1']:
            try:
                for paragraph in paragraphs:
                    with open('../corpus/txtFiles/anandabazar_p.txt', 'a', encoding=encoding) as out_file:
                        try:
                            text = clean(paragraph.text)
                            if text != '' or text != ' ':
                                out_file.write(text)
                                out_file.write('\n')
                                print(text)
                                print('\n')
                        except UnicodeEncodeError:
                            print('UnicodeEncodeError')
            except UnicodeEncodeError:
                print('UnicodeEncodeError')


def extract_from_html(html_directory):
    for root, dirs, files in os.walk(html_directory):
        for filename in files:
            if filename.endswith('.html') or filename.endswith('.htm'):
                file_path = os.path.join(root, filename)
                get_paragraphs(file_path)   













def main():
    html_directory = '../corpus/anandabazar/'
    extract_from_html(html_directory)

if __name__ == "__main__":
    main()