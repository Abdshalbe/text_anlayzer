from PeopleKAssociations import PeopleKAssociations
from test_SearchEngine import *

peopleK1 = PeopleKAssociations(4, json_input_path=json1, preprocessed=True, N=4)
peopleK1_json = PeopleKAssociations(4, sentence_input_path=csv_sentence1, remove_input_path=csv_remved, N=4,
                                    people_input_path=people_names1_file)
peopleK2 = PeopleKAssociations(4, json_input_path=json2, preprocessed=True, N=3)
peopleK2_json = PeopleKAssociations(4, sentence_input_path=csv_sentence1, remove_input_path=csv_remved, N=3,
                                    people_input_path=people_names2_file)
peopleK3 = PeopleKAssociations(4, json_input_path=json3, preprocessed=True, N=2)
peopleK3_json = PeopleKAssociations(4, sentence_input_path=csv_sentence1, remove_input_path=csv_remved, N=2,
                                    people_input_path=people_names3_file)
peopleK4 = PeopleKAssociations(4, json_input_path=json4, preprocessed=True, N=6)
peopleK4_json = PeopleKAssociations(4, sentence_input_path=csv_sentence2, remove_input_path=csv_remved, N=6,
                                    people_input_path=people_names1_file)
peopleK5 = PeopleKAssociations(4, json_input_path=json5, preprocessed=True, N=1)
peopleK5_json = PeopleKAssociations(4, sentence_input_path=csv_sentence2, remove_input_path=csv_remved, N=1,
                                    people_input_path=people_names2_file)
peopleK6 = PeopleKAssociations(4, json_input_path=json6, preprocessed=True, N=2)
peopleK6_json = PeopleKAssociations(4, sentence_input_path=csv_sentence2, remove_input_path=csv_remved, N=2,
                                    people_input_path=people_names3_file)
peopleK7 = PeopleKAssociations(4, json_input_path=json7, preprocessed=True, N=5)
peopleK7_json = PeopleKAssociations(4, sentence_input_path=csv_sentence3, remove_input_path=csv_remved, N=5,
                                    people_input_path=people_names1_file)
peopleK8 = PeopleKAssociations(4, json_input_path=json8, preprocessed=True, N=1)
peopleK8_json = PeopleKAssociations(4, sentence_input_path=csv_sentence3, remove_input_path=csv_remved, N=1,
                                    people_input_path=people_names2_file)
peopleK9 = PeopleKAssociations(4, json_input_path=json9, preprocessed=True, N=4)
peopleK9_json = PeopleKAssociations(4, sentence_input_path=csv_sentence3, remove_input_path=csv_remved, N=4,
                                    people_input_path=people_names3_file)


def check_different_csr_same_res():
    """
    Checks if the different cstr format will not result different values
    """
    assert peopleK1.create_k_seqs() == peopleK1_json.create_k_seqs()
    assert peopleK2.create_k_seqs() == peopleK2_json.create_k_seqs()
    assert peopleK3.create_k_seqs() == peopleK3_json.create_k_seqs()
    assert peopleK4.create_k_seqs() == peopleK4_json.create_k_seqs()
    assert peopleK5.create_k_seqs() == peopleK5_json.create_k_seqs()
    assert peopleK6.create_k_seqs() == peopleK6_json.create_k_seqs()
    assert peopleK7.create_k_seqs() == peopleK7_json.create_k_seqs()
    assert peopleK8.create_k_seqs() == peopleK8_json.create_k_seqs()
    assert peopleK9.create_k_seqs() == peopleK9_json.create_k_seqs()
    assert peopleK1.get_sentences_len() == peopleK1_json.get_sentences_len()
    assert peopleK2.get_sentences_len() == peopleK2_json.get_sentences_len()
    assert peopleK3.get_sentences_len() == peopleK3_json.get_sentences_len()
    assert peopleK4.get_sentences_len() == peopleK4_json.get_sentences_len()
    assert peopleK5.get_sentences_len() == peopleK5_json.get_sentences_len()
    assert peopleK6.get_sentences_len() == peopleK6_json.get_sentences_len()
    assert peopleK7.get_sentences_len() == peopleK7_json.get_sentences_len()
    assert peopleK8.get_sentences_len() == peopleK8_json.get_sentences_len()
    assert peopleK9.get_sentences_len() == peopleK9_json.get_sentences_len()
    assert peopleK1.return_results() == peopleK1_json.return_results()
    assert peopleK2.return_results() == peopleK2_json.return_results()
    assert peopleK3.return_results() == peopleK3_json.return_results()
    assert peopleK4.return_results() == peopleK4_json.return_results()
    assert peopleK5.return_results() == peopleK5_json.return_results()
    assert peopleK6.return_results() == peopleK6_json.return_results()
    assert peopleK7.return_results() == peopleK7_json.return_results()
    assert peopleK8.return_results() == peopleK8_json.return_results()
    assert peopleK9.return_results() == peopleK9_json.return_results()


