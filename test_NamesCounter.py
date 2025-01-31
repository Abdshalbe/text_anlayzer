from NamesCounter import NamesCounter
from test_SequinceCounter import *

names_list1 = [['Alix "dan', 'Professor, The Smarter person'], ['Bagman Sr.', ''],
               ['Ludo Bagman', ''], ['Otto Bagman', ''], ['Millicent Bagnold', ''],
               ['Bathilda Bagshot', 'batty'], ['Kquewanda Bailey', ''],
               ['Ballyfumble Stranger', '"quin, quivering quintus, quintusofthesillyname"']]
names_list2 = [['Malcolm Baddock', ''], ['Malcolm McGonagall', ''], ['Harold Skively', ''], ['Harper', ''],
               ['Harry Potter',
                '"the boy who lived, undesirable number one, the chosen one, parry otter, the chosen boy, '
                'the mudbloods friend"'],
               ['Harvey Ridgebit', ''], ['Hassan Mostafa', ''], ['kathrin', 'cathy', 'cath']]
names_list3 = []

text1 = [['Alix is a will known person'], ['he learn from Malcolm'], ['mallcom is will known mathmtican professor'],
         ['bagman learned from the smarter person'], ['the smarter']]
text2 = []
text3 = [['mallcom was best friend of harry'], ['but harry was best friend of cathy']]

remvoe_words = [['the'], ['of'], ['but'], ['is'], ['a']]

people_names1_file = create_temp_csv(names_list1, ["Name", "Other Names"])
people_names2_file = create_temp_csv(names_list2, ["Name", "Other Names"])
people_names3_file = create_temp_csv(names_list3, ["Name", "Other Names"])
csv_sentence1 = create_temp_csv(text1, ["sentence"])
csv_sentence2 = create_temp_csv(text2, ["sentence"])
csv_sentence3 = create_temp_csv(text3, ["sentence"])
csv_remved = create_temp_csv(remvoe_words, ["words"])

json1 = process_json_data(Parser(1, peopleInputPath=people_names1_file, sentenceInputPath=csv_sentence1,
                                 removeInputPath=csv_remved).return_results())
json2 = process_json_data(Parser(1, peopleInputPath=people_names2_file, sentenceInputPath=csv_sentence1,
                                 removeInputPath=csv_remved).return_results())
json3 = process_json_data(Parser(1, peopleInputPath=people_names3_file, sentenceInputPath=csv_sentence1,
                                 removeInputPath=csv_remved).return_results())
json4 = process_json_data(Parser(1, peopleInputPath=people_names1_file, sentenceInputPath=csv_sentence2,
                                 removeInputPath=csv_remved).return_results())
json5 = process_json_data(Parser(1, peopleInputPath=people_names2_file, sentenceInputPath=csv_sentence2,
                                 removeInputPath=csv_remved).return_results())
json6 = process_json_data(Parser(1, peopleInputPath=people_names3_file, sentenceInputPath=csv_sentence2,
                                 removeInputPath=csv_remved).return_results())
json7 = process_json_data(Parser(1, peopleInputPath=people_names1_file, sentenceInputPath=csv_sentence3,
                                 removeInputPath=csv_remved).return_results())
json8 = process_json_data(Parser(1, peopleInputPath=people_names2_file, sentenceInputPath=csv_sentence3,
                                 removeInputPath=csv_remved).return_results())
json9 = process_json_data(Parser(1, peopleInputPath=people_names3_file, sentenceInputPath=csv_sentence3,
                                 removeInputPath=csv_remved).return_results())


