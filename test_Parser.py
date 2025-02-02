import json
import string
from Parser import process_sentence, hash_dict_for_punctuation, Parser
import tempfile
import csv


def test_preprocesser_text():
    assert process_sentence("H   i") == "h i"  # test remove duplicate white space in middle of sentence
    assert process_sentence("mr   dunder") == "mr dunder"
    assert process_sentence("Mr.Alix") == "mr alix"  # test remove punctuation white space in middle of sentence
    assert process_sentence(" Mr- Potter ") == "mr potter"
    assert process_sentence("") == ""
    assert process_sentence("Mr.") == "mr"
    assert process_sentence("José ") == 'jos'
    result1 = (
        "under a tuft of jet black hair over boy forehead dumbledore and mcgonagall could see a curiously shaped "
        "cut like a bolt of lightning")
    input1 = ("Under a tuft of jet- black hair over boy forehead Dumbledore and  McGonagall could see a curiously "
              "shaped cut, like a bolt of lightning.")
    assert process_sentence(input1) == result1
    input2 = ("Ten years ago, there had been lots of pictures of what looked like a large pink beach ball wearing "
              "different- colored bonnets-- but    Dudley Dursley was no longer a baby, and now the photographs "
              "showed a large blond boy riding boy first bicycle, on a carousel at the fair, playing a computer game "
              "with boy father, being hugged and kissed by boy mother.")
    result2 = ("ten years ago there had been lots of pictures of what looked like a large pink beach ball wearing "
               "different colored bonnets but dudley dursley was no longer a baby and now the photographs showed a large "
               "blond boy riding boy first bicycle on a carousel at the fair playing a computer game with boy father "
               "being hugged and kissed by boy mother")
    assert process_sentence(input2) == result2
    assert process_sentence("Hello WORLD!") == "hello world"
    assert process_sentence("MiXed CASE!") == "mixed case"

    # Test that punctuation is replaced with a whitespace
    assert process_sentence("Mr. Potter!") == "mr potter"
    assert process_sentence("I don'__Threshold know!") == "i don threshold know"
    assert process_sentence("Hello... Mr. Watson!!!") == "hello mr watson"

    # Test that double whitespaces are removed
    assert process_sentence("This  is   a  test") == "this is a test"
    assert process_sentence("Mr.   Potter  and   Mrs.  Weasley") == "mr potter and mrs weasley"

    # Test for mixed cases and spaces
    assert process_sentence("   This   is a   sentence!  ") == "this is a sentence"
    assert process_sentence("Hello   World   !") == "hello world"

    # Test more complex __sentences
    input1 = "Hello, Mr. Potter!   How are you?"
    result1 = "hello mr potter how are you"
    assert process_sentence(input1) == result1

    input2 = "   I   don'__Threshold    understand... what's going on!!"
    result2 = "i don threshold understand what s going on"
    assert process_sentence(input2) == result2

    input3 = "   I said, Mr. Watson, Come here! "
    result3 = "i said mr watson come here"
    assert process_sentence(input3) == result3

    input4 = "It's  a long   day, isn'__Threshold it?"
    result4 = "it s a long day isn __Threshold it"
    assert process_sentence(input4) != result4


def test_hashDict():
    # Call the function to get the hash map
    hashDict = hash_dict_for_punctuation()
    # Test that a space maps to a space
    assert hashDict[" "] == " "
    # Test that lowercase letters map to themselves
    for value in range(97, 123):
        assert hashDict[chr(value)] == chr(value)
    # Test that uppercase letters map to lowercase
    for value in range(65, 91):
        assert hashDict[chr(value)] == chr(value + 32)
    # Test that digits map to themselves
    for value in range(48, 58):
        assert hashDict[chr(value)] == chr(value)
    # Test that punctuation characters map to a space
    for char in string.punctuation:
        assert hashDict[char] == " "
    # Test that newlines and tabs remain unchanged
    assert hashDict["\n"] == "\n"
    assert hashDict["\t"] == "\t"


def create_temp_csv(data, start):
    # Create a temporary file using tempfile.NamedTemporaryFile
    with tempfile.NamedTemporaryFile(delete=False, mode='w', newline='', suffix='.csv') as tmp_file:
        # Create a CSV writer object and write the data to the temporary file
        writer = csv.writer(tmp_file)
        # Write header (optional)
        writer.writerow(start)
        # Write the rows of data
        writer.writerows(data)
        # Return the path of the temporary file
        return tmp_file.name


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


def create_temp_csv_with_data(data: list[list[str]], headers: list[str]) -> str:
    """
    Creates a temporary CSV file with the given headers and data.
    Parameters:
        data (list of lists): A list of rows, where each row is a list of values.
        headers (list of str): A list of strings representing the column headers.
    Returns:
        str: The path to the created temporary CSV file.
    """
    try:
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, mode='w', newline='', encoding='utf-8',
                                         suffix='.csv') as temp_file:
            writer = csv.writer(temp_file)

            # Write the headers
            writer.writerow(headers)

            # Write the rows
            writer.writerows(data, )

            # Get the path to the temporary file
            temp_file_path = temp_file.name

        print(f"Temporary CSV file created at: {temp_file_path}")
        return temp_file_path

    except Exception as e:
        print(f"An error occurred while creating the temporary CSV file: {e}")
        raise


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
    ['Ballyfumble Stranger', 'quin , quivering quintus , quintusofthesillyname'],['on a he','']

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

remve_words2 = [['on'],
                ["a"],
                ["he"],
                ["of"],
                ["it"],
                ["was"],
                ["the"],
                ["over"],
                ["in"]]
remve_words1 = [['on'],
                ["a"],
                ["he"],
                ["of"],
                ["it"],
                ["was"],
                ["the"],
                ["in"]]
remve_words3 = [['on'],
                ["a"],
                ["he"],
                ["as"],
                ["of"],
                ["it"],
                ["was"],
                ["the"]]

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

name_res1 = [[['over', 'attentive', 'wizard'], []],
             [['bertram', 'aubrey'], []],
             [['audrey', 'weasley'], []],
             [['augusta', 'gran', 'longbottom'], []],
             [['augustus', 'pye'], []],
             [['augustus', 'rookwood'], []],
             [['augustus', 'worme'], []],
             [['auntie', 'muriel'], []],
             [['aunt', 'marge', 'dursley'], []],
             [['aurelius', 'dumbledore'], []],
             [['aurora', 'sinistra'], []],
             [['avery'], []],
             [['babajide', 'akingbade'], []],
             [['babayaga'], []],
             [['babbitty', 'rabbitty'], []],
             [['bagman', 'sr'], []],
             [['ludo', 'bagman'], []],
             [['otto', 'bagman'], []],
             [['millicent', 'bagnold'], []],
             [['bathilda', 'bagshot'], [['batty']]],
             [['kquewanda', 'bailey'], []],
             [['ballyfumble', 'stranger'],
         [['quin'], ['quivering', 'quintus'], ['quintusofthesillyname']]]]
name_res2 = [[['attentive', 'wizard'], []],
             [['bertram', 'aubrey'], []],
             [['audrey', 'weasley'], []],
             [['augusta', 'gran', 'longbottom'], []],
             [['augustus', 'pye'], []],
             [['augustus', 'rookwood'], []],
             [['augustus', 'worme'], []],
             [['auntie', 'muriel'], []],
             [['aunt', 'marge', 'dursley'], []],
             [['aurelius', 'dumbledore'], []],
             [['aurora', 'sinistra'], []],
             [['avery'], []],
             [['babajide', 'akingbade'], []],
             [['babayaga'], []],
             [['babbitty', 'rabbitty'], []],
             [['bagman', 'sr'], []],
             [['ludo', 'bagman'], []],
             [['otto', 'bagman'], []],
             [['millicent', 'bagnold'], []],
             [['bathilda', 'bagshot'], [['batty']]],
             [['kquewanda', 'bailey'], []],
             [['ballyfumble', 'stranger'],
         [['quin'], ['quivering', 'quintus'], ['quintusofthesillyname']]]]
name_res3 = [[['attentive', 'wizard'], []],
             [['bertram', 'aubrey'], []],
             [['audrey', 'weasley'], []],
             [['augusta', 'gran', 'longbottom'], []],
             [['augustus', 'pye'], []],
             [['augustus', 'rookwood'], []],
             [['augustus', 'worme'], []],
             [['auntie', 'muriel'], []],
             [['aunt', 'marge', 'dursley'], []],
             [['aurelius', 'dumbledore'], []],
             [['aurora', 'sinistra'], []],
             [['avery'], []],
             [['babajide', 'akingbade'], []],
             [['babayaga'], []],
             [['babbitty', 'rabbitty'], []],
             [['bagman', 'sr'], []],
             [['ludo', 'bagman'], []],
             [['otto', 'bagman'], []],
             [['millicent', 'bagnold'], []],
             [['bathilda', 'bagshot'], [['batty']]],
             [['kquewanda', 'bailey'], []]]

name_res5 = [[['bertram', 'aubrey'], []],
             [['audrey', 'weasley'], []],
             [['augusta', 'gran', 'longbottom'], []],
             [['augustus', 'pye'], []],
             [['augustus', 'rookwood'], []],
             [['augustus', 'worme'], []],
             [['auntie', 'muriel'], []],
             [['aunt', 'marge', 'dursley'], []],
             [['aurelius', 'dumbledore'], []],
             [['aurora', 'sinistra'], []],
             [['avery'], []],
             [['babajide', 'akingbade'], []],
             [['babayaga'], []],
             [['babbitty', 'rabbitty'], []],
             [['bagman', 'sr'], []],
             [['ludo', 'bagman'], []],
             [['otto', 'bagman'], []],
             [['millicent', 'bagnold'], []],
             [['bathilda', 'bagshot'], [['batty']]],
             [['kquewanda', 'bailey'], []]]

name_res4 = []

name_res6 = [[['attentive', 'wizard'], []],
             [['bertram', 'aubrey'], []],
             [['audrey', 'weasley'], []],
             [['augusta', 'gran', 'longbottom'], []],
             [['augustus', 'pye'], []],
             [['augustus', 'rookwood'], []],
             [['augustus', 'worme'], []],
             [['auntie', 'muriel'], []],
             [['aunt', 'marge', 'dursley'], []],
             [['aurelius', 'dumbledore'], []],
             [['aurora', 'sinistra'], []],
             [['avery'], []],
             [['babajide', 'akingbade'], []],
             [['babayaga'], []],
             [['babbitty', 'rabbitty'], []],
             [['bagman', 'sr'], []],
             [['ludo', 'bagman'], []],
             [['otto', 'bagman'], []],
             [['millicent', 'bagnold'], []],
             [['bathilda', 'bagshot'], [['batty']]],
             [['kquewanda', 'bailey'], []]]


def test_name_Parser():
    assert parser1.get_people() == name_res1
    assert parser2.get_people() == name_res2
    assert parser3.get_people() == name_res3
    assert parser4.get_people() == []
    assert parser5.get_people() == name_res5
    assert parser6.get_people() == name_res6


sentence1 = [['harry', 'rode', 'silver', 'chariot'], ['shined', 'like', 'star', 'platinum'],
             ['known', 'red', 'magician']]
sentence2 = []
sentence3 = [
    ['under', 'tuft', 'jet', 'black', 'hair', 'boy', 'forehead', 'dumbledore', 'and', 'mcgonagall', 'could', 'see',
     'curiously', 'shaped', 'cut', 'like', 'bolt', 'lightning'],
    ['is', 'that', 'where', 'whispered', 'professor', 'mcgonagall'],
    ['yes', 'said', 'dumbledore', 'dumbledore', 'll', 'have', 'that', 'scar', 'forever', 'couldn', 't', 'you', 'do',
     'something', 'about', 'scar', 'dumbledore', 'even', 'if', 'i', 'could', 'i', 'wouldn', 't']]
sentence4 = [
    ['under', 'tuft', 'jet', 'black', 'hair', 'boy', 'forehead', 'dumbledore', 'and', 'mcgonagall', 'could', 'see',
     'curiously', 'shaped', 'cut', 'like', 'bolt', 'lightning'],
    ['is', 'that', 'where', 'whispered', 'professor', 'mcgonagall'],
    ['yes', 'said', 'dumbledore', 'dumbledore', 'll', 'have', 'that', 'scar', 'forever', 'couldn', 't', 'you', 'do',
     'something', 'about', 'scar', 'dumbledore', 'even', 'if', 'i', 'could', 'i', 'wouldn', 't']]
sentence5 = [['marry', 'called', 'his', 'name'], ['max']]
sentence6 = [['marry', 'called', 'his', 'name'], ['max']]


def test_parser_procees_senetnec():
    assert parser1.getSentences() == sentence1
    assert parser2.getSentences() == sentence2
    assert parser3.getSentences() == sentence3
    assert parser4.getSentences() == sentence4
    assert parser5.getSentences() == sentence5
    assert parser6.getSentences() == sentence6


def test_parser_words_to_remove():
    assert parser1.get_remove_words() == {'a': True, 'as': True, 'he': True, 'it': True, 'of': True, 'on': True,
                                          'the': True, 'was': True}
    assert parser2.get_remove_words() == {'a': True, 'he': True, 'in': True, 'it': True, 'of': True, 'on': True,
                                          'over': True, 'the': True, 'was': True}
    assert parser3.get_remove_words() == {'a': True, 'he': True, 'in': True, 'it': True, 'of': True, 'on': True,
                                          'over': True, 'the': True, 'was': True}
    assert parser4.get_remove_words() == {'a': True, 'he': True, 'in': True, 'it': True, 'of': True, 'on': True,
                                          'over': True, 'the': True, 'was': True}
    assert parser5.get_remove_words() == {'a': True, 'he': True, 'in': True, 'it': True, 'of': True, 'on': True,
                                          'over': True, 'the': True, 'was': True}
    assert parser6.get_remove_words() == {'a': True, 'he': True, 'in': True, 'it': True, 'of': True, 'on': True,
                                          'over': True, 'the': True, 'was': True}


data_str = ('{\n'
            '    "Question 1": {\n'
            '        "Processed Sentences": [\n'
            '            [\n'
            '                "harry",\n'
            '                "rode",\n'
            '                "silver",\n'
            '                "chariot"\n'
            '            ],\n'
            '            [\n'
            '                "shined",\n'
            '                "like",\n'
            '                "star",\n'
            '                "platinum"\n'
            '            ],\n'
            '            [\n'
            '                "known",\n'
            '                "red",\n'
            '                "magician"\n'
            '            ]\n'
            '        ],\n'
            '        "Processed Names": [\n'
            '            [\n'
            '                [\n'
            '                    "over",\n'
            '                    "attentive",\n'
            '                    "wizard"\n'
            '                ],\n'
            '                []\n'
            '            ],\n'
            '            [\n'
            '                [\n'
            '                    "bertram",\n'
            '                    "aubrey"\n'
            '                ],\n'
            '                []\n'
            '            ],\n'
            '            [\n'
            '                [\n'
            '                    "audrey",\n'
            '                    "weasley"\n'
            '                ],\n'
            '                []\n'
            '            ],\n'
            '            [\n'
            '                [\n'
            '                    "augusta",\n'
            '                    "gran",\n'
            '                    "longbottom"\n'
            '                ],\n'
            '                []\n'
            '            ],\n'
            '            [\n'
            '                [\n'
            '                    "augustus",\n'
            '                    "pye"\n'
            '                ],\n'
            '                []\n'
            '            ],\n'
            '            [\n'
            '                [\n'
            '                    "augustus",\n'
            '                    "rookwood"\n'
            '                ],\n'
            '                []\n'
            '            ],\n'
            '            [\n'
            '                [\n'
            '                    "augustus",\n'
            '                    "worme"\n'
            '                ],\n'
            '                []\n'
            '            ],\n'
            '            [\n'
            '                [\n'
            '                    "auntie",\n'
            '                    "muriel"\n'
            '                ],\n'
            '                []\n'
            '            ],\n'
            '            [\n'
            '                [\n'
            '                    "aunt",\n'
            '                    "marge",\n'
            '                    "dursley"\n'
            '                ],\n'
            '                []\n'
            '            ],\n'
            '            [\n'
            '                [\n'
            '                    "aurelius",\n'
            '                    "dumbledore"\n'
            '                ],\n'
            '                []\n'
            '            ],\n'
            '            [\n'
            '                [\n'
            '                    "aurora",\n'
            '                    "sinistra"\n'
            '                ],\n'
            '                []\n'
            '            ],\n'
            '            [\n'
            '                [\n'
            '                    "avery"\n'
            '                ],\n'
            '                []\n'
            '            ],\n'
            '            [\n'
            '                [\n'
            '                    "babajide",\n'
            '                    "akingbade"\n'
            '                ],\n'
            '                []\n'
            '            ],\n'
            '            [\n'
            '                [\n'
            '                    "babayaga"\n'
            '                ],\n'
            '                []\n'
            '            ],\n'
            '            [\n'
            '                [\n'
            '                    "babbitty",\n'
            '                    "rabbitty"\n'
            '                ],\n'
            '                []\n'
            '            ],\n'
            '            [\n'
            '                [\n'
            '                    "bagman",\n'
            '                    "sr"\n'
            '                ],\n'
            '                []\n'
            '            ],\n'
            '            [\n'
            '                [\n'
            '                    "ludo",\n'
            '                    "bagman"\n'
            '                ],\n'
            '                []\n'
            '            ],\n'
            '            [\n'
            '                [\n'
            '                    "otto",\n'
            '                    "bagman"\n'
            '                ],\n'
            '                []\n'
            '            ],\n'
            '            [\n'
            '                [\n'
            '                    "millicent",\n'
            '                    "bagnold"\n'
            '                ],\n'
            '                []\n'
            '            ],\n'
            '            [\n'
            '                [\n'
            '                    "bathilda",\n'
            '                    "bagshot"\n'
            '                ],\n'
            '                [\n'
            '                    [\n'
            '                        "batty"\n'
            '                    ]\n'
            '                ]\n'
            '            ],\n'
            '            [\n'
            '                [\n'
            '                    "kquewanda",\n'
            '                    "bailey"\n'
            '                ],\n'
            '                []\n'
            '            ],\n'
            '            [\n'
            '                [\n'
            '                    "ballyfumble",\n'
            '                    "stranger"\n'
            '                ],\n'
            '                [\n'
            '                    [\n'
            '                        "quin"\n'
            '                    ],\n'
            '                    [\n'
            '                        "quivering",\n'
            '                        "quintus"\n'
            '                    ],\n'
            '                    [\n'
            '                        "quintusofthesillyname"\n'
            '                    ]\n'
            '                ]\n'
            '            ]\n'
            '        ]\n'
            '    }\n'
            '}')

data_str2 = ('{\n'
             '    "Question 1": {\n'
             '        "Processed Sentences": [],\n'
             '        "Processed Names": [\n'
             '            [\n'
             '                [\n'
             '                    "attentive",\n'
             '                    "wizard"\n'
             '                ],\n'
             '                []\n'
             '            ],\n'
             '            [\n'
             '                [\n'
             '                    "bertram",\n'
             '                    "aubrey"\n'
             '                ],\n'
             '                []\n'
             '            ],\n'
             '            [\n'
             '                [\n'
             '                    "audrey",\n'
             '                    "weasley"\n'
             '                ],\n'
             '                []\n'
             '            ],\n'
             '            [\n'
             '                [\n'
             '                    "augusta",\n'
             '                    "gran",\n'
             '                    "longbottom"\n'
             '                ],\n'
             '                []\n'
             '            ],\n'
             '            [\n'
             '                [\n'
             '                    "augustus",\n'
             '                    "pye"\n'
             '                ],\n'
             '                []\n'
             '            ],\n'
             '            [\n'
             '                [\n'
             '                    "augustus",\n'
             '                    "rookwood"\n'
             '                ],\n'
             '                []\n'
             '            ],\n'
             '            [\n'
             '                [\n'
             '                    "augustus",\n'
             '                    "worme"\n'
             '                ],\n'
             '                []\n'
             '            ],\n'
             '            [\n'
             '                [\n'
             '                    "auntie",\n'
             '                    "muriel"\n'
             '                ],\n'
             '                []\n'
             '            ],\n'
             '            [\n'
             '                [\n'
             '                    "aunt",\n'
             '                    "marge",\n'
             '                    "dursley"\n'
             '                ],\n'
             '                []\n'
             '            ],\n'
             '            [\n'
             '                [\n'
             '                    "aurelius",\n'
             '                    "dumbledore"\n'
             '                ],\n'
             '                []\n'
             '            ],\n'
             '            [\n'
             '                [\n'
             '                    "aurora",\n'
             '                    "sinistra"\n'
             '                ],\n'
             '                []\n'
             '            ],\n'
             '            [\n'
             '                [\n'
             '                    "avery"\n'
             '                ],\n'
             '                []\n'
             '            ],\n'
             '            [\n'
             '                [\n'
             '                    "babajide",\n'
             '                    "akingbade"\n'
             '                ],\n'
             '                []\n'
             '            ],\n'
             '            [\n'
             '                [\n'
             '                    "babayaga"\n'
             '                ],\n'
             '                []\n'
             '            ],\n'
             '            [\n'
             '                [\n'
             '                    "babbitty",\n'
             '                    "rabbitty"\n'
             '                ],\n'
             '                []\n'
             '            ],\n'
             '            [\n'
             '                [\n'
             '                    "bagman",\n'
             '                    "sr"\n'
             '                ],\n'
             '                []\n'
             '            ],\n'
             '            [\n'
             '                [\n'
             '                    "ludo",\n'
             '                    "bagman"\n'
             '                ],\n'
             '                []\n'
             '            ],\n'
             '            [\n'
             '                [\n'
             '                    "otto",\n'
             '                    "bagman"\n'
             '                ],\n'
             '                []\n'
             '            ],\n'
             '            [\n'
             '                [\n'
             '                    "millicent",\n'
             '                    "bagnold"\n'
             '                ],\n'
             '                []\n'
             '            ],\n'
             '            [\n'
             '                [\n'
             '                    "bathilda",\n'
             '                    "bagshot"\n'
             '                ],\n'
             '                [\n'
             '                    [\n'
             '                        "batty"\n'
             '                    ]\n'
             '                ]\n'
             '            ],\n'
             '            [\n'
             '                [\n'
             '                    "kquewanda",\n'
             '                    "bailey"\n'
             '                ],\n'
             '                []\n'
             '            ],\n'
             '            [\n'
             '                [\n'
             '                    "ballyfumble",\n'
             '                    "stranger"\n'
             '                ],\n'
             '                [\n'
             '                    [\n'
             '                        "quin"\n'
             '                    ],\n'
             '                    [\n'
             '                        "quivering",\n'
             '                        "quintus"\n'
             '                    ],\n'
             '                    [\n'
             '                        "quintusofthesillyname"\n'
             '                    ]\n'
             '                ]\n'
             '            ]\n'
             '        ]\n'
             '    }\n'
             '}')
data_str3 = ('{\n'
             '    "Question 1": {\n'
             '        "Processed Sentences": [\n'
             '            [\n'
             '                "under",\n'
             '                "tuft",\n'
             '                "jet",\n'
             '                "black",\n'
             '                "hair",\n'
             '                "boy",\n'
             '                "forehead",\n'
             '                "dumbledore",\n'
             '                "and",\n'
             '                "mcgonagall",\n'
             '                "could",\n'
             '                "see",\n'
             '                "curiously",\n'
             '                "shaped",\n'
             '                "cut",\n'
             '                "like",\n'
             '                "bolt",\n'
             '                "lightning"\n'
             '            ],\n'
             '            [\n'
             '                "is",\n'
             '                "that",\n'
             '                "where",\n'
             '                "whispered",\n'
             '                "professor",\n'
             '                "mcgonagall"\n'
             '            ],\n'
             '            [\n'
             '                "yes",\n'
             '                "said",\n'
             '                "dumbledore",\n'
             '                "dumbledore",\n'
             '                "ll",\n'
             '                "have",\n'
             '                "that",\n'
             '                "scar",\n'
             '                "forever",\n'
             '                "couldn",\n'
             '                "t",\n'
             '                "you",\n'
             '                "do",\n'
             '                "something",\n'
             '                "about",\n'
             '                "scar",\n'
             '                "dumbledore",\n'
             '                "even",\n'
             '                "if",\n'
             '                "i",\n'
             '                "could",\n'
             '                "i",\n'
             '                "wouldn",\n'
             '                "t"\n'
             '            ]\n'
             '        ],\n'
             '        "Processed Names": [\n'
             '            [\n'
             '                [\n'
             '                    "attentive",\n'
             '                    "wizard"\n'
             '                ],\n'
             '                []\n'
             '            ],\n'
             '            [\n'
             '                [\n'
             '                    "bertram",\n'
             '                    "aubrey"\n'
             '                ],\n'
             '                []\n'
             '            ],\n'
             '            [\n'
             '                [\n'
             '                    "audrey",\n'
             '                    "weasley"\n'
             '                ],\n'
             '                []\n'
             '            ],\n'
             '            [\n'
             '                [\n'
             '                    "augusta",\n'
             '                    "gran",\n'
             '                    "longbottom"\n'
             '                ],\n'
             '                []\n'
             '            ],\n'
             '            [\n'
             '                [\n'
             '                    "augustus",\n'
             '                    "pye"\n'
             '                ],\n'
             '                []\n'
             '            ],\n'
             '            [\n'
             '                [\n'
             '                    "augustus",\n'
             '                    "rookwood"\n'
             '                ],\n'
             '                []\n'
             '            ],\n'
             '            [\n'
             '                [\n'
             '                    "augustus",\n'
             '                    "worme"\n'
             '                ],\n'
             '                []\n'
             '            ],\n'
             '            [\n'
             '                [\n'
             '                    "auntie",\n'
             '                    "muriel"\n'
             '                ],\n'
             '                []\n'
             '            ],\n'
             '            [\n'
             '                [\n'
             '                    "aunt",\n'
             '                    "marge",\n'
             '                    "dursley"\n'
             '                ],\n'
             '                []\n'
             '            ],\n'
             '            [\n'
             '                [\n'
             '                    "aurelius",\n'
             '                    "dumbledore"\n'
             '                ],\n'
             '                []\n'
             '            ],\n'
             '            [\n'
             '                [\n'
             '                    "aurora",\n'
             '                    "sinistra"\n'
             '                ],\n'
             '                []\n'
             '            ],\n'
             '            [\n'
             '                [\n'
             '                    "avery"\n'
             '                ],\n'
             '                []\n'
             '            ],\n'
             '            [\n'
             '                [\n'
             '                    "babajide",\n'
             '                    "akingbade"\n'
             '                ],\n'
             '                []\n'
             '            ],\n'
             '            [\n'
             '                [\n'
             '                    "babayaga"\n'
             '                ],\n'
             '                []\n'
             '            ],\n'
             '            [\n'
             '                [\n'
             '                    "babbitty",\n'
             '                    "rabbitty"\n'
             '                ],\n'
             '                []\n'
             '            ],\n'
             '            [\n'
             '                [\n'
             '                    "bagman",\n'
             '                    "sr"\n'
             '                ],\n'
             '                []\n'
             '            ],\n'
             '            [\n'
             '                [\n'
             '                    "ludo",\n'
             '                    "bagman"\n'
             '                ],\n'
             '                []\n'
             '            ],\n'
             '            [\n'
             '                [\n'
             '                    "otto",\n'
             '                    "bagman"\n'
             '                ],\n'
             '                []\n'
             '            ],\n'
             '            [\n'
             '                [\n'
             '                    "millicent",\n'
             '                    "bagnold"\n'
             '                ],\n'
             '                []\n'
             '            ],\n'
             '            [\n'
             '                [\n'
             '                    "bathilda",\n'
             '                    "bagshot"\n'
             '                ],\n'
             '                [\n'
             '                    [\n'
             '                        "batty"\n'
             '                    ]\n'
             '                ]\n'
             '            ],\n'
             '            [\n'
             '                [\n'
             '                    "kquewanda",\n'
             '                    "bailey"\n'
             '                ],\n'
             '                []\n'
             '            ]\n'
             '        ]\n'
             '    }\n'
             '}')

