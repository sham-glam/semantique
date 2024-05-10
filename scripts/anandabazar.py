from bs4 import BeautifulSoup
import os
import regex

def clean(text):
    text = regex.sub(r'\s+', ' ', text)
    text = regex.sub(r'\n+', ' ', text)
    text = regex.sub(r'\n\s*\n', '\n', text)
    text = regex.sub(r' {2,}', ' ', text)
    text = regex.sub(r'[^\u0980-\u09FF ]', '', text) # chars bengali
    text = regex.sub(r'^\s*\w+\s*$', '', text)
    text = regex.sub(r'টি\s*ছবি\s*', '', text)
    text = regex.sub(r'\p{N}+\s+\w+\s+\p{N}+\s+ইপেপার', '', text)
    text = regex.sub(r'আনন্দবাজার\s*পত্রিকা', '', text)
    text = regex.sub(r'সম্পাদকের\s*পাতা', '', text)
    text = regex.sub(r'^\s*$', '', text, flags=regex.MULTILINE)
    text = regex.sub(r'সম্পাদক\s*সমীপেষু', '', text, flags=regex.MULTILINE)
    text = regex.sub(r'^\n*$', '', text, flags=regex.MULTILINE)

   
    return text


def get_paragraphs(html_file):
    with open(html_file, 'rb') as f:
        soup = BeautifulSoup(f, 'html.parser')
        paragraphs = soup.find_all('p')
        for encoding in ['utf-8', 'latin-1', 'iso-8859-1']:
            try:
                for paragraph in paragraphs:
                    with open('../corpus/txtFiles/sample_anandabazar.txt', 'a', encoding=encoding) as out_file:
                        try:
                            text = clean(paragraph.text)
                            if all([text != x for x in ['', ' ', '\n', '\t', None]]):
                                out_file.write(text+'\n')
                                return text
                            else:
                                pass
                        except UnicodeEncodeError:
                            pass
            except UnicodeEncodeError:
                pass


def append_to_file(text):
    for line in text:
        if line is not None:
            with open('../corpus/txtFiles/anandabazar.txt', 'a', encoding='utf-8') as out_file:
                    out_file.write(line+'\n')


def extract_from_html(html_directory):
    text = []
    for root, dirs, files in os.walk(html_directory):

        for filename in files:
            if filename.endswith('.html') or filename.endswith('.htm'):
                file_path = os.path.join(root, filename)
                text.append(get_paragraphs(file_path))

    append_to_file(list(set(text)))


def main():
    html_directory = '../corpus/anandabazar/'
    extract_from_html(html_directory)

if __name__ == "__main__":
    main()