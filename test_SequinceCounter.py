from SequinceCounter import generate_k_seqs, SequinceCounter
from test_Parser import *


def create_temp_json(data):
    # Create a temporary file using tempfile.NamedTemporaryFile
    with tempfile.NamedTemporaryFile(delete=False, mode='w', newline='', suffix='.json') as tmp_file:
        # Prepare the data as a dictionary with the 'start' as the key
        json_data = {data}

        # Write the JSON data to the temporary file
        json.dump(json_data, tmp_file, indent=4)

        # Return the path of the temporary file
        return tmp_file.nam


def test_generate_k_seqs():
    text = [["hello", "world"], ["hello", "world"]]
    assert generate_k_seqs(text, 2) == {'1_seq': [(('hello',), 2), (('world',), 2)], '2_seq': [(('hello', 'world'), 2)]}
    assert generate_k_seqs(text, 3) == {'1_seq': [(('hello',), 2), (('world',), 2)], '2_seq': [(('hello', 'world'), 2)],
                                        '3_seq': []}
    assert generate_k_seqs(text, 4) == {'1_seq': [(('hello',), 2), (('world',), 2)]}


json1 = create_temp_json(data_str)
json2 = create_temp_json(data_str2)
json3 = create_temp_json(data_str3)
json4 = create_temp_json(data_str4)
json5 = create_temp_json(data_str5)
json6 = create_temp_json(data_str6)


def test_SEQUENCE_CST():
    """
    Tests that the SEQUENCE_COUNTER with  two different construct value will return the same value if they are equal
    :return:
    """
    assert SequinceCounter(1, sentence_input_path=csv_sentence1, remove_input_path=csv_remved2,
                           N=4).count_sequences() == SequinceCounter(1, json_input_path=json1,
                                                                     preprocessed=True).count_sequences()
    # assert SequinceCounter(1,sentence_input_path=csv_sentence6,remove_input_path=csv_remved1,N = 4).count_sequences() == SequinceCounter(1,json_input_path=json2,preprocessed=True).count_sequences()
    # assert SequinceCounter(1,sentence_input_path=csv_sentence2,remove_input_path=csv_remved1,N = 4).count_sequences() == SequinceCounter(1,json_input_path=json3,preprocessed=True).count_sequences()
    # assert SequinceCounter(1,sentence_input_path=csv_sentence3,remove_input_path=csv_remved1,N = 4).count_sequences() == SequinceCounter(1,json_input_path=json4,preprocessed=True).count_sequences()
    # assert SequinceCounter(1,sentence_input_path=csv_sentence4,remove_input_path=csv_remved1,N = 4).count_sequences() == SequinceCounter(1,json_input_path=json5,preprocessed=True).count_sequences()
    # assert SequinceCounter(1,sentence_input_path=csv_sentence5,remove_input_path=csv_remved1,N = 4).count_sequences() == SequinceCounter(1,json_input_path=json6,preprocessed=True).count_sequences()


def test_load_Sentences_names():
    pass


def test_count_sentences():
    pass


def test_compare_json():
    pass
