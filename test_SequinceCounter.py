import pytest
from SequinceCounter import SequinceCounter

SEQUENCE_COUNTER1 = SequinceCounter(2,
                                   sentence_input_path=r"C:\Users\abdsh\OneDrive\Desktop\huji cs\intro\finalProject\text_analyzer\2_examples\Q2_examples\example_1\sentences_small_1.csv",
                                   remove_input_path=r"C:\Users\abdsh\OneDrive\Desktop\huji cs\intro\finalProject\text_analyzer\1_data\data\REMOVEWORDS.csv",
                                   N=3)
SEQUENCE_COUNTER2= SequinceCounter(2,
                                   sentence_input_path=r"C:\Users\abdsh\OneDrive\Desktop\huji cs\intro\finalProject\text_analyzer\2_examples\Q2_examples\example_2\sentences_small_2.csv",
                                   remove_input_path=r"C:\Users\abdsh\OneDrive\Desktop\huji cs\intro\finalProject\text_analyzer\1_data\data\REMOVEWORDS.csv",
                                   N=3)
SEQUENCE_COUNTER3 = SequinceCounter(2,
                                   sentence_input_path=r"C:\Users\abdsh\OneDrive\Desktop\huji cs\intro\finalProject\text_analyzer\2_examples\Q2_examples\example_3\sentences_small_3.csv",
                                   remove_input_path=r"C:\Users\abdsh\OneDrive\Desktop\huji cs\intro\finalProject\text_analyzer\1_data\data\REMOVEWORDS.csv",
                                   N=3)
SEQUENCE_COUNTER4 = SequinceCounter(2, json_input_path="text_analyzer/Q1_result1.json", N=3)
SEQUENCE_COUNTER5 = SequinceCounter(2, json_input_path="text_analyzer/Q1_result2.json",N=4)
SEQUENCE_COUNTER6 = SequinceCounter(2, json_input_path="text_analyzer/Q1_result3.json",N=5)
# print(SEQUENCE_COUNTER1.count_sequences())
def test_SEQUENCE_COUNTER():
    """
    Tests that the SEQUENCE_COUNTER with  two different construct value will return the same value if they are equal
    :return:
    """
    # assert SEQUENCE_COUNTER4.count_sequences() == SEQUENCE_COUNTER1.count_sequences()
    # assert SEQUENCE_COUNTER5.count_sequences() == SEQUENCE_COUNTER2.count_sequences()
    assert SEQUENCE_COUNTER6.count_sequences() == SEQUENCE_COUNTER3.count_sequences()