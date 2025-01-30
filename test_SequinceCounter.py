import csv

from Parser import Parser
from SequinceCounter import generate_k_seqs, SequinceCounter, load_data, load_Sentences_names
import tempfile
import json
from test_Parser import create_temp_csv, data_str4, data_str, data_str2, data_str6, data_str5, data_str3, res1, res2, \
    res3, res5, res6, res4, sentence1, sentence2, sentence3, sentence4, sentence5, sentence6


import json
import tempfile


def create_temp_json(data):
    # Create a temporary file using tempfile.NamedTemporaryFile
    with tempfile.NamedTemporaryFile(delete=False, mode='w', newline='', suffix='.json') as tmp_file:
        # Ensure all sets in the data are converted to lists
        # Recursively convert sets to lists in the data
        def convert_sets_to_lists(obj):
            if isinstance(obj, set):
                return list(obj)
            elif isinstance(obj, dict):
                return {key: convert_sets_to_lists(value) for key, value in obj.items()}
            elif isinstance(obj, list):
                return [convert_sets_to_lists(item) for item in obj]
            else:
                return obj

        # Convert sets to lists
        data = convert_sets_to_lists(data)

        # Write the JSON data to the temporary file
        json.dump(data, tmp_file, indent=4)

        # Return the path of the temporary file
        return tmp_file.name


def test_generate_k_seqs():
    """
    Test the generate_k_seqs work as needed
    :return:
    """
    text = [["hello", "world"], ["hello", "world"]]
    assert generate_k_seqs(text, 2) == {'1_seq': [(('hello',), 2), (('world',), 2)], '2_seq': [(('hello', 'world'), 2)]}
    assert generate_k_seqs(text, 3) == {'1_seq': [(('hello',), 2), (('world',), 2)], '2_seq': [(('hello', 'world'), 2)],
                                        '3_seq': []}
    assert generate_k_seqs(text, 4) == {'1_seq': [(('hello',), 2), (('world',), 2)], '2_seq': [(('hello', 'world'), 2)],
                                        '3_seq': [], '4_seq': []}


# examine geeven example
text1 = [["Harry rode on a silver chariot"],
         ["It shined!    like a star of platinum"],
         ["He was known as the red magician "]]
# remove punction
text2 = [[
    '"Under a tuft of jet- black hair over boy forehead Dumbledore and  McGonagall could see a curiously shaped cut, like a bolt of lightning."'],
    ['` Is that where-?` whispered Professor  McGonagall.'],
    [
        '"` Yes,` said  Dumbledore.` Dumbledore,ll have that scar forever.` ` Couldn"t you do something about scar,  Dumbledore?` ` Even if I could, I wouldn"t."']]
# remove double white spaces
text3 = [[
    '"Under a tuft of jet- black hair over boy    forehead Dumbledore and   McGonagall could see a curiously shaped cut, like a bolt of lightning."'],
    ['` Is that where-?` whispered Professor  McGonagall.'],
    [
        '"` Yes,` said   Dumbledore.`   Dumbledore,ll have that scar forever.` ` Couldn"t you do something about scar,  Dumbledore?` ` Even if I could, I wouldn"t."']]
