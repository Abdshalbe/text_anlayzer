from CheckConnection import *
from test_PeopleConnectionGraph import *
from PeopleConnectionGraph import PeopleConnectionGraph

json_data = {
    "keys": [
        ["harry potter", "aurelius dumbledore"],
        ["hermione granger", "draco malfoy"],
        ["hermione granger", "harry potter"]
    ]
}
json_data1 = {
    "keys": [["cristiano ronaldo", "lionel messi"],
             ["harry maguire", "harry cane"],
             ["harry potter", "ron weasley"],
             ["donald trump", "joe biden"]]
}
json_key_file = process_json_data(json.dumps(json_data))
json_key_file1 = process_json_data(json.dumps(json_data1))


def test_extract_keys_from_json():
    assert extract_keys_from_json(json_key_file) == [
        ["harry potter", "aurelius dumbledore"],
        ["hermione granger", "draco malfoy"],
        ["hermione granger", "harry potter"]
    ]
    assert extract_keys_from_json(json_key_file1) == [
        ["cristiano ronaldo", "lionel messi"],
        ["harry maguire", "harry cane"],
        ["harry potter", "ron weasley"],
        ["donald trump", "joe biden"]
    ]


sentence_lest1 = [[
    '''In the Hogwarts library, Harry Potter, Hermione Granger, and Ron Weasley were studying for their upcoming exams. They had been preparing for weeks, and the pressure was mounting. "I can't believe how much we've studied," Hermione said, adjusting her glasses. "It feels like we've been here forever!"'''],
    [
        'Meanwhile, Neville Longbottom was across the room, struggling with a spell. "I’ll never get this right," he muttered to himself. Luna Lovegood, sitting nearby, overheard and offered to help. "Neville, don’t worry," she said with a gentle smile. "You’ll get it eventually."'],
    [
        'Later, Harry Potter had to meet Professor Dumbledore to discuss something important. He walked toward the headmaster’s office, passing by Draco Malfoy and Pansy Parkinson, who were gossiping in the hallway. They sneered at Harry as he passed, but he ignored them, focusing on his meeting with Dumbledore.'],
    ['''That evening, in the Great Hall, a loud argument broke out between Draco Malfoy and Ron Weasley. "You think 
you're better than me, don't you, Weasley?" Draco spat. Ron stood up to him, "Not in a million years, Malfoy!" The 
tension was palpable.'''],
    [
        'After the argument, Harry Potter, Ron Weasley, and Hermione Granger sat together, discussing the recent events. "We need to be careful," Harry said. "Things are starting to get out of hand."'],
    [
        'Luna Lovegood, who had joined them, nodded in agreement. "Yes, you never know who might be listening," she said cryptically.']]
people_list = [['Harry Potter', ' "The boy who lived"'],
               ['Hermione Granger', '"Granger, the know-it-all"'],
               ['"Ron Weasley"', '"Weasley, the redhead"'],
               ['Neville Longbottom', '"Neville"'],
               ['Luna Lovegood', '"Luna"'],
               ['Professor McGonagall', '"Minerva"'],
               ['Draco Malfoy', "Draco"]]
remove_words = [
    ['a'], ['and'], ['the'], ['is'], ['it'], ['of'], ['in'], ['to']
    , ['was'], ['were'], ['he'], ['she'], ['his'], ['her'], ['they'], ['for'], ['on']]
json_data2 = {"keys": [
    ["Harry Potter", "Hermione Granger"],
    ["Hermione Granger", "Ron Weasley"],
    ["Harry Potter", "Ron Weasley"],
    ["Harry Potter", "Professor Dumbledore"],
    ["Ron Weasley", "Professor Dumbledore"],
    ["Luna Lovegood", "Neville Longbottom"],
    ["Luna Lovegood", "Ron Weasley"],
    ["Neville Longbottom", "Ron Weasley"],
    ["Harry Potter", "Luna Lovegood"],
    ["Draco Malfoy", "Ron Weasley"]]}
json_data3 = {"keys": [["cristiano ronaldo", "lionel messi"],
                       ["harry maguire", "harry cane"],
                       ["harry potter", "ron weasley"],
                       ["donald trump", "joe biden"]]}

people_list2 = [["Cristiano Ronaldo", ''], ["lionel messi", ''],
                ["harry maguire", ''], ["harry cane", ''],
                ["Donald Trump", 'golden'], ["Joe Biden", '']]

text1 = [['Ronaldo is on of the most known persons in the sport indenture'],
         ['like his friend lionel messi ,cristiano have many brands'],
         ['but some football players does not have any brands like cane and maguire'],
         ['but cristiano an like messi  have not any political friends like joe and golden']]

people_list_scv = create_temp_csv_with_data(people_list, ['Name', 'Other Names'])
sentence_lest1_scv = create_temp_csv_with_data(sentence_lest1, ['sentence'])
people_list2_scv = create_temp_csv_with_data(people_list2, ['Name', 'Other Names'])
sentence_lest2_scv = create_temp_csv_with_data(text1, ['sentence'])
sentence_remove_scv = create_temp_csv_with_data(remove_words, ['words'])
keys_json = process_json_data(json.dumps(json_data2))
keys_json2 = process_json_data(json.dumps(json_data1))

json_file = process_json_data(
    PeopleConnectionGraph(QNum=6, people_input_path=people_list_scv, remove_input_path=sentence_remove_scv,
                          sentence_input_path=sentence_lest1_scv, WindowSize=4, Threshold=1).return_results())
json_file_to_comp = process_json_data(
    PeopleConnectionGraph(QNum=6, people_input_path=people_list2_scv, remove_input_path=sentence_remove_scv,
                          sentence_input_path=sentence_lest2_scv, WindowSize=2, Threshold=1).return_results())


def equalCtr():
    """
    test that the constructor of task 7 with json or with csv are equal
    """
    assert CheckConnection(7, people_input_path=people_list_scv, remove_input_path=sentence_remove_scv,
                           sentence_input_path=sentence_lest1_scv, WindowSize=2, Threshold=1,
                           People_connections_to_check=keys_json,
                           Maximal_distance=5).return_results() == CheckConnection(7,
                                                                                   jsonInputFile=json_file,
                                                                                   preprocessed=True,
                                                                                   People_connections_to_check=keys_json,
                                                                                   Maximal_distance=5).return_results()
    assert CheckConnection(7, people_input_path=people_list_scv, remove_input_path=sentence_remove_scv,
                           sentence_input_path=sentence_lest1_scv, WindowSize=2, Threshold=1,
                           People_connections_to_check=keys_json,
                           Maximal_distance=4).return_results() == CheckConnection(7,
                                                                                   jsonInputFile=json_file,
                                                                                   preprocessed=True,
                                                                                   People_connections_to_check=keys_json,
                                                                                   Maximal_distance=4).return_results()
    assert CheckConnection(7, people_input_path=people_list_scv, remove_input_path=sentence_remove_scv,
                           sentence_input_path=sentence_lest1_scv, WindowSize=2, Threshold=1,
                           People_connections_to_check=keys_json,
                           Maximal_distance=3).return_results() == CheckConnection(7,
                                                                                   jsonInputFile=json_file,
                                                                                   preprocessed=True,
                                                                                   People_connections_to_check=keys_json,
                                                                                   Maximal_distance=3).return_results()
    assert CheckConnection(7, people_input_path=people_list2_scv, remove_input_path=sentence_remove_scv,
                           sentence_input_path=sentence_lest2_scv, WindowSize=2, Threshold=1,
                           People_connections_to_check=keys_json2,
                           Maximal_distance=5).return_results() == CheckConnection(7,
                                                                                   jsonInputFile=json_file_to_comp,
                                                                                   preprocessed=True,
                                                                                   People_connections_to_check=keys_json2,
                                                                                   Maximal_distance=5).return_results()
    assert CheckConnection(7, people_input_path=people_list2_scv, remove_input_path=sentence_remove_scv,
                           sentence_input_path=sentence_lest2_scv, WindowSize=2, Threshold=1,
                           People_connections_to_check=keys_json2,
                           Maximal_distance=4).return_results() == CheckConnection(7,
                                                                                   jsonInputFile=json_file_to_comp,
                                                                                   preprocessed=True,
                                                                                   People_connections_to_check=keys_json2,
                                                                                   Maximal_distance=4).return_results()
    assert CheckConnection(7, people_input_path=people_list2_scv, remove_input_path=sentence_remove_scv,
                           sentence_input_path=sentence_lest2_scv, WindowSize=2, Threshold=1,
                           People_connections_to_check=keys_json,
                           Maximal_distance=3).return_results() == CheckConnection(7,
                                                                                   jsonInputFile=json_file_to_comp,
                                                                                   preprocessed=True,
                                                                                   People_connections_to_check=keys_json2,
                                                                                   Maximal_distance=3).return_results()


def test_check_results_7():
    """
    test the result of task 7
    i tested the following conditions:
    Disconnected Graph: If the graph has no connections (isolated nodes), ensure that the check for indirect connections returns False for all pairs.
    Large Graph with Multiple Paths: Ensure the program correctly identifies indirect connections even if multiple paths exist.
    No Path Found: Ensure the correct return of False if no path exists between two people.
    """
    result1 = ('{\n'
               '    "Question 7": {\n'
               '        "Pair Matches": [\n'
               '            [\n'
               '                "Draco Malfoy",\n'
               '                "Ron Weasley",\n'
               '                false\n'
               '            ],\n'
               '            [\n'
               '                "Harry Potter",\n'
               '                "Hermione Granger",\n'
               '                false\n'
               '            ],\n'
               '            [\n'
               '                "Harry Potter",\n'
               '                "Luna Lovegood",\n'
               '                false\n'
               '            ],\n'
               '            [\n'
               '                "Harry Potter",\n'
               '                "Professor Dumbledore",\n'
               '                false\n'
               '            ],\n'
               '            [\n'
               '                "Harry Potter",\n'
               '                "Ron Weasley",\n'
               '                false\n'
               '            ],\n'
               '            [\n'
               '                "Hermione Granger",\n'
               '                "Ron Weasley",\n'
               '                false\n'
               '            ],\n'
               '            [\n'
               '                "Luna Lovegood",\n'
               '                "Neville Longbottom",\n'
               '                false\n'
               '            ],\n'
               '            [\n'
               '                "Luna Lovegood",\n'
               '                "Ron Weasley",\n'
               '                false\n'
               '            ],\n'
               '            [\n'
               '                "Neville Longbottom",\n'
               '                "Ron Weasley",\n'
               '                false\n'
               '            ],\n'
               '            [\n'
               '                "Professor Dumbledore",\n'
               '                "Ron Weasley",\n'
               '                false\n'
               '            ]\n'
               '        ]\n'
               '    }\n'
               '}')
    result2 = ('{\n'
               '    "Question 7": {\n'
               '        "Pair Matches": [\n'
               '            [\n'
               '                "cristiano ronaldo",\n'
               '                "lionel messi",\n'
               '                true\n'
               '            ],\n'
               '            [\n'
               '                "donald trump",\n'
               '                "joe biden",\n'
               '                true\n'
               '            ],\n'
               '            [\n'
               '                "harry cane",\n'
               '                "harry maguire",\n'
               '                true\n'
               '            ],\n'
               '            [\n'
               '                "harry potter",\n'
               '                "ron weasley",\n'
               '                false\n'
               '            ]\n'
               '        ]\n'
               '    }\n'
               '}')
    result3 = ('{\n'
               '    "Question 7": {\n'
               '        "Pair Matches": [\n'
               '            [\n'
               '                "cristiano ronaldo",\n'
               '                "lionel messi",\n'
               '                true\n'
               '            ],\n'
               '            [\n'
               '                "donald trump",\n'
               '                "joe biden",\n'
               '                false\n'
               '            ],\n'
               '            [\n'
               '                "harry cane",\n'
               '                "harry maguire",\n'
               '                true\n'
               '            ],\n'
               '            [\n'
               '                "harry potter",\n'
               '                "ron weasley",\n'
               '                false\n'
               '            ]\n'
               '        ]\n'
               '    }\n'
               '}')
    assert CheckConnection(7, people_input_path=people_list_scv, remove_input_path=sentence_remove_scv,
                           sentence_input_path=sentence_lest1_scv, WindowSize=2, Threshold=1,
                           People_connections_to_check=keys_json, Maximal_distance=5).return_results() == result1
    #
    assert CheckConnection(7, people_input_path=people_list_scv, remove_input_path=sentence_remove_scv,
                           sentence_input_path=sentence_lest1_scv, WindowSize=7, Threshold=1,
                           People_connections_to_check=keys_json, Maximal_distance=4).return_results() == result1
    #
    assert CheckConnection(7, people_input_path=people_list_scv, remove_input_path=sentence_remove_scv,
                           sentence_input_path=sentence_lest1_scv, WindowSize=2, Threshold=1,
                           People_connections_to_check=keys_json, Maximal_distance=20).return_results() == result1

    assert CheckConnection(7, people_input_path=people_list_scv, remove_input_path=sentence_remove_scv,
                           sentence_input_path=sentence_lest1_scv, WindowSize=2, Threshold=1,
                           People_connections_to_check=keys_json, Maximal_distance=31).return_results() == result1

    assert CheckConnection(7, people_input_path=people_list2_scv, remove_input_path=sentence_remove_scv,
                           sentence_input_path=sentence_lest2_scv, WindowSize=4, Threshold=1,
                           People_connections_to_check=keys_json2, Maximal_distance=2).return_results() == result2
    assert CheckConnection(7, people_input_path=people_list2_scv, remove_input_path=sentence_remove_scv,
                           sentence_input_path=sentence_lest2_scv, WindowSize=2, Threshold=2,
                           People_connections_to_check=keys_json2, Maximal_distance=2).return_results() == result3


def test_equal_cstr():
    assert CheckConnection(8, people_input_path=people_list_scv, remove_input_path=sentence_remove_scv,
                           sentence_input_path=sentence_lest1_scv, WindowSize=2, Threshold=1,
                           People_connections_to_check=keys_json, fixed_length=True,
                           k=5).return_results() == CheckConnection(8,
                                                                    jsonInputFile=json_file,
                                                                    preprocessed=True,
                                                                    People_connections_to_check=keys_json,
                                                                    fixed_length=True,
                                                                    k=5).return_results()
    assert CheckConnection(8, people_input_path=people_list_scv, remove_input_path=sentence_remove_scv,
                           sentence_input_path=sentence_lest1_scv, WindowSize=2, Threshold=1,
                           People_connections_to_check=keys_json, fixed_length=True,
                           k=4).return_results() == CheckConnection(8,
                                                                    jsonInputFile=json_file,
                                                                    preprocessed=True,
                                                                    People_connections_to_check=keys_json,
                                                                    fixed_length=True,
                                                                    k=4).return_results()
    assert CheckConnection(8, people_input_path=people_list_scv, remove_input_path=sentence_remove_scv,
                           sentence_input_path=sentence_lest1_scv, WindowSize=2, Threshold=1,
                           People_connections_to_check=keys_json, fixed_length=True,
                           k=3).return_results() == CheckConnection(8,
                                                                    jsonInputFile=json_file,
                                                                    preprocessed=True,
                                                                    People_connections_to_check=keys_json,
                                                                    fixed_length=True,
                                                                    k=3).return_results()
    assert CheckConnection(8, people_input_path=people_list2_scv, remove_input_path=sentence_remove_scv,
                           sentence_input_path=sentence_lest2_scv, WindowSize=2, Threshold=1,
                           People_connections_to_check=keys_json2, fixed_length=True,
                           k=5).return_results() == CheckConnection(8,
                                                                    jsonInputFile=json_file_to_comp,
                                                                    preprocessed=True,
                                                                    People_connections_to_check=keys_json2,
                                                                    fixed_length=True,
                                                                    k=5).return_results()
    assert CheckConnection(8, people_input_path=people_list2_scv, remove_input_path=sentence_remove_scv,
                           sentence_input_path=sentence_lest2_scv, WindowSize=2, Threshold=1,
                           People_connections_to_check=keys_json2, fixed_length=True,
                           k=4).return_results() == CheckConnection(8,
                                                                    jsonInputFile=json_file_to_comp,
                                                                    preprocessed=True,
                                                                    People_connections_to_check=keys_json2,
                                                                    fixed_length=True,
                                                                    k=4).return_results()