def test_equal_csr():
    """
    Test the equality of two CSRs of the text and names and removal
    :return: failed or not (True/False)
    """
    assert NamesCounter(QNum=3, json_input_path=json1, preprocessed=True).return_results() == NamesCounter(3,
                                                                                                           people_input_path=people_names1_file,
                                                                                                           sentence_input_path=csv_sentence1,
                                                                                                           remove_input_path=csv_remved).return_results()
    assert NamesCounter(QNum=3, json_input_path=json2, preprocessed=True).return_results() == NamesCounter(3,
                                                                                                           people_input_path=people_names2_file,
                                                                                                           sentence_input_path=csv_sentence1,
                                                                                                           remove_input_path=csv_remved).return_results()
    assert NamesCounter(QNum=3, json_input_path=json3, preprocessed=True).return_results() == NamesCounter(3,
                                                                                                           people_input_path=people_names3_file,
                                                                                                           sentence_input_path=csv_sentence1,
                                                                                                           remove_input_path=csv_remved).return_results()
    assert NamesCounter(QNum=3, json_input_path=json4, preprocessed=True).return_results() == NamesCounter(3,
                                                                                                           people_input_path=people_names1_file,
                                                                                                           sentence_input_path=csv_sentence2,
                                                                                                           remove_input_path=csv_remved).return_results()
    assert NamesCounter(QNum=3, json_input_path=json5, preprocessed=True).return_results() == NamesCounter(3,
                                                                                                           people_input_path=people_names2_file,
                                                                                                           sentence_input_path=csv_sentence2,
                                                                                                           remove_input_path=csv_remved).return_results()
    assert NamesCounter(QNum=3, json_input_path=json6, preprocessed=True).return_results() == NamesCounter(3,
                                                                                                           people_input_path=people_names3_file,
                                                                                                           sentence_input_path=csv_sentence2,
                                                                                                           remove_input_path=csv_remved).return_results()
    assert NamesCounter(QNum=3, json_input_path=json7, preprocessed=True).return_results() == NamesCounter(3,
                                                                                                           people_input_path=people_names1_file,
                                                                                                           sentence_input_path=csv_sentence3,
                                                                                                           remove_input_path=csv_remved).return_results()
    assert NamesCounter(QNum=3, json_input_path=json8, preprocessed=True).return_results() == NamesCounter(3,
                                                                                                           people_input_path=people_names2_file,
                                                                                                           sentence_input_path=csv_sentence3,
                                                                                                           remove_input_path=csv_remved).return_results()
    assert NamesCounter(QNum=3, json_input_path=json9, preprocessed=True).return_results() == NamesCounter(3,
                                                                                                           people_input_path=people_names3_file,
                                                                                                           sentence_input_path=csv_sentence3,
                                                                                                           remove_input_path=csv_remved).return_results()
    assert NamesCounter(QNum=3, json_input_path=json1, preprocessed=True).count_names() == NamesCounter(3,
                                                                                                        people_input_path=people_names1_file,
                                                                                                        sentence_input_path=csv_sentence1,
                                                                                                        remove_input_path=csv_remved).count_names()
    assert NamesCounter(QNum=3, json_input_path=json2, preprocessed=True).count_names() == NamesCounter(3,
                                                                                                        people_input_path=people_names2_file,
                                                                                                        sentence_input_path=csv_sentence1,
                                                                                                        remove_input_path=csv_remved).count_names()
    assert NamesCounter(QNum=3, json_input_path=json3, preprocessed=True).count_names() == NamesCounter(3,
                                                                                                        people_input_path=people_names3_file,
                                                                                                        sentence_input_path=csv_sentence1,
                                                                                                        remove_input_path=csv_remved).count_names()
    assert NamesCounter(QNum=3, json_input_path=json4, preprocessed=True).count_names() == NamesCounter(3,
                                                                                                        people_input_path=people_names1_file,
                                                                                                        sentence_input_path=csv_sentence2,
                                                                                                        remove_input_path=csv_remved).count_names()
    assert NamesCounter(QNum=3, json_input_path=json5, preprocessed=True).count_names() == NamesCounter(3,
                                                                                                        people_input_path=people_names2_file,
                                                                                                        sentence_input_path=csv_sentence2,
                                                                                                        remove_input_path=csv_remved).count_names()
    assert NamesCounter(QNum=3, json_input_path=json6, preprocessed=True).count_names() == NamesCounter(3,
                                                                                                        people_input_path=people_names3_file,
                                                                                                        sentence_input_path=csv_sentence2,
                                                                                                        remove_input_path=csv_remved).count_names()
    assert NamesCounter(QNum=3, json_input_path=json7, preprocessed=True).count_names() == NamesCounter(3,
                                                                                                        people_input_path=people_names1_file,
                                                                                                        sentence_input_path=csv_sentence3,
                                                                                                        remove_input_path=csv_remved).count_names()
    assert NamesCounter(QNum=3, json_input_path=json8, preprocessed=True).count_names() == NamesCounter(3,
                                                                                                        people_input_path=people_names2_file,
                                                                                                        sentence_input_path=csv_sentence3,
                                                                                                        remove_input_path=csv_remved).count_names()
    assert NamesCounter(QNum=3, json_input_path=json9, preprocessed=True).count_names() == NamesCounter(3,
                                                                                                        people_input_path=people_names3_file,
                                                                                                        sentence_input_path=csv_sentence3,
                                                                                                        remove_input_path=csv_remved).count_names()


