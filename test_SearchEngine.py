from contextlib import redirect_stderr

from SearchEngine import SearchEngine
from test_NamesCounter import *

keys1 = {'keys': [["known", "person"], ["learn", "malcolm"], ["friend"], ["was", "best", "friend"]]}
keys2 = {'keys': [["harry"], ["learn", "smarter"], ["MAX"]]}
keys3 = {'keys': [['DAD'], ['sandy']]}  # no appearance

# Convert the dictionaries to JSON strings
keys_file1 = process_json_data(json.dumps(keys1))  # Convert to JSON string first
keys_file2 = process_json_data(json.dumps(keys2))  # Convert to JSON string first
keys_file3 = process_json_data(json.dumps(keys3))  # Convert to JSON string first


def test_equal_csr():
    """"
    assert that the supplied json file contains the same as csv are same in construction
    """
    assert SearchEngine(4, jsonInputFile=json1, kSeqJson=keys_file1,
                        preprocessed=True).return_results() == SearchEngine(4, sentence_input_path=csv_sentence1,
                                                                            remove_input_path=csv_remved,
                                                                            kSeqJson=keys_file1).return_results()
    assert SearchEngine(4, jsonInputFile=json4, kSeqJson=keys_file1,
                        preprocessed=True).return_results() == SearchEngine(4, sentence_input_path=csv_sentence2,
                                                                            remove_input_path=csv_remved,
                                                                            kSeqJson=keys_file1).return_results()
    assert SearchEngine(4, jsonInputFile=json7, kSeqJson=keys_file1,
                        preprocessed=True).return_results() == SearchEngine(4, sentence_input_path=csv_sentence3,
                                                                            remove_input_path=csv_remved,
                                                                            kSeqJson=keys_file1).return_results()
    assert SearchEngine(4, jsonInputFile=json1, kSeqJson=keys_file2,
                        preprocessed=True).return_results() == SearchEngine(4, sentence_input_path=csv_sentence1,
                                                                            remove_input_path=csv_remved,
                                                                            kSeqJson=keys_file2).return_results()
    assert SearchEngine(4, jsonInputFile=json4, kSeqJson=keys_file2,
                        preprocessed=True).return_results() == SearchEngine(4, sentence_input_path=csv_sentence2,
                                                                            remove_input_path=csv_remved,
                                                                            kSeqJson=keys_file2).return_results()
    assert SearchEngine(4, jsonInputFile=json7, kSeqJson=keys_file2,
                        preprocessed=True).return_results() == SearchEngine(4, sentence_input_path=csv_sentence3,
                                                                            remove_input_path=csv_remved,
                                                                            kSeqJson=keys_file2).return_results()
    assert SearchEngine(4, jsonInputFile=json1, kSeqJson=keys_file3,
                        preprocessed=True).return_results() == SearchEngine(4, sentence_input_path=csv_sentence1,
                                                                            remove_input_path=csv_remved,
                                                                            kSeqJson=keys_file3).return_results()
    assert SearchEngine(4, jsonInputFile=json4, kSeqJson=keys_file3,
                        preprocessed=True).return_results() == SearchEngine(4, sentence_input_path=csv_sentence2,
                                                                            remove_input_path=csv_remved,
                                                                            kSeqJson=keys_file3).return_results()
    assert SearchEngine(4, jsonInputFile=json7, kSeqJson=keys_file3,
                        preprocessed=True).return_results() == SearchEngine(4, sentence_input_path=csv_sentence3,
                                                                            remove_input_path=csv_remved,
                                                                            kSeqJson=keys_file3).return_results()
    assert SearchEngine(4, jsonInputFile=json1, kSeqJson=keys_file1,
                        preprocessed=True).result_KseqData() == SearchEngine(4, sentence_input_path=csv_sentence1,
                                                                             remove_input_path=csv_remved,
                                                                             kSeqJson=keys_file1).result_KseqData()
    assert SearchEngine(4, jsonInputFile=json4, kSeqJson=keys_file1,
                        preprocessed=True).result_KseqData() == SearchEngine(4, sentence_input_path=csv_sentence2,
                                                                             remove_input_path=csv_remved,
                                                                             kSeqJson=keys_file1).result_KseqData()
    assert SearchEngine(4, jsonInputFile=json7, kSeqJson=keys_file1,
                        preprocessed=True).result_KseqData() == SearchEngine(4, sentence_input_path=csv_sentence3,
                                                                             remove_input_path=csv_remved,
                                                                             kSeqJson=keys_file1).result_KseqData()
    assert SearchEngine(4, jsonInputFile=json1, kSeqJson=keys_file2,
                        preprocessed=True).result_KseqData() == SearchEngine(4, sentence_input_path=csv_sentence1,
                                                                             remove_input_path=csv_remved,
                                                                             kSeqJson=keys_file2).result_KseqData()
    assert SearchEngine(4, jsonInputFile=json4, kSeqJson=keys_file2,
                        preprocessed=True).result_KseqData() == SearchEngine(4, sentence_input_path=csv_sentence2,
                                                                             remove_input_path=csv_remved,
                                                                             kSeqJson=keys_file2).result_KseqData()
    assert SearchEngine(4, jsonInputFile=json7, kSeqJson=keys_file2,
                        preprocessed=True).result_KseqData() == SearchEngine(4, sentence_input_path=csv_sentence3,
                                                                             remove_input_path=csv_remved,
                                                                             kSeqJson=keys_file2).result_KseqData()
    assert SearchEngine(4, jsonInputFile=json1, kSeqJson=keys_file3,
                        preprocessed=True).result_KseqData() == SearchEngine(4, sentence_input_path=csv_sentence1,
                                                                             remove_input_path=csv_remved,
                                                                             kSeqJson=keys_file3).result_KseqData()
    assert SearchEngine(4, jsonInputFile=json4, kSeqJson=keys_file3,
                        preprocessed=True).result_KseqData() == SearchEngine(4, sentence_input_path=csv_sentence2,
                                                                             remove_input_path=csv_remved,
                                                                             kSeqJson=keys_file3).result_KseqData()
    assert SearchEngine(4, jsonInputFile=json7, kSeqJson=keys_file3,
                        preprocessed=True).result_KseqData() == SearchEngine(4, sentence_input_path=csv_sentence3,
                                                                             remove_input_path=csv_remved,
                                                                             kSeqJson=keys_file3).result_KseqData()