def test_result8():
    """
    Test the result8 function
    i tested the following
    Fixed Length Larger Than Graph Depth: If the fixed length is greater than the number of nodes or connections, return False.
    Path Not Found: If no path of the exact specified length exists, return False.
    Looping Paths: Ensure no loops are allowed (i.e., a node should not appear twice in the path).
    Exact Length Matching: Ensure that only paths that exactly match the specified length are returned as True.
    """
    res1 = ('{\n'
            '    "Question 8": {\n'
            '        "Pair Matches": [\n'
            '            [\n'
            '                "Draco Malfoy",\n'
            '                "Ron Weasley",\n'
            '                false\n'
            '            ],\n'
            '            [\n'
            '                "Harry Potter",\n'
            '                "Hermione Granger",\n'
            '                false\n'
            '            ],\n'
            '            [\n'
            '                "Harry Potter",\n'
            '                "Luna Lovegood",\n'
            '                false\n'
            '            ],\n'
            '            [\n'
            '                "Harry Potter",\n'
            '                "Professor Dumbledore",\n'
            '                false\n'
            '            ],\n'
            '            [\n'
            '                "Harry Potter",\n'
            '                "Ron Weasley",\n'
            '                false\n'
            '            ],\n'
            '            [\n'
            '                "Hermione Granger",\n'
            '                "Ron Weasley",\n'
            '                false\n'
            '            ],\n'
            '            [\n'
            '                "Luna Lovegood",\n'
            '                "Neville Longbottom",\n'
            '                false\n'
            '            ],\n'
            '            [\n'
            '                "Luna Lovegood",\n'
            '                "Ron Weasley",\n'
            '                false\n'
            '            ],\n'
            '            [\n'
            '                "Neville Longbottom",\n'
            '                "Ron Weasley",\n'
            '                false\n'
            '            ],\n'
            '            [\n'
            '                "Professor Dumbledore",\n'
            '                "Ron Weasley",\n'
            '                false\n'
            '            ]\n'
            '        ]\n'
            '    }\n'
            '}')
    res2 = ('{\n'
            '    "Question 8": {\n'
            '        "Pair Matches": [\n'
            '            [\n'
            '                "cristiano ronaldo",\n'
            '                "lionel messi",\n'
            '                true\n'
            '            ],\n'
            '            [\n'
            '                "donald trump",\n'
            '                "joe biden",\n'
            '                true\n'
            '            ],\n'
            '            [\n'
            '                "harry cane",\n'
            '                "harry maguire",\n'
            '                true\n'
            '            ],\n'
            '            [\n'
            '                "harry potter",\n'
            '                "ron weasley",\n'
            '                false\n'
            '            ]\n'
            '        ]\n'
            '    }\n'
            '}')
    res3 = ('{\n'
            '    "Question 8": {\n'
            '        "Pair Matches": [\n'
            '            [\n'
            '                "cristiano ronaldo",\n'
            '                "lionel messi",\n'
            '                false\n'
            '            ],\n'
            '            [\n'
            '                "donald trump",\n'
            '                "joe biden",\n'
            '                false\n'
            '            ],\n'
            '            [\n'
            '                "harry cane",\n'
            '                "harry maguire",\n'
            '                false\n'
            '            ],\n'
            '            [\n'
            '                "harry potter",\n'
            '                "ron weasley",\n'
            '                false\n'
            '            ]\n'
            '        ]\n'
            '    }\n'
            '}')
    assert CheckConnection(8, people_input_path=people_list_scv, remove_input_path=sentence_remove_scv,
                           sentence_input_path=sentence_lest1_scv, WindowSize=2, Threshold=1,
                           People_connections_to_check=keys_json, fixed_length=True,
                           k=5).return_results() == res1
    assert CheckConnection(8, people_input_path=people_list_scv, remove_input_path=sentence_remove_scv,
                           sentence_input_path=sentence_lest1_scv, WindowSize=2, Threshold=1,
                           People_connections_to_check=keys_json, fixed_length=True,
                           k=20).return_results() == res1
    assert CheckConnection(8, people_input_path=people_list_scv, remove_input_path=sentence_remove_scv,
                           sentence_input_path=sentence_lest1_scv, WindowSize=2, Threshold=1,
                           People_connections_to_check=keys_json, fixed_length=True,
                           k=4).return_results() == res1
    assert CheckConnection(8, people_input_path=people_list_scv, remove_input_path=sentence_remove_scv,
                           sentence_input_path=sentence_lest1_scv, WindowSize=2, Threshold=1,
                           People_connections_to_check=keys_json, fixed_length=True,
                           k=3).return_results() == res1
    assert CheckConnection(8, people_input_path=people_list2_scv, remove_input_path=sentence_remove_scv,
                           sentence_input_path=sentence_lest2_scv, WindowSize=2, Threshold=1,
                           People_connections_to_check=keys_json2, fixed_length=True,
                           k=5).return_results() == res2
    assert CheckConnection(8, people_input_path=people_list2_scv, remove_input_path=sentence_remove_scv,
                           sentence_input_path=sentence_lest2_scv, WindowSize=2, Threshold=1,
                           People_connections_to_check=keys_json2, fixed_length=True,
                           k=4).return_results() == res2
    assert CheckConnection(8, people_input_path=people_list2_scv, remove_input_path=sentence_remove_scv,
                           sentence_input_path=sentence_lest2_scv, WindowSize=2, Threshold=1,
                           People_connections_to_check=keys_json2, fixed_length=True,
                           k=10).return_results() == res3