data_str4 = ('{\n'
             '    "Question 1": {\n'
             '        "Processed Sentences": [\n'
             '            [\n'
             '                "under",\n'
             '                "tuft",\n'
             '                "jet",\n'
             '                "black",\n'
             '                "hair",\n'
             '                "boy",\n'
             '                "forehead",\n'
             '                "dumbledore",\n'
             '                "and",\n'
             '                "mcgonagall",\n'
             '                "could",\n'
             '                "see",\n'
             '                "curiously",\n'
             '                "shaped",\n'
             '                "cut",\n'
             '                "like",\n'
             '                "bolt",\n'
             '                "lightning"\n'
             '            ],\n'
             '            [\n'
             '                "is",\n'
             '                "that",\n'
             '                "where",\n'
             '                "whispered",\n'
             '                "professor",\n'
             '                "mcgonagall"\n'
             '            ],\n'
             '            [\n'
             '                "yes",\n'
             '                "said",\n'
             '                "dumbledore",\n'
             '                "dumbledore",\n'
             '                "ll",\n'
             '                "have",\n'
             '                "that",\n'
             '                "scar",\n'
             '                "forever",\n'
             '                "couldn",\n'
             '                "t",\n'
             '                "you",\n'
             '                "do",\n'
             '                "something",\n'
             '                "about",\n'
             '                "scar",\n'
             '                "dumbledore",\n'
             '                "even",\n'
             '                "if",\n'
             '                "i",\n'
             '                "could",\n'
             '                "i",\n'
             '                "wouldn",\n'
             '                "t"\n'
             '            ]\n'
             '        ],\n'
             '        "Processed Names": []\n'
             '    }\n'
             '}')
data_str5 = ('{\n'
             '    "Question 1": {\n'
             '        "Processed Sentences": [\n'
             '            [\n'
             '                "marry",\n'
             '                "called",\n'
             '                "his",\n'
             '                "name"\n'
             '            ],\n'
             '            [\n'
             '                "max"\n'
             '            ]\n'
             '        ],\n'
             '        "Processed Names": [\n'
             '            [\n'
             '                [\n'
             '                    "bertram",\n'
             '                    "aubrey"\n'
             '                ],\n'
             '                []\n'
             '            ],\n'
             '            [\n'
             '                [\n'
             '                    "audrey",\n'
             '                    "weasley"\n'
             '                ],\n'
             '                []\n'
             '            ],\n'
             '            [\n'
             '                [\n'
             '                    "augusta",\n'
             '                    "gran",\n'
             '                    "longbottom"\n'
             '                ],\n'
             '                []\n'
             '            ],\n'
             '            [\n'
             '                [\n'
             '                    "augustus",\n'
             '                    "pye"\n'
             '                ],\n'
             '                []\n'
             '            ],\n'
             '            [\n'
             '                [\n'
             '                    "augustus",\n'
             '                    "rookwood"\n'
             '                ],\n'
             '                []\n'
             '            ],\n'
             '            [\n'
             '                [\n'
             '                    "augustus",\n'
             '                    "worme"\n'
             '                ],\n'
             '                []\n'
             '            ],\n'
             '            [\n'
             '                [\n'
             '                    "auntie",\n'
             '                    "muriel"\n'
             '                ],\n'
             '                []\n'
             '            ],\n'
             '            [\n'
             '                [\n'
             '                    "aunt",\n'
             '                    "marge",\n'
             '                    "dursley"\n'
             '                ],\n'
             '                []\n'
             '            ],\n'
             '            [\n'
             '                [\n'
             '                    "aurelius",\n'
             '                    "dumbledore"\n'
             '                ],\n'
             '                []\n'
             '            ],\n'
             '            [\n'
             '                [\n'
             '                    "aurora",\n'
             '                    "sinistra"\n'
             '                ],\n'
             '                []\n'
             '            ],\n'
             '            [\n'
             '                [\n'
             '                    "avery"\n'
             '                ],\n'
             '                []\n'
             '            ],\n'
             '            [\n'
             '                [\n'
             '                    "babajide",\n'
             '                    "akingbade"\n'
             '                ],\n'
             '                []\n'
             '            ],\n'
             '            [\n'
             '                [\n'
             '                    "babayaga"\n'
             '                ],\n'
             '                []\n'
             '            ],\n'
             '            [\n'
             '                [\n'
             '                    "babbitty",\n'
             '                    "rabbitty"\n'
             '                ],\n'
             '                []\n'
             '            ],\n'
             '            [\n'
             '                [\n'
             '                    "bagman",\n'
             '                    "sr"\n'
             '                ],\n'
             '                []\n'
             '            ],\n'
             '            [\n'
             '                [\n'
             '                    "ludo",\n'
             '                    "bagman"\n'
             '                ],\n'
             '                []\n'
             '            ],\n'
             '            [\n'
             '                [\n'
             '                    "otto",\n'
             '                    "bagman"\n'
             '                ],\n'
             '                []\n'
             '            ],\n'
             '            [\n'
             '                [\n'
             '                    "millicent",\n'
             '                    "bagnold"\n'
             '                ],\n'
             '                []\n'
             '            ],\n'
             '            [\n'
             '                [\n'
             '                    "bathilda",\n'
             '                    "bagshot"\n'
             '                ],\n'
             '                [\n'
             '                    [\n'
             '                        "batty"\n'
             '                    ]\n'
             '                ]\n'
             '            ],\n'
             '            [\n'
             '                [\n'
             '                    "kquewanda",\n'
             '                    "bailey"\n'
             '                ],\n'
             '                []\n'
             '            ]\n'
             '        ]\n'
             '    }\n'
             '}')