def test_get_length():
        """
        Test the get_length function
        :return:
        """
        assert peopleK1.get_sentences_len() == 5
        assert peopleK2.get_sentences_len() == 5
        assert peopleK3.get_sentences_len() == 5
        assert peopleK4.get_sentences_len() == 0
        assert peopleK5.get_sentences_len() == 0
        assert peopleK6.get_sentences_len() == 0
        assert peopleK7.get_sentences_len() == 2
        assert peopleK8.get_sentences_len() == 2
        assert peopleK9.get_sentences_len() == 2


def test_get_names_appearances_idx():
    """
    Tests whether get_names_appearances_idx returns the correct index
    """
    assert peopleK1.get_names_appearances_idx() == {'alix dan': [0, 2, 3], 'bagman sr': [3], 'ludo bagman': [3],
                                                    'otto bagman': [3]}
    assert peopleK2.get_names_appearances_idx() == {'malcolm baddock': [1], 'malcolm mcgonagall': [1]}
    assert peopleK3.get_names_appearances_idx() == {}
    assert peopleK4.get_names_appearances_idx() == {}
    assert peopleK5.get_names_appearances_idx() == {}
    assert peopleK6.get_names_appearances_idx() == {}
    assert peopleK7.get_names_appearances_idx() == {}
    assert peopleK8.get_names_appearances_idx() == {'harry potter': [0, 1], 'kathrin': [1]}
    assert peopleK9.get_names_appearances_idx() == {}


