from bs4 import BeautifulSoup
import os
import chardet


# def decode_bengali_text(html_file, output_file):
#     with open(html_file, 'r', encoding='utf-8') as f:
#         soup = BeautifulSoup(f.read(), 'html.parser')
#         font_tag = soup.find_all('font', {'face': 'Aabpbengali'})

#         if font_tag:
#             decoded_text = font_tag.text
#             print(decoded_text)
#             # with open(output_file, 'w', encoding='utf-8') as out_file:
#             #     for char in decoded_text:
#             #         # out_file.write(f'U+{ord(char):04X}\n')
#             #         print(f'U+{ord(char):04X}')
#             # print(f'Unicode values written to {output_file}')
#         else:
#             print('Bengali text not found')



def decode_bengali_text(html_file, output_file):
    with open(html_file, 'r', encoding='iso-8859-1') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

        font_tag = soup.find('font', {'face': 'Aabpbengali'})

        if font_tag:
            decoded_text = font_tag.text
            with open(output_file, 'w', encoding='utf-8') as out_file:
                for char in decoded_text:
                    out_file.write(f'U+{ord(char):04X}\n')
            print(f'Unicode values written to {output_file}')
        else:
            print('Bengali text not found')


# def decode_bengali_text(html_file, output_file):
#     utf8_text = ""
#     with open(html_file, 'r') as file:
#         for line in file:
#             try:
#                 decoded_line = line.decode('latin1')
#                 print(decoded_line)
#                 utf8_text += decoded_line
#             except UnicodeDecodeError:
#                 continue
#     # return utf8_text
    # with open(html_file, 'rb') as file:
    #     try:

    #         unicode_html = file.read().decode('utf-8', 'ignore')  
    #         soup = BeautifulSoup(unicode_html)
    #         # html_content = file.read()
    #         # soup = BeautifulSoup(html_content, 'html.parser')
    #         bengali_elements = soup.find_all('font', {'face': 'Aabpbengali'})
    #         decoded_text = []
    #         for element in bengali_elements:
    #             print(element.text)
    #             text = element.decode('utf-8')
    #             print(text)

                # try:
                #     text = element.decode('utf-8')
                #     print(text)
                # except UnicodeDecodeError:
                #     # If decoding as UTF-8 fails, try decoding as Latin-1
                #     decoded_text = text.decode('latin-1')
                #     # return decoded_text
                #     print(decoded_text)
                # with open(output_file, 'a', encoding='utf-8') as f:
                #     f.write(element.text + '\n')

        #     # return decoded_text
        # except Exception as e:
        #     print(f"Error while decoding Bengali text: {e}")
        #     return 0

# Convert the specified HTML file to UTF-8 and export the Bengali text to a text file
# 
def convert_and_export(html_file, output_file):
    # Try different encodings until successful or raise an error
    for encoding in ['utf-8', 'latin-1', 'iso-8859-1']:
        try:
            with open(html_file, 'r', encoding='iso-8859-1') as file:
                html_content = file.read()
            break
        except UnicodeDecodeError:
            continue
            # if encoding == 'iso-8859-1':
            #     raise UnicodeDecodeError("Unable to decode the file with known encodings.")

    soup = BeautifulSoup(html_content, 'html.parser')
    bengali_elements = soup.find_all(lambda tag: tag.name == 'font' and tag.get('face') and 'Aabpbengali' in tag.get('face'))
    for element in bengali_elements:
        text = element.get_text()
        print(text)
        # utf_text = text.encode('utf-8')
        utf_text = text.encode('iso-8859-1')
        # .decode('utf-8')
        print(utf_text)
        # Use chardet to guess the encoding
        guess = chardet.detect(utf_text)
        print(f'chardet guess: {guess}')

        # Use the guessed encoding to decode the string
        if utf_text is not None:
            decoded_text = utf_text.decode('latin-1', errors='ignore')
            print(f'decoded text: {decoded_text}')
        # try:
        #     print(utf_text.decode('utf-8'))
        #     with open(output_file, 'a', encoding='utf-8') as output:
        #         output.write(utf_text.decode('utf-8') + '\n')
        # except UnicodeDecodeError:
        #     print('UnicodeDecodeError')


# Convert all HTML files in the specified directory to UTF-8
def convert_all_html_files(directory):
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.html') or filename.endswith('.htm'):
                file_path = os.path.join(root, filename)
                convert_and_export(file_path, '../corpus/txtFiles/anandabazar.txt')
                decode_bengali_text(file_path, '../corpus/txtFiles/anandabazar.txt')





def main():
    html_directory = '../corpus/anandabazar/'
    convert_all_html_files(html_directory)

if __name__ == "__main__":
    main()