def test_result_KseqData():
    """
    Test the result of the Kseq Search Engine as needed
    """
    assert SearchEngine(4, jsonInputFile=json1, kSeqJson=keys_file1,
                        preprocessed=True).result_KseqData() == {('friend',): [], ('known', 'person'): [
        ['alix', 'will', 'known', 'person']], ('learn', 'malcolm'): [], ('was', 'best', 'friend'): []}
    assert SearchEngine(4, sentence_input_path=csv_sentence2, remove_input_path=csv_remved,
                        kSeqJson=keys_file1).result_KseqData() == {('friend',): [], ('known', 'person'): [],
                                                                   ('learn', 'malcolm'): [],
                                                                   ('was', 'best', 'friend'): []}
    assert SearchEngine(4, jsonInputFile=json7, kSeqJson=keys_file1,
                        preprocessed=True).result_KseqData() == SearchEngine(4, sentence_input_path=csv_sentence3,
                                                                             remove_input_path=csv_remved,
                                                                             kSeqJson=keys_file1).result_KseqData() == {
               ('friend',): [['harry', 'was', 'best', 'friend', 'cathy'],
                             ['mallcom', 'was', 'best', 'friend', 'harry']],
               ('known', 'person'): [],
               ('learn', 'malcolm'): [],
               ('was', 'best', 'friend'): [['harry', 'was', 'best', 'friend', 'cathy'],
                                           ['mallcom', 'was', 'best', 'friend', 'harry']]}
    assert SearchEngine(4, jsonInputFile=json1, kSeqJson=keys_file2,
                        preprocessed=True).result_KseqData() == SearchEngine(4, sentence_input_path=csv_sentence1,
                                                                             remove_input_path=csv_remved,
                                                                             kSeqJson=keys_file2).result_KseqData() == {
               ('harry',): [], ('learn', 'smarter'): [], ('max',): []}
    assert SearchEngine(4, jsonInputFile=json4, kSeqJson=keys_file2,
                        preprocessed=True).result_KseqData() == SearchEngine(4, sentence_input_path=csv_sentence2,
                                                                             remove_input_path=csv_remved,
                                                                             kSeqJson=keys_file2).result_KseqData() == {
               ('harry',): [], ('learn', 'smarter'): [], ('max',): []}
    assert SearchEngine(4, jsonInputFile=json7, kSeqJson=keys_file2,
                        preprocessed=True).result_KseqData() == SearchEngine(4, sentence_input_path=csv_sentence3,
                                                                             remove_input_path=csv_remved,
                                                                             kSeqJson=keys_file2).result_KseqData() == {
               ('harry',): [['harry', 'was', 'best', 'friend', 'cathy'], ['mallcom', 'was', 'best', 'friend', 'harry']],
               ('learn', 'smarter'): [], ('max',): []}
    assert SearchEngine(4, jsonInputFile=json1, kSeqJson=keys_file3,
                        preprocessed=True).result_KseqData() == SearchEngine(4, sentence_input_path=csv_sentence1,
                                                                             remove_input_path=csv_remved,
                                                                             kSeqJson=keys_file3).result_KseqData() == {
               ('dad',): [], ('sandy',): []}
    assert SearchEngine(4, jsonInputFile=json4, kSeqJson=keys_file3,
                        preprocessed=True).result_KseqData() == SearchEngine(4, sentence_input_path=csv_sentence2,
                                                                             remove_input_path=csv_remved,
                                                                             kSeqJson=keys_file3).result_KseqData() == {
               ('dad',): [], ('sandy',): []}
    assert SearchEngine(4, jsonInputFile=json7, kSeqJson=keys_file3,
                        preprocessed=True).result_KseqData() == SearchEngine(4, sentence_input_path=csv_sentence3,
                                                                             remove_input_path=csv_remved,
                                                                             kSeqJson=keys_file3).result_KseqData() == {
               ('dad',): [], ('sandy',): []}


def test_result():
    """
    Test the result of the search engine is as needed
    I TESTED :
    Empty K-seq List: If the list of k-seqs contains no sequences.
    K-seq Not Found in Any Sentence: The search should return an empty list if no sentences contain the k-seq.
    Case Sensitivity: Handle case variations in search queries and sentences.
    Multiple Occurrences of a K-seq in the Same Sentence: Ensure the same sequence is counted only once per sentence.
    """
    res1 = ('{\n'
            '    "Question 4": {\n'
            '        "K-Seq Matches": [\n'
            '            [\n'
            '                "known person",\n'
            '                [\n'
            '                    [\n'
            '                        "alix",\n'
            '                        "will",\n'
            '                        "known",\n'
            '                        "person"\n'
            '                    ]\n'
            '                ]\n'
            '            ]\n'
            '        ]\n'
            '    }\n'
            '}')
    res2 = '{\n    "Question 4": {\n        "K-Seq Matches": []\n    }\n}'
    res3 = ('{\n'
            '    "Question 4": {\n'
            '        "K-Seq Matches": [\n'
            '            [\n'
            '                "friend",\n'
            '                [\n'
            '                    [\n'
            '                        "harry",\n'
            '                        "was",\n'
            '                        "best",\n'
            '                        "friend",\n'
            '                        "cathy"\n'
            '                    ],\n'
            '                    [\n'
            '                        "mallcom",\n'
            '                        "was",\n'
            '                        "best",\n'
            '                        "friend",\n'
            '                        "harry"\n'
            '                    ]\n'
            '                ]\n'
            '            ],\n'
            '            [\n'
            '                "was best friend",\n'
            '                [\n'
            '                    [\n'
            '                        "harry",\n'
            '                        "was",\n'
            '                        "best",\n'
            '                        "friend",\n'
            '                        "cathy"\n'
            '                    ],\n'
            '                    [\n'
            '                        "mallcom",\n'
            '                        "was",\n'
            '                        "best",\n'
            '                        "friend",\n'
            '                        "harry"\n'
            '                    ]\n'
            '                ]\n'
            '            ]\n'
            '        ]\n'
            '    }\n'
            '}')
    res4 = ('{\n'
            '    "Question 4": {\n'
            '        "K-Seq Matches": [\n'
            '            [\n'
            '                "harry",\n'
            '                [\n'
            '                    [\n'
            '                        "harry",\n'
            '                        "was",\n'
            '                        "best",\n'
            '                        "friend",\n'
            '                        "cathy"\n'
            '                    ],\n'
            '                    [\n'
            '                        "mallcom",\n'
            '                        "was",\n'
            '                        "best",\n'
            '                        "friend",\n'
            '                        "harry"\n'
            '                    ]\n'
            '                ]\n'
            '            ]\n'
            '        ]\n'
            '    }\n'
            '}')

    assert SearchEngine(4, jsonInputFile=json1, kSeqJson=keys_file1, preprocessed=True).return_results() == res1
    assert SearchEngine(4, sentence_input_path=csv_sentence2, remove_input_path=csv_remved,
                        kSeqJson=keys_file1).return_results() == res2
    assert SearchEngine(4, jsonInputFile=json7, kSeqJson=keys_file1, preprocessed=True).return_results() == res3
    assert SearchEngine(4, sentence_input_path=csv_sentence1, remove_input_path=csv_remved,
                        kSeqJson=keys_file2).return_results() == res2
    assert SearchEngine(4, jsonInputFile=json4, kSeqJson=keys_file2, preprocessed=True).return_results() == res2
    assert SearchEngine(4, jsonInputFile=json7, kSeqJson=keys_file2, preprocessed=True).return_results() == res4
    assert SearchEngine(4, sentence_input_path=csv_sentence1, remove_input_path=csv_remved,
                        kSeqJson=keys_file3).return_results() == res2
    assert SearchEngine(4, jsonInputFile=json4, kSeqJson=keys_file3, preprocessed=True).return_results() == res2
    assert SearchEngine(4, sentence_input_path=csv_sentence3, remove_input_path=csv_remved,
                        kSeqJson=keys_file3).return_results() == res2