def test_return_result():
    """
Test the return value
in this cases we checked theat if people don't finde will not include in the result and
to check if min name is not shown and the other name was fined will be counted
I TESTED : Empty K-seq List: If the list of k-seqs contains no sequences.
K-seq Not Found in Any Sentence: The search should return an empty list if no sentences contain the k-seq.
Case Sensitivity: Handle case variations in search queries and sentences.
Multiple Occurrences of a K-seq in the Same Sentence: Ensure the same sequence is counted only once per sentence.
    """
    res1 = ('{\n'
            '    "Question 4": {\n'
            '        "Person Contexts and K-Seqs": [\n'
            '            [\n'
            '                "alix dan",\n'
            '                [\n'
            '                    [\n'
            '                        "alix"\n'
            '                    ],\n'
            '                    [\n'
            '                        "alix",\n'
            '                        "will"\n'
            '                    ],\n'
            '                    [\n'
            '                        "alix",\n'
            '                        "will",\n'
            '                        "known"\n'
            '                    ],\n'
            '                    [\n'
            '                        "alix",\n'
            '                        "will",\n'
            '                        "known",\n'
            '                        "person"\n'
            '                    ],\n'
            '                    [\n'
            '                        "bagman"\n'
            '                    ],\n'
            '                    [\n'
            '                        "bagman",\n'
            '                        "learned"\n'
            '                    ],\n'
            '                    [\n'
            '                        "bagman",\n'
            '                        "learned",\n'
            '                        "from"\n'
            '                    ],\n'
            '                    [\n'
            '                        "bagman",\n'
            '                        "learned",\n'
            '                        "from",\n'
            '                        "smarter"\n'
            '                    ],\n'
            '                    [\n'
            '                        "from"\n'
            '                    ],\n'
            '                    [\n'
            '                        "from",\n'
            '                        "smarter"\n'
            '                    ],\n'
            '                    [\n'
            '                        "from",\n'
            '                        "smarter",\n'
            '                        "person"\n'
            '                    ],\n'
            '                    [\n'
            '                        "known"\n'
            '                    ],\n'
            '                    [\n'
            '                        "known",\n'
            '                        "mathmtican"\n'
            '                    ],\n'
            '                    [\n'
            '                        "known",\n'
            '                        "mathmtican",\n'
            '                        "professor"\n'
            '                    ],\n'
            '                    [\n'
            '                        "known",\n'
            '                        "person"\n'
            '                    ],\n'
            '                    [\n'
            '                        "learned"\n'
            '                    ],\n'
            '                    [\n'
            '                        "learned",\n'
            '                        "from"\n'
            '                    ],\n'
            '                    [\n'
            '                        "learned",\n'
            '                        "from",\n'
            '                        "smarter"\n'
            '                    ],\n'
            '                    [\n'
            '                        "learned",\n'
            '                        "from",\n'
            '                        "smarter",\n'
            '                        "person"\n'
            '                    ],\n'
            '                    [\n'
            '                        "mallcom"\n'
            '                    ],\n'
            '                    [\n'
            '                        "mallcom",\n'
            '                        "will"\n'
            '                    ],\n'
            '                    [\n'
            '                        "mallcom",\n'
            '                        "will",\n'
            '                        "known"\n'
            '                    ],\n'
            '                    [\n'
            '                        "mallcom",\n'
            '                        "will",\n'
            '                        "known",\n'
            '                        "mathmtican"\n'
            '                    ],\n'
            '                    [\n'
            '                        "mathmtican"\n'
            '                    ],\n'
            '                    [\n'
            '                        "mathmtican",\n'
            '                        "professor"\n'
            '                    ],\n'
            '                    [\n'
            '                        "person"\n'
            '                    ],\n'
            '                    [\n'
            '                        "professor"\n'
            '                    ],\n'
            '                    [\n'
            '                        "smarter"\n'
            '                    ],\n'
            '                    [\n'
            '                        "smarter",\n'
            '                        "person"\n'
            '                    ],\n'
            '                    [\n'
            '                        "will"\n'
            '                    ],\n'
            '                    [\n'
            '                        "will",\n'
            '                        "known"\n'
            '                    ],\n'
            '                    [\n'
            '                        "will",\n'
            '                        "known",\n'
            '                        "mathmtican"\n'
            '                    ],\n'
            '                    [\n'
            '                        "will",\n'
            '                        "known",\n'
            '                        "mathmtican",\n'
            '                        "professor"\n'
            '                    ],\n'
            '                    [\n'
            '                        "will",\n'
            '                        "known",\n'
            '                        "person"\n'
            '                    ]\n'
            '                ]\n'
            '            ],\n'
            '            [\n'
            '                "bagman sr",\n'
            '                [\n'
            '                    [\n'
            '                        "bagman"\n'
            '                    ],\n'
            '                    [\n'
            '                        "bagman",\n'
            '                        "learned"\n'
            '                    ],\n'
            '                    [\n'
            '                        "bagman",\n'
            '                        "learned",\n'
            '                        "from"\n'
            '                    ],\n'
            '                    [\n'
            '                        "bagman",\n'
            '                        "learned",\n'
            '                        "from",\n'
            '                        "smarter"\n'
            '                    ],\n'
            '                    [\n'
            '                        "from"\n'
            '                    ],\n'
            '                    [\n'
            '                        "from",\n'
            '                        "smarter"\n'
            '                    ],\n'
            '                    [\n'
            '                        "from",\n'
            '                        "smarter",\n'
            '                        "person"\n'
            '                    ],\n'
            '                    [\n'
            '                        "learned"\n'
            '                    ],\n'
            '                    [\n'
            '                        "learned",\n'
            '                        "from"\n'
            '                    ],\n'
            '                    [\n'
            '                        "learned",\n'
            '                        "from",\n'
            '                        "smarter"\n'
            '                    ],\n'
            '                    [\n'
            '                        "learned",\n'
            '                        "from",\n'
            '                        "smarter",\n'
            '                        "person"\n'
            '                    ],\n'
            '                    [\n'
            '                        "person"\n'
            '                    ],\n'
            '                    [\n'
            '                        "smarter"\n'
            '                    ],\n'
            '                    [\n'
            '                        "smarter",\n'
            '                        "person"\n'
            '                    ]\n'
            '                ]\n'
            '            ],\n'
            '            [\n'
            '                "ludo bagman",\n'
            '                [\n'
            '                    [\n'
            '                        "bagman"\n'
            '                    ],\n'
            '                    [\n'
            '                        "bagman",\n'
            '                        "learned"\n'
            '                    ],\n'
            '                    [\n'
            '                        "bagman",\n'
            '                        "learned",\n'
            '                        "from"\n'
            '                    ],\n'
            '                    [\n'
            '                        "bagman",\n'
            '                        "learned",\n'
            '                        "from",\n'
            '                        "smarter"\n'
            '                    ],\n'
            '                    [\n'
            '                        "from"\n'
            '                    ],\n'
            '                    [\n'
            '                        "from",\n'
            '                        "smarter"\n'
            '                    ],\n'
            '                    [\n'
            '                        "from",\n'
            '                        "smarter",\n'
            '                        "person"\n'
            '                    ],\n'
            '                    [\n'
            '                        "learned"\n'
            '                    ],\n'
            '                    [\n'
            '                        "learned",\n'
            '                        "from"\n'
            '                    ],\n'
            '                    [\n'
            '                        "learned",\n'
            '                        "from",\n'
            '                        "smarter"\n'
            '                    ],\n'
            '                    [\n'
            '                        "learned",\n'
            '                        "from",\n'
            '                        "smarter",\n'
            '                        "person"\n'
            '                    ],\n'
            '                    [\n'
            '                        "person"\n'
            '                    ],\n'
            '                    [\n'
            '                        "smarter"\n'
            '                    ],\n'
            '                    [\n'
            '                        "smarter",\n'
            '                        "person"\n'
            '                    ]\n'
            '                ]\n'
            '            ],\n'
            '            [\n'
            '                "otto bagman",\n'
            '                [\n'
            '                    [\n'
            '                        "bagman"\n'
            '                    ],\n'
            '                    [\n'
            '                        "bagman",\n'
            '                        "learned"\n'
            '                    ],\n'
            '                    [\n'
            '                        "bagman",\n'
            '                        "learned",\n'
            '                        "from"\n'
            '                    ],\n'
            '                    [\n'
            '                        "bagman",\n'
            '                        "learned",\n'
            '                        "from",\n'
            '                        "smarter"\n'
            '                    ],\n'
            '                    [\n'
            '                        "from"\n'
            '                    ],\n'
            '                    [\n'
            '                        "from",\n'
            '                        "smarter"\n'
            '                    ],\n'
            '                    [\n'
            '                        "from",\n'
            '                        "smarter",\n'
            '                        "person"\n'
            '                    ],\n'
            '                    [\n'
            '                        "learned"\n'
            '                    ],\n'
            '                    [\n'
            '                        "learned",\n'
            '                        "from"\n'
            '                    ],\n'
            '                    [\n'
            '                        "learned",\n'
            '                        "from",\n'
            '                        "smarter"\n'
            '                    ],\n'
            '                    [\n'
            '                        "learned",\n'
            '                        "from",\n'
            '                        "smarter",\n'
            '                        "person"\n'
            '                    ],\n'
            '                    [\n'
            '                        "person"\n'
            '                    ],\n'
            '                    [\n'
            '                        "smarter"\n'
            '                    ],\n'
            '                    [\n'
            '                        "smarter",\n'
            '                        "person"\n'
            '                    ]\n'
            '                ]\n'
            '            ]\n'
            '        ]\n'
            '    }\n'
            '}')
    res2 = ('{\n'
            '    "Question 4": {\n'
            '        "Person Contexts and K-Seqs": [\n'
            '            [\n'
            '                "malcolm baddock",\n'
            '                [\n'
            '                    [\n'
            '                        "from"\n'
            '                    ],\n'
            '                    [\n'
            '                        "from",\n'
            '                        "malcolm"\n'
            '                    ],\n'
            '                    [\n'
            '                        "he"\n'
            '                    ],\n'
            '                    [\n'
            '                        "he",\n'
            '                        "learn"\n'
            '                    ],\n'
            '                    [\n'
            '                        "he",\n'
            '                        "learn",\n'
            '                        "from"\n'
            '                    ],\n'
            '                    [\n'
            '                        "learn"\n'
            '                    ],\n'
            '                    [\n'
            '                        "learn",\n'
            '                        "from"\n'
            '                    ],\n'
            '                    [\n'
            '                        "learn",\n'
            '                        "from",\n'
            '                        "malcolm"\n'
            '                    ],\n'
            '                    [\n'
            '                        "malcolm"\n'
            '                    ]\n'
            '                ]\n'
            '            ],\n'
            '            [\n'
            '                "malcolm mcgonagall",\n'
            '                [\n'
            '                    [\n'
            '                        "from"\n'
            '                    ],\n'
            '                    [\n'
            '                        "from",\n'
            '                        "malcolm"\n'
            '                    ],\n'
            '                    [\n'
            '                        "he"\n'
            '                    ],\n'
            '                    [\n'
            '                        "he",\n'
            '                        "learn"\n'
            '                    ],\n'
            '                    [\n'
            '                        "he",\n'
            '                        "learn",\n'
            '                        "from"\n'
            '                    ],\n'
            '                    [\n'
            '                        "learn"\n'
            '                    ],\n'
            '                    [\n'
            '                        "learn",\n'
            '                        "from"\n'
            '                    ],\n'
            '                    [\n'
            '                        "learn",\n'
            '                        "from",\n'
            '                        "malcolm"\n'
            '                    ],\n'
            '                    [\n'
            '                        "malcolm"\n'
            '                    ]\n'
            '                ]\n'
            '            ]\n'
            '        ]\n'
            '    }\n'
            '}')
    res3 = ('{\n'
            '    "Question 4": {\n'
            '        "Person Contexts and K-Seqs": []\n'
            '    }\n'
            '}')
    res4 = ('{\n'
            '    "Question 4": {\n'
            '        "Person Contexts and K-Seqs": [\n'
            '            [\n'
            '                "harry potter",\n'
            '                [\n'
            '                    [\n'
            '                        "best"\n'
            '                    ],\n'
            '                    [\n'
            '                        "cathy"\n'
            '                    ],\n'
            '                    [\n'
            '                        "friend"\n'
            '                    ],\n'
            '                    [\n'
            '                        "harry"\n'
            '                    ],\n'
            '                    [\n'
            '                        "mallcom"\n'
            '                    ],\n'
            '                    [\n'
            '                        "was"\n'
            '                    ]\n'
            '                ]\n'
            '            ],\n'
            '            [\n'
            '                "kathrin",\n'
            '                [\n'
            '                    [\n'
            '                        "best"\n'
            '                    ],\n'
            '                    [\n'
            '                        "cathy"\n'
            '                    ],\n'
            '                    [\n'
            '                        "friend"\n'
            '                    ],\n'
            '                    [\n'
            '                        "harry"\n'
            '                    ],\n'
            '                    [\n'
            '                        "was"\n'
            '                    ]\n'
            '                ]\n'
            '            ]\n'
            '        ]\n'
            '    }\n'
            '}')
    assert peopleK1.return_results() == res1
    assert peopleK2.return_results() == res2
    assert peopleK3.return_results() == res3
    assert peopleK4.return_results() == res3
    assert peopleK5.return_results() == res3
    assert peopleK6.return_results() == res3
    assert peopleK7.return_results() == res3
    assert peopleK8.return_results() == res4
    assert peopleK9.return_results() == res3