# remove empty lines
text4 = [['he was the over'], ['marry called his name'], ['he was the max']]
# remove white space pre/suf
text5 = [[' he was the over '], [' marry called his name '], [' he was the max ']]
text6 = []
people_names1 = [
    ['Over-Attentive Wizard', ''],
    ['Bertram Aubrey', ''],
    ['Audrey Weasley', ''],
    ['"Augusta" "Gran" "Longbottom"', ''],  # Using single quotes for internal quotes
    ['Augustus Pye', ''],
    ['Augustus Rookwood', ''],
    ['Augustus Worme', ''],
    ['Auntie Muriel', ''],
    ['Aunt Marge Dursley', ''],
    ['Aurelius Dumbledore', ''],
    ['Aurora Sinistra', ''],
    ['Avery', ''],
    ['Babajide Akingbade', ''],
    ['Babayaga', ''],
    ['Babbitty Rabbitty', ''],
    ['Bagman Sr.', ''],
    ['Ludo Bagman', ''],
    ['Otto Bagman', ''],
    ['Millicent Bagnold', ''],
    ['Bathilda Bagshot', 'batty'],
    ['Kquewanda Bailey', ''],
    ['Ballyfumble Stranger', 'quin , quivering quintus , quintusofthesillyname']
]
# check remove whits space
people_names2 = [
    ['Over-Attentive  Wizard', ''],
    ['Bertram Aubrey', ''],
    ['Audrey Weasley', ''],
    ['"Augusta" "Gran" "Longbottom"', ''],  # Using single quotes for internal quotes
    ['Augustus  Pye', ''],
    ['Augustus Rookwood', ''],
    ['Augustus  Worme', ''],
    ['Auntie Muriel', ''],
    ['Aunt Marge Dursley', ''],
    ['Aurelius  Dumbledore', ''],
    ['Aurora   Sinistra', ''],
    ['Avery', ''],
    ['Babajide   Akingbade', ''],
    ['Babayaga', ''],
    ['Babbitty  Rabbitty', ''],
    ['Bagman Sr.', ''],
    ['Ludo  Bagman', ''],
    ['Otto Bagman', ''],
    ['Millicent  Bagnold', ''],
    ['Bathilda   Bagshot', 'batty'],
    ['Kquewanda Bailey', ''],
    ['Ballyfumble Stranger', 'quin , quivering   quintus , quintusofthesillyname']
]
# check add names with no main name
people_names3 = [
    ['Over-Attentive Wizard', ''],
    ['Bertram Aubrey', ''],
    ['Audrey Weasley', ''],
    ['"Augusta" "Gran" "Longbottom"', ''],  # Using single quotes for internal quotes
    ['Augustus Pye', ''],
    ['Augustus Rookwood', ''],
    ['Augustus Worme', ''],
    ['Auntie Muriel', ''],
    ['Aunt Marge Dursley', ''],
    ['Aurelius Dumbledore', ''],
    ['Aurora Sinistra', ''],
    ['Avery', ''],
    ['Babajide Akingbade', ''],
    ['Babayaga', ''],
    ['Babbitty Rabbitty', ''],
    ['Bagman Sr.', ''],
    ['Ludo Bagman', ''],
    ['Otto Bagman', ''],
    ['Millicent Bagnold', ''],
    ['Bathilda Bagshot', 'batty'],
    ['Kquewanda Bailey', ''],
    ['', 'quin , quivering quintus , quintusofthesillyname']
]
# check empty suit
people_names4 = []
# check name that fully main name removed or nick names
people_names5 = [
    ['Over-In', ''],
    ['Bertram Aubrey', ''],
    ['Audrey Weasley', ''],
    ['"Augusta" "Gran" "Longbottom"', ''],  # Using single quotes for internal quotes
    ['Augustus Pye', ''],
    ['Augustus Rookwood', ''],
    ['Augustus Worme', ''],
    ['Auntie Muriel', ''],
    ['Aunt Marge Dursley', ''],
    ['Aurelius Dumbledore', ''],
    ['Aurora Sinistra', ''],
    ['Avery', ''],
    ['Babajide Akingbade', ''],
    ['Babayaga', ''],
    ['Babbitty Rabbitty', ''],
    ['Bagman Sr.', ''],
    ['Ludo Bagman', ''],
    ['Otto Bagman', 'in'],
    ['Millicent Bagnold', ''],
    ['Bathilda Bagshot', 'batty'],
    ['Kquewanda Bailey', ''],
    ['', 'quin , quivering quintus , quintusofthesillyname']
]
# check duplicate names
people_names6 = [
    ['Over-Attentive Wizard', ''],
    ['Bertram Aubrey', ''],
    ['Audrey Weasley', ''],
    ['"Augusta" "Gran" "Longbottom"', ''],  # Using single quotes for internal quotes
    ['Augustus Pye', ''],
    ['Augustus Rookwood', ''],
    ['Augustus Worme', ''],
    ['Auntie Muriel', ''],
    ['Aunt Marge Dursley', ''],
    ['Aurelius Dumbledore', ''],
    ['Aurora Sinistra', ''],
    ['Avery', ''],
    ['Babajide Akingbade', ''],
    ['Babayaga', ''],
    ['Babbitty Rabbitty', ''],
    ['Bagman Sr.', ''],
    ['Ludo Bagman', ''],
    ['Otto Bagman', ''],
    ['Otto Bagman', 'harry cane'],
    ['Millicent Bagnold', ''],
    ['Bathilda Bagshot', 'batty'],
    ['Kquewanda Bailey', ''],
    ['', 'quin , quivering quintus , quintusofthesillyname']
]

# Create the temp CSV file for names
people_names1_path = create_temp_csv(people_names1, ["Name", "Other Names"])
people_names2_path = create_temp_csv(people_names2, ["Name", "Other Names"])
people_names3_path = create_temp_csv(people_names3, ["Name", "Other Names"])
people_names4_path = create_temp_csv(people_names4, ["Name", "Other Names"])
people_names5_path = create_temp_csv(people_names5, ["Name", "Other Names"])
people_names6_path = create_temp_csv(people_names6, ["Name", "Other Names"])

remve_words2 = [['on'], ["a"], ["he"], ["of"], ["it"], ["was"], ["the"], ["over"], ["in"]]
remve_words1 = [['on'], ["a"], ["he"], ["of"], ["it"], ["was"], ["the"], ["in"]]
remve_words3 = [['on'], ["a"], ["he"], ["as"], ["of"], ["it"], ["was"], ["the"]]

csv_sentence1 = create_temp_csv(text1, ["sentence"])
csv_sentence2 = create_temp_csv(text2, ["sentence"])
csv_sentence3 = create_temp_csv(text3, ["sentence"])
csv_sentence4 = create_temp_csv(text4, ["sentence"])
csv_sentence5 = create_temp_csv(text5, ["sentence"])
csv_sentence6 = create_temp_csv(text6, ["sentence"])
csv_remved = create_temp_csv(remve_words1, ["words"])
csv_remved1 = create_temp_csv(remve_words2, ["words"])
csv_remved2 = create_temp_csv(remve_words3, ["words"])

parser1 = Parser(1, sentenceInputPath=csv_sentence1, removeInputPath=csv_remved2, peopleInputPath=people_names1_path)
parser2 = Parser(1, sentenceInputPath=csv_sentence6, removeInputPath=csv_remved1, peopleInputPath=people_names2_path)
parser3 = Parser(1, sentenceInputPath=csv_sentence2, removeInputPath=csv_remved1, peopleInputPath=people_names3_path)
parser4 = Parser(1, sentenceInputPath=csv_sentence3, removeInputPath=csv_remved1, peopleInputPath=people_names4_path)
parser5 = Parser(1, sentenceInputPath=csv_sentence4, removeInputPath=csv_remved1, peopleInputPath=people_names5_path)
parser6 = Parser(1, sentenceInputPath=csv_sentence5, removeInputPath=csv_remved1, peopleInputPath=people_names6_path)

json1 = create_temp_json(data_str)


def test_load_sentence_names():
    loaded_data = load_Sentences_names(json1)
    assert loaded_data == (sentence1, people_names1)


def test_equal_csr():
    pass
