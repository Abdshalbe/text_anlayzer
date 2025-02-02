from SentencesGraph import *
from test_CheckConnection import *

empty_file = []

no_shared_words = [["Harry Potter was sitting alone in the library."],
                   ["Professor McGonagall was walking down the hallway, reading a letter."],
                   ["Draco Malfoy was practicing spells in an empty classroom."],
                   ["Albus Dumbledore was observing the students from his office."]]

no_shared_words2 = [["Harry Potter was sitting in the library reading a book."],
                    ["Professor Snape was brewing a potion in the dungeon."],
                    ["Draco Malfoy was practicing spells in an empty classroom."],
                    ["Albus Dumbledore observed the students from his office."]]

no_shared_words3 = [["The sun set behind the mountains."], ["Rain fell softly on the rooftops."],
                    ["A bird flew across the sky at dawn."], ["The ocean waves crashed on the shore."]]

shared1_word = [["The cat sat on the mat."], ["The dog ran across the street."], ["The cat jumped on the roof."],
                ["The dog barked loudly."]]

shared1_word_2 = [["The sun rises in the east."], ["The moon shines brightly in the sky moon."],
                  ["The sun sets in the west."], ["The stars twinkle at night."]]

shared_words = [["The cat sat on the mat."], ["The dog ran across the mat."], ["She sat next to the cat on the mat."],
                ["The dog chased the cat around the yard."], ["The mat was in the living room."]]

shared_word_2 = [["John went to the store to buy some milk."], ["Susan visited the store after work."],
                 ["Mark likes to go to the gym on Sundays."], ["John and Susan met at the store and talked."],
                 ["Mark and John went to the gym together."]]

remove_words = [['on'], ['the'], ['to'], ['and'], ['at'], ['in'], ['a'], ['at'], ['was'], ['an'], ['from']]

empty_file_csv = create_temp_csv_with_data(empty_file, ['sentence'])
no_shared_words1_csv = create_temp_csv_with_data(no_shared_words, ['sentence'])
no_shared_words2_csv = create_temp_csv_with_data(no_shared_words2, ['sentence'])
no_shared_words3_csv = create_temp_csv_with_data(no_shared_words3, ['sentence'])
shared1_word_csv = create_temp_csv_with_data(shared1_word, ['sentence'])
shared1_word_2_csv = create_temp_csv_with_data(shared1_word_2, ['sentence'])
shared_words_csv = create_temp_csv_with_data(shared_words, ['sentence'])
shared_words_2_csv = create_temp_csv_with_data(shared_word_2, ['sentence'])
remove_words_csv = create_temp_csv_with_data(remove_words, ['word'])

json_file1 = process_json_data(
    Parser(1, removeInputPath=remove_words_csv, sentenceInputPath=empty_file_csv).return_results())
json_file2 = process_json_data(
    Parser(1, removeInputPath=remove_words_csv, sentenceInputPath=no_shared_words1_csv).return_results())
json_file3 = process_json_data(
    Parser(1, removeInputPath=remove_words_csv, sentenceInputPath=no_shared_words2_csv).return_results())
json_file4 = process_json_data(
    Parser(1, removeInputPath=remove_words_csv, sentenceInputPath=no_shared_words3_csv).return_results())
json_file5 = process_json_data(
    Parser(1, removeInputPath=remove_words_csv, sentenceInputPath=shared1_word_csv).return_results())
json_file6 = process_json_data(
    Parser(1, removeInputPath=remove_words_csv, sentenceInputPath=shared1_word_2_csv).return_results())
json_file7 = process_json_data(
    Parser(1, removeInputPath=remove_words_csv, sentenceInputPath=shared_words_csv).return_results())
json_file8 = process_json_data(
    Parser(1, removeInputPath=remove_words_csv, sentenceInputPath=shared_words_2_csv).return_results())


def test_equal_cstr():
    """
    Test the instillation using json or csv files are equal
    """
    assert SentenceGraph(9, sentence_input_path=empty_file_csv, remove_input_path=remove_words_csv,
                         threshold=2).return_results() == SentenceGraph(9, json_input_path=json_file1,
                                                                        preprocessed=True, threshold=2).return_results()
    assert SentenceGraph(9, sentence_input_path=no_shared_words1_csv, remove_input_path=remove_words_csv,
                         threshold=4).return_results() == SentenceGraph(9, json_input_path=json_file2,
                                                                        preprocessed=True, threshold=4).return_results()
    assert SentenceGraph(9, sentence_input_path=no_shared_words2_csv, remove_input_path=remove_words_csv,
                         threshold=3).return_results() == SentenceGraph(9, json_input_path=json_file3,
                                                                        preprocessed=True, threshold=3).return_results()
    assert SentenceGraph(9, sentence_input_path=no_shared_words3_csv, remove_input_path=remove_words_csv,
                         threshold=1).return_results() == SentenceGraph(9, json_input_path=json_file4,
                                                                        preprocessed=True, threshold=1).return_results()
    assert SentenceGraph(9, sentence_input_path=shared1_word_csv, remove_input_path=remove_words_csv,
                         threshold=2).return_results() == SentenceGraph(9, json_input_path=json_file5,
                                                                        preprocessed=True, threshold=2).return_results()
    assert SentenceGraph(9, sentence_input_path=shared1_word_2_csv, remove_input_path=remove_words_csv,
                         threshold=3).return_results() == SentenceGraph(9, json_input_path=json_file6,
                                                                        preprocessed=True, threshold=3).return_results()
    assert SentenceGraph(9, sentence_input_path=shared_words_csv, remove_input_path=remove_words_csv,
                         threshold=2).return_results() == SentenceGraph(9, json_input_path=json_file7,
                                                                        preprocessed=True, threshold=2).return_results()
    assert SentenceGraph(9, sentence_input_path=shared_words_2_csv, remove_input_path=remove_words_csv,
                         threshold=1).return_results() == SentenceGraph(9, json_input_path=json_file8,
                                                                        preprocessed=True, threshold=1).return_results()