data_str6 = ('{\n'
             '    "Question 1": {\n'
             '        "Processed Sentences": [\n'
             '            [\n'
             '                "marry",\n'
             '                "called",\n'
             '                "his",\n'
             '                "name"\n'
             '            ],\n'
             '            [\n'
             '                "max"\n'
             '            ]\n'
             '        ],\n'
             '        "Processed Names": [\n'
             '            [\n'
             '                [\n'
             '                    "attentive",\n'
             '                    "wizard"\n'
             '                ],\n'
             '                []\n'
             '            ],\n'
             '            [\n'
             '                [\n'
             '                    "bertram",\n'
             '                    "aubrey"\n'
             '                ],\n'
             '                []\n'
             '            ],\n'
             '            [\n'
             '                [\n'
             '                    "audrey",\n'
             '                    "weasley"\n'
             '                ],\n'
             '                []\n'
             '            ],\n'
             '            [\n'
             '                [\n'
             '                    "augusta",\n'
             '                    "gran",\n'
             '                    "longbottom"\n'
             '                ],\n'
             '                []\n'
             '            ],\n'
             '            [\n'
             '                [\n'
             '                    "augustus",\n'
             '                    "pye"\n'
             '                ],\n'
             '                []\n'
             '            ],\n'
             '            [\n'
             '                [\n'
             '                    "augustus",\n'
             '                    "rookwood"\n'
             '                ],\n'
             '                []\n'
             '            ],\n'
             '            [\n'
             '                [\n'
             '                    "augustus",\n'
             '                    "worme"\n'
             '                ],\n'
             '                []\n'
             '            ],\n'
             '            [\n'
             '                [\n'
             '                    "auntie",\n'
             '                    "muriel"\n'
             '                ],\n'
             '                []\n'
             '            ],\n'
             '            [\n'
             '                [\n'
             '                    "aunt",\n'
             '                    "marge",\n'
             '                    "dursley"\n'
             '                ],\n'
             '                []\n'
             '            ],\n'
             '            [\n'
             '                [\n'
             '                    "aurelius",\n'
             '                    "dumbledore"\n'
             '                ],\n'
             '                []\n'
             '            ],\n'
             '            [\n'
             '                [\n'
             '                    "aurora",\n'
             '                    "sinistra"\n'
             '                ],\n'
             '                []\n'
             '            ],\n'
             '            [\n'
             '                [\n'
             '                    "avery"\n'
             '                ],\n'
             '                []\n'
             '            ],\n'
             '            [\n'
             '                [\n'
             '                    "babajide",\n'
             '                    "akingbade"\n'
             '                ],\n'
             '                []\n'
             '            ],\n'
             '            [\n'
             '                [\n'
             '                    "babayaga"\n'
             '                ],\n'
             '                []\n'
             '            ],\n'
             '            [\n'
             '                [\n'
             '                    "babbitty",\n'
             '                    "rabbitty"\n'
             '                ],\n'
             '                []\n'
             '            ],\n'
             '            [\n'
             '                [\n'
             '                    "bagman",\n'
             '                    "sr"\n'
             '                ],\n'
             '                []\n'
             '            ],\n'
             '            [\n'
             '                [\n'
             '                    "ludo",\n'
             '                    "bagman"\n'
             '                ],\n'
             '                []\n'
             '            ],\n'
             '            [\n'
             '                [\n'
             '                    "otto",\n'
             '                    "bagman"\n'
             '                ],\n'
             '                []\n'
             '            ],\n'
             '            [\n'
             '                [\n'
             '                    "millicent",\n'
             '                    "bagnold"\n'
             '                ],\n'
             '                []\n'
             '            ],\n'
             '            [\n'
             '                [\n'
             '                    "bathilda",\n'
             '                    "bagshot"\n'
             '                ],\n'
             '                [\n'
             '                    [\n'
             '                        "batty"\n'
             '                    ]\n'
             '                ]\n'
             '            ],\n'
             '            [\n'
             '                [\n'
             '                    "kquewanda",\n'
             '                    "bailey"\n'
             '                ],\n'
             '                []\n'
             '            ]\n'
             '        ]\n'
             '    }\n'
             '}')


def test_results():
    assert parser1.return_results() == data_str
    assert parser2.return_results() == data_str2
    assert parser3.return_results() == data_str3
    assert parser4.return_results() == data_str4
    assert parser5.return_results() == data_str5
    assert parser6.return_results() == data_str6