def test_count_names():
    assert NamesCounter(QNum=3, json_input_path=json1, preprocessed=True).count_names() == (
        {'alix dan': 3, 'bagman sr': 1, 'ludo bagman': 1, 'otto bagman': 1},
        {'alix dan': [0, 2, 3], 'bagman sr': [3], 'ludo bagman': [3], 'otto bagman': [3]})
    assert NamesCounter(QNum=3, people_input_path=people_names2_file, sentence_input_path=csv_sentence1,
                        remove_input_path=csv_remved).count_names() == (
               {'malcolm baddock': 1, 'malcolm mcgonagall': 1}, {'malcolm baddock': [1], 'malcolm mcgonagall': [1]})
    assert NamesCounter(QNum=3, json_input_path=json3, preprocessed=True).count_names() == ({}, {})
    assert NamesCounter(QNum=3, people_input_path=people_names1_file, sentence_input_path=csv_sentence2,
                        remove_input_path=csv_remved).count_names() == ({}, {})
    assert NamesCounter(QNum=3, json_input_path=json5, preprocessed=True).count_names() == ({}, {})
    assert NamesCounter(QNum=3, json_input_path=json7, preprocessed=True).count_names() == ({}, {})
    assert NamesCounter(QNum=3, people_input_path=people_names2_file, sentence_input_path=csv_sentence3,
                        remove_input_path=csv_remved).count_names() == (
               {'harry potter': 2, 'kathrin': 1}, {'harry potter': [0, 1], 'kathrin': [1]})
    assert NamesCounter(QNum=3, json_input_path=json9, preprocessed=True).count_names() == ({}, {})


def test_result():
    result1 = ('{\n'
               '    "Question 3": {\n'
               '        "Name Mentions": [\n'
               '            [\n'
               '                "alix dan",\n'
               '                3\n'
               '            ],\n'
               '            [\n'
               '                "bagman sr",\n'
               '                1\n'
               '            ],\n'
               '            [\n'
               '                "ludo bagman",\n'
               '                1\n'
               '            ],\n'
               '            [\n'
               '                "otto bagman",\n'
               '                1\n'
               '            ]\n'
               '        ]\n'
               '    }\n'
               '}')
    result2 = ('{\n'
               '    "Question 3": {\n'
               '        "Name Mentions": [\n'
               '            [\n'
               '                "malcolm baddock",\n'
               '                1\n'
               '            ],\n'
               '            [\n'
               '                "malcolm mcgonagall",\n'
               '                1\n'
               '            ]\n'
               '        ]\n'
               '    }\n'
               '}')
    result3 = '{\n    "Question 3": {\n        "Name Mentions": []\n    }\n}'
    result4 = ('{\n'
               '    "Question 3": {\n'
               '        "Name Mentions": [\n'
               '            [\n'
               '                "harry potter",\n'
               '                2\n'
               '            ],\n'
               '            [\n'
               '                "kathrin",\n'
               '                1\n'
               '            ]\n'
               '        ]\n'
               '    }\n'
               '}')

    assert NamesCounter(QNum=3, json_input_path=json1, preprocessed=True).return_results() == result1
    assert NamesCounter(QNum=3, people_input_path=people_names2_file, sentence_input_path=csv_sentence1,
                        remove_input_path=csv_remved).return_results() == result2
    assert NamesCounter(QNum=3, json_input_path=json3, preprocessed=True).return_results() == result3
    assert NamesCounter(QNum=3, people_input_path=people_names1_file, sentence_input_path=csv_sentence2,
                        remove_input_path=csv_remved).return_results() == result3
    assert NamesCounter(QNum=3, json_input_path=json5, preprocessed=True).return_results() == result3
    assert NamesCounter(QNum=3, json_input_path=json7, preprocessed=True).return_results() == result3
    assert NamesCounter(QNum=3, people_input_path=people_names2_file, sentence_input_path=csv_sentence3,
                        remove_input_path=csv_remved).return_results() == result4
    assert NamesCounter(QNum=3, json_input_path=json9, preprocessed=True).return_results() == result3