def test_SentenceGraph_results():
    empty_res = '{\n    "Question 9": {\n        "group Matches": []\n    }\n}'
    res1 = ('{\n'
            '    "Question 9": {\n'
            '        "group Matches": [\n'
            '            [\n'
            '                "Group 1",\n'
            '                [\n'
            '                    [\n'
            '                        "albus",\n'
            '                        "dumbledore",\n'
            '                        "observing",\n'
            '                        "students",\n'
            '                        "his",\n'
            '                        "office"\n'
            '                    ]\n'
            '                ]\n'
            '            ],\n'
            '            [\n'
            '                "Group 2",\n'
            '                [\n'
            '                    [\n'
            '                        "draco",\n'
            '                        "malfoy",\n'
            '                        "practicing",\n'
            '                        "spells",\n'
            '                        "empty",\n'
            '                        "classroom"\n'
            '                    ]\n'
            '                ]\n'
            '            ],\n'
            '            [\n'
            '                "Group 3",\n'
            '                [\n'
            '                    [\n'
            '                        "harry",\n'
            '                        "potter",\n'
            '                        "sitting",\n'
            '                        "alone",\n'
            '                        "library"\n'
            '                    ]\n'
            '                ]\n'
            '            ],\n'
            '            [\n'
            '                "Group 4",\n'
            '                [\n'
            '                    [\n'
            '                        "professor",\n'
            '                        "mcgonagall",\n'
            '                        "walking",\n'
            '                        "down",\n'
            '                        "hallway",\n'
            '                        "reading",\n'
            '                        "letter"\n'
            '                    ]\n'
            '                ]\n'
            '            ]\n'
            '        ]\n'
            '    }\n'
            '}')
    res2 = ('{\n'
            '    "Question 9": {\n'
            '        "group Matches": [\n'
            '            [\n'
            '                "Group 1",\n'
            '                [\n'
            '                    [\n'
            '                        "albus",\n'
            '                        "dumbledore",\n'
            '                        "observed",\n'
            '                        "students",\n'
            '                        "his",\n'
            '                        "office"\n'
            '                    ]\n'
            '                ]\n'
            '            ],\n'
            '            [\n'
            '                "Group 2",\n'
            '                [\n'
            '                    [\n'
            '                        "draco",\n'
            '                        "malfoy",\n'
            '                        "practicing",\n'
            '                        "spells",\n'
            '                        "empty",\n'
            '                        "classroom"\n'
            '                    ]\n'
            '                ]\n'
            '            ],\n'
            '            [\n'
            '                "Group 3",\n'
            '                [\n'
            '                    [\n'
            '                        "harry",\n'
            '                        "potter",\n'
            '                        "sitting",\n'
            '                        "library",\n'
            '                        "reading",\n'
            '                        "book"\n'
            '                    ]\n'
            '                ]\n'
            '            ],\n'
            '            [\n'
            '                "Group 4",\n'
            '                [\n'
            '                    [\n'
            '                        "professor",\n'
            '                        "snape",\n'
            '                        "brewing",\n'
            '                        "potion",\n'
            '                        "dungeon"\n'
            '                    ]\n'
            '                ]\n'
            '            ]\n'
            '        ]\n'
            '    }\n'
            '}')
    res3 = ('{\n'
            '    "Question 9": {\n'
            '        "group Matches": [\n'
            '            [\n'
            '                "Group 1",\n'
            '                [\n'
            '                    [\n'
            '                        "bird",\n'
            '                        "flew",\n'
            '                        "across",\n'
            '                        "sky",\n'
            '                        "dawn"\n'
            '                    ]\n'
            '                ]\n'
            '            ],\n'
            '            [\n'
            '                "Group 2",\n'
            '                [\n'
            '                    [\n'
            '                        "ocean",\n'
            '                        "waves",\n'
            '                        "crashed",\n'
            '                        "shore"\n'
            '                    ]\n'
            '                ]\n'
            '            ],\n'
            '            [\n'
            '                "Group 3",\n'
            '                [\n'
            '                    [\n'
            '                        "rain",\n'
            '                        "fell",\n'
            '                        "softly",\n'
            '                        "rooftops"\n'
            '                    ]\n'
            '                ]\n'
            '            ],\n'
            '            [\n'
            '                "Group 4",\n'
            '                [\n'
            '                    [\n'
            '                        "sun",\n'
            '                        "set",\n'
            '                        "behind",\n'
            '                        "mountains"\n'
            '                    ]\n'
            '                ]\n'
            '            ]\n'
            '        ]\n'
            '    }\n'
            '}')
    res4 = ('{\n'
            '    "Question 9": {\n'
            '        "group Matches": [\n'
            '            [\n'
            '                "Group 1",\n'
            '                [\n'
            '                    [\n'
            '                        "cat",\n'
            '                        "jumped",\n'
            '                        "roof"\n'
            '                    ]\n'
            '                ]\n'
            '            ],\n'
            '            [\n'
            '                "Group 2",\n'
            '                [\n'
            '                    [\n'
            '                        "cat",\n'
            '                        "sat",\n'
            '                        "mat"\n'
            '                    ]\n'
            '                ]\n'
            '            ],\n'
            '            [\n'
            '                "Group 3",\n'
            '                [\n'
            '                    [\n'
            '                        "dog",\n'
            '                        "barked",\n'
            '                        "loudly"\n'
            '                    ]\n'
            '                ]\n'
            '            ],\n'
            '            [\n'
            '                "Group 4",\n'
            '                [\n'
            '                    [\n'
            '                        "dog",\n'
            '                        "ran",\n'
            '                        "across",\n'
            '                        "street"\n'
            '                    ]\n'
            '                ]\n'
            '            ]\n'
            '        ]\n'
            '    }\n'
            '}')
    res5 = ('{\n'
            '    "Question 9": {\n'
            '        "group Matches": [\n'
            '            [\n'
            '                "Group 1",\n'
            '                [\n'
            '                    [\n'
            '                        "cat",\n'
            '                        "jumped",\n'
            '                        "roof"\n'
            '                    ],\n'
            '                    [\n'
            '                        "cat",\n'
            '                        "sat",\n'
            '                        "mat"\n'
            '                    ]\n'
            '                ]\n'
            '            ],\n'
            '            [\n'
            '                "Group 2",\n'
            '                [\n'
            '                    [\n'
            '                        "dog",\n'
            '                        "barked",\n'
            '                        "loudly"\n'
            '                    ],\n'
            '                    [\n'
            '                        "dog",\n'
            '                        "ran",\n'
            '                        "across",\n'
            '                        "street"\n'
            '                    ]\n'
            '                ]\n'
            '            ]\n'
            '        ]\n'
            '    }\n'
            '}')
    res6 = ('{\n'
            '    "Question 9": {\n'
            '        "group Matches": [\n'
            '            [\n'
            '                "Group 1",\n'
            '                [\n'
            '                    [\n'
            '                        "moon",\n'
            '                        "shines",\n'
            '                        "brightly",\n'
            '                        "sky",\n'
            '                        "moon"\n'
            '                    ]\n'
            '                ]\n'
            '            ],\n'
            '            [\n'
            '                "Group 2",\n'
            '                [\n'
            '                    [\n'
            '                        "stars",\n'
            '                        "twinkle",\n'
            '                        "night"\n'
            '                    ]\n'
            '                ]\n'
            '            ],\n'
            '            [\n'
            '                "Group 3",\n'
            '                [\n'
            '                    [\n'
            '                        "sun",\n'
            '                        "rises",\n'
            '                        "east"\n'
            '                    ]\n'
            '                ]\n'
            '            ],\n'
            '            [\n'
            '                "Group 4",\n'
            '                [\n'
            '                    [\n'
            '                        "sun",\n'
            '                        "sets",\n'
            '                        "west"\n'
            '                    ]\n'
            '                ]\n'
            '            ]\n'
            '        ]\n'
            '    }\n'
            '}')
    res7 = ('{\n'
            '    "Question 9": {\n'
            '        "group Matches": [\n'
            '            [\n'
            '                "Group 1",\n'
            '                [\n'
            '                    [\n'
            '                        "dog",\n'
            '                        "chased",\n'
            '                        "cat",\n'
            '                        "around",\n'
            '                        "yard"\n'
            '                    ]\n'
            '                ]\n'
            '            ],\n'
            '            [\n'
            '                "Group 2",\n'
            '                [\n'
            '                    [\n'
            '                        "dog",\n'
            '                        "ran",\n'
            '                        "across",\n'
            '                        "mat"\n'
            '                    ]\n'
            '                ]\n'
            '            ],\n'
            '            [\n'
            '                "Group 3",\n'
            '                [\n'
            '                    [\n'
            '                        "mat",\n'
            '                        "living",\n'
            '                        "room"\n'
            '                    ]\n'
            '                ]\n'
            '            ],\n'
            '            [\n'
            '                "Group 4",\n'
            '                [\n'
            '                    [\n'
            '                        "cat",\n'
            '                        "sat",\n'
            '                        "mat"\n'
            '                    ],\n'
            '                    [\n'
            '                        "she",\n'
            '                        "sat",\n'
            '                        "next",\n'
            '                        "cat",\n'
            '                        "mat"\n'
            '                    ]\n'
            '                ]\n'
            '            ]\n'
            '        ]\n'
            '    }\n'
            '}')
    res8 = ('{\n'
            '    "Question 9": {\n'
            '        "group Matches": [\n'
            '            [\n'
            '                "Group 1",\n'
            '                [\n'
            '                    [\n'
            '                        "john",\n'
            '                        "susan",\n'
            '                        "met",\n'
            '                        "store",\n'
            '                        "talked"\n'
            '                    ],\n'
            '                    [\n'
            '                        "john",\n'
            '                        "went",\n'
            '                        "store",\n'
            '                        "buy",\n'
            '                        "some",\n'
            '                        "milk"\n'
            '                    ],\n'
            '                    [\n'
            '                        "mark",\n'
            '                        "john",\n'
            '                        "went",\n'
            '                        "gym",\n'
            '                        "together"\n'
            '                    ],\n'
            '                    [\n'
            '                        "mark",\n'
            '                        "likes",\n'
            '                        "go",\n'
            '                        "gym",\n'
            '                        "sundays"\n'
            '                    ],\n'
            '                    [\n'
            '                        "susan",\n'
            '                        "visited",\n'
            '                        "store",\n'
            '                        "after",\n'
            '                        "work"\n'
            '                    ]\n'
            '                ]\n'
            '            ]\n'
            '        ]\n'
            '    }\n'
            '}')
    assert SentenceGraph(9, sentence_input_path=empty_file_csv, remove_input_path=remove_words_csv,
                         threshold=2).return_results() == empty_res
    assert SentenceGraph(9, sentence_input_path=no_shared_words1_csv, remove_input_path=remove_words_csv,
                         threshold=4).return_results() == res1
    assert SentenceGraph(9, sentence_input_path=no_shared_words2_csv, remove_input_path=remove_words_csv,
                         threshold=1).return_results() == res2
    assert SentenceGraph(9, sentence_input_path=no_shared_words3_csv, remove_input_path=remove_words_csv,
                         threshold=1).return_results() == res3
    assert SentenceGraph(9, sentence_input_path=shared1_word_csv, remove_input_path=remove_words_csv,
                         threshold=2).return_results() == res4  # double words counted once
    assert SentenceGraph(9, sentence_input_path=shared1_word_csv, remove_input_path=remove_words_csv,
                         threshold=1).return_results() == res5
    assert SentenceGraph(9, sentence_input_path=shared1_word_2_csv, remove_input_path=remove_words_csv,
                         threshold=3).return_results() == res6
    assert SentenceGraph(9, sentence_input_path=shared_words_csv, remove_input_path=remove_words_csv,
                         threshold=2).return_results() == res7
    assert SentenceGraph(9, sentence_input_path=shared_words_2_csv, remove_input_path=remove_words_csv,
                         threshold=1).return_results() == res8
