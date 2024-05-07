# read banlaGanashakti.txt count number of tokens -> 2502466
# except for lines starting with 'Image Path: '

import json
import regex
import banglanltk as bn         # https://pypi.org/project/banglanltk/
from pprint import pprint


def count_tokens_in_file(file_path):
    try:
        with open(file_path , 'r' , encoding='utf-8') as f:
            long_string = ""
            lines = f.readlines()
        for line in lines:
            if not line.startswith('Image Path: '):
                long_string += line # concatenate 
        lines = regex.sub(r'\n', ' ', long_string)
        lines = regex.sub(r'[^\p{Bengali}\s]+', '', lines)
        lines = regex.sub(r'\s+', ' ', lines)

        lines = lines.split(' ')
        # count = len(lines)
        print(lines[:100])
        return lines
    except Exception as e:
        print(f"Error while counting tokens in file {file_path.split('/')[-1]}: {e}")
        return 0
    
# étiquetage morpho-syntaxique
def pos_tag_bengali_text(textList):
    word_tag_dict = {}      # {(word, tag):count}
    for word in textList:
        # print(bn.pos_tag(word))
        if (word, bn.pos_tag(word)) not in word_tag_dict:
            word_tag_dict[(word, bn.pos_tag(word))] = 1
        else:
            word_tag_dict[(word, bn.pos_tag(word))] += 1

    return word_tag_dict

def stem_bengali_text(textList):
    # print(bn.stemmer(w))
    pass

# export to json file
def write_to_json(data, output_file):
    # reorder data to have the highest count first
    data = {k: v for k, v in sorted(data.items(), key=lambda item: item[1], reverse=True)}
    json_data = {str(tuple(key)): value for key, value in data.items()}
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)


# main
def main():
    file_path = '../corpus/txtFiles/banglaGanashakti.txt'
    words = count_tokens_in_file(file_path)
    print(f"Number of Bengali tokens in {file_path.split('/')[-1]}: {len(words)}")
    pos_tags = pos_tag_bengali_text(words)
    # pprint(pos_tags)
    write_to_json(pos_tags, '../corpus/txtFiles/banglaGanashakti_pos_tags.json')

if __name__ == "__main__":
     main()

