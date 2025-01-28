import json

import pytest
from NamesCounter import NamesCounter

NAMES_COUNTER1 = NamesCounter(3, json_input_path="text_analyzer/2_examples/Q1_examples/example_1/Q1_result1.json",preprocessed=True)
NAMES_COUNTER2 = NamesCounter(3, json_input_path="text_analyzer/2_examples/Q1_examples/example_2/Q1_result2.json",preprocessed= True)
NAMES_COUNTER3 = NamesCounter(3, json_input_path="text_analyzer/2_examples/Q1_examples/example_3/Q1_result3.json",preprocessed= True)
NAMES_COUNTER4 = NamesCounter(3,
                              people_input_path="text_analyzer/2_examples/Q3_examples/example_1/people_small_1.csv",
                              remove_input_path="text_analyzer/1_data/data/REMOVEWORDS.csv",
                              sentence_input_path="text_analyzer/2_examples/Q3_examples/example_1/sentences_small_1.csv")
NAMES_COUNTER5 = NamesCounter(3,
                              people_input_path="text_analyzer/2_examples/Q3_examples/example_2/people_small_2.csv",
                              remove_input_path="text_analyzer/1_data/data/REMOVEWORDS.csv",
                              sentence_input_path="text_analyzer/2_examples/Q3_examples/example_2/sentences_small_2.csv")
NAMES_COUNTER6 = NamesCounter(3,
                              people_input_path="text_analyzer/2_examples/Q3_examples/example_3/people_small_3.csv",
                              remove_input_path="text_analyzer/1_data/data/REMOVEWORDS.csv",
                              sentence_input_path="text_analyzer/2_examples/Q3_examples/example_3/sentences_small_3.csv")

def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


# Function to compare two JSON files and return True if they are identical, False otherwise
def compare_json(file1, file2):
    """
    Compares two json files after load them
    :param file1: first json file
    :param file2: second json file
    :return: true if they are equal, false otherwise
    """
    try:
        # Load both JSON files into dictionaries
        data1 = load_json(file1)
        data2 = load_json(file2)
        # Compare the two dictionaries and return True if they are identical
        return data1 == data2
    except Exception as e:
        print(f"Error comparing JSON files: {e}")
        return False

def test_equal_csr():
    """
    Test the equality of two CSRs of the text and names and removal
    :return: failed or not (True/False)
    """
    assert NAMES_COUNTER1.get_names() == NAMES_COUNTER4.get_names() and NAMES_COUNTER1.get_sentences() == NAMES_COUNTER4.get_sentences()
    assert NAMES_COUNTER2.get_names() == NAMES_COUNTER5.get_names() and NAMES_COUNTER2.get_sentences() == NAMES_COUNTER5.get_sentences()
    assert NAMES_COUNTER3.get_names() == NAMES_COUNTER6.get_names() and NAMES_COUNTER3.get_sentences() == NAMES_COUNTER6.get_sentences()


def test_not_equal_csr():
    assert NAMES_COUNTER1.get_names() != NAMES_COUNTER5.get_names() and NAMES_COUNTER1.get_sentences() != NAMES_COUNTER5 .get_sentences()
    assert NAMES_COUNTER2.get_names() != NAMES_COUNTER6.get_names() and NAMES_COUNTER2.get_sentences() != NAMES_COUNTER6.get_sentences()
    assert NAMES_COUNTER3.get_names() != NAMES_COUNTER4.get_names() and NAMES_COUNTER3.get_sentences() != NAMES_COUNTER4.get_sentences()


def test_get_names():
    Res1 = [[['attentive', 'wizard'], []], [['bertram', 'aubrey'], []], [['audrey', 'weasley'], []],
            [['augusta', 'gran', 'longbottom'], []], [['augustus', 'pye'], []], [['augustus', 'rookwood'], []],
            [['augustus', 'worme'], []], [['auntie', 'muriel'], []], [['aunt', 'marge', 'dursley'], []],
            [['aurelius', 'dumbledore'], []], [['aurora', 'sinistra'], []], [['avery'], []],
            [['babajide', 'akingbade'], []], [['babayaga'], []], [['babbitty', 'rabbitty'], []], [['bagman', 'sr'], []],
            [['ludo', 'bagman'], []], [['otto', 'bagman'], []], [['millicent', 'bagnold'], []],
            [['bathilda', 'bagshot'], [['batty']]], [['kquewanda', 'bailey'], []],
            [['ballyfumble', 'stranger'], [['quin'], ['quivering', 'quintus'], ['quintusofthesillyname']]]]
    Res2 = [[['ignatia', 'wildsmith'], []], [['ignatius', 'prewett'], []], [['ignatius', 'tuft'], []],
            [['ignotus', 'peverell'], []], [['igor', 'karkaroff'], []], [['illyius'], []], [['ingolfr', 'iambic'], []]]
    Res3 = [[['magnus', 'dent', 'macdonald'], []], [['magorian'], []], [['maisie', 'cattermole'], []],
            [['malcolm'], []], [['malcolm', 'baddock'], []], [['malcolm', 'mcgonagall'], []],
            [['harold', 'skively'], []], [['harper'], []], [['harry', 'potter'],
                                                            [['lived'], ['undesirable', 'number'], ['chosen'],
                                                             ['parry', 'otter'], ['chosen'], ['mudbloods', 'friend']]],
            [['harvey', 'ridgebit'], []], [['hassan', 'mostafa'], []]]
    assert NAMES_COUNTER1.get_names() == Res1
    assert NAMES_COUNTER2.get_names() == Res2
    assert NAMES_COUNTER3.get_names() == Res3
    assert NAMES_COUNTER4.get_names() == Res1
    assert NAMES_COUNTER5.get_names() == Res2
    assert NAMES_COUNTER6.get_names() == Res3


def test_get_sentence():
    Res1 = [
        ['tuft', 'jet', 'black', 'forehead', 'dumbledore', 'mcgonagall', 'curiously', 'shaped', 'cut', 'like', 'bolt',
         'lightning'], ['whispered', 'professor', 'mcgonagall'],
        ['dumbledore', 'dumbledore', 'll', 'scar', 'forever', 'couldn', 'something', 'scar', 'dumbledore', 'wouldn'],
        ['scars', 'handy'], ['left', 'knee', 'perfect', 'map', 'london', 'underground'],
        ['well', 'dumbledore', 'hagrid', 'better', 'dumbledore', 'took', 'harry', 'harry', 'arms', 'turned', 'toward',
         'dursley', 'dursley', 'dudley', 'dursley', 'house'], ['good', 'bye', 'harry', 'sir', 'asked', 'hagrid'],
        ['harry', 'bent', 'harry', 'great', 'shaggy', 'harry', 'gave', 'scratchy', 'whiskery', 'kiss'],
        ['suddenly', 'hagrid', 'howl', 'like', 'wounded', 'dog'],
        ['shhh', 'hissed', 'professor', 'mcgonagall', 'll', 'wake', 'muggles', 'sorry', 'sobbed', 'hagrid', 'taking',
         'large', 'spotted', 'handkerchief', 'burying', 'hagrid', 'face', 'handkerchief', 'stand', 'handkerchief',
         'lily', 'james', 'dead', 'poor', 'little', 'harry', 'ter', 'muggles', 'handkerchief', 'sad', 'grip', 'hagrid',
         'll', 'professor', 'mcgonagall', 'whispered', 'patting', 'hagrid', 'gingerly', 'arm', 'dumbledore', 'stepped',
         'low', 'garden', 'wall', 'walked', 'front', 'door'],
        ['dumbledore', 'laid', 'harry', 'gently', 'doorstep', 'took', 'letter', 'dumbledore', 'cloak', 'tucked',
         'letter', 'inside', 'harry', 'blankets', 'came'],
        ['full', 'minute', 'three', 'stood', 'looked', 'little', 'bundle', 'hagrid', 'shoulders', 'shook', 'professor',
         'mcgonagall', 'blinked', 'furiously', 'twinkling', 'light', 'usually', 'shone', 'dumbledore', 'eyes',
         'seemed'], ['well', 'dumbledore', 'finally'], ['ve', 'business', 'staying'],
        ['well', 'go', 'join', 'celebrations', 'hagrid', 'muffled', 'voice', 'll', 'takin', 'sirius', 'sirius', 'bike',
         'professor', 'mcgonagall', 'professor', 'dumbledore', 'sir', 'wiping', 'sirius', 'streaming', 'eyes', 'sirius',
         'jacket', 'sleeve', 'hagrid', 'swung', 'hagrid', 'onto', 'motorcycle', 'kicked', 'engine', 'roar', 'engine',
         'rose', 'air'], ['shall', 'expect', 'professor', 'mcgonagall', 'dumbledore', 'nodding', 'voice'],
        ['professor', 'mcgonagall', 'blew', 'mcgonagall', 'nose', 'reply'],
        ['dumbledore', 'turned', 'walked', 'street'], ['corner', 'dumbledore', 'stopped', 'took', 'silver', 'outer'],
        ['dumbledore', 'clicked', 'outer', 'twelve', 'balls', 'light', 'sped', 'balls', 'street', 'lamps', 'privet',
         'drive', 'glowed', 'suddenly', 'orange', 'dumbledore', 'tabby', 'cat', 'slinking', 'corner', 'street'],
        ['dumbledore', 'bundle', 'blankets', 'step', 'number', 'four'],
        ['good', 'luck', 'harry', 'dumbledore', 'murmured'],
        ['dumbledore', 'turned', 'dumbledore', 'heel', 'swish', 'dumbledore', 'cloak', 'dumbledore'],
        ['breeze', 'ruffled', 'neat', 'hedges', 'privet', 'drive', 'lay', 'silent', 'tidy', 'inky', 'sky', 'place',
         'expect', 'astonishing', 'things'],
        ['harry', 'potter', 'rolled', 'inside', 'dumbledore', 'blankets', 'without', 'waking'],
        ['small', 'hand', 'closed', 'letter', 'beside', 'dumbledore', 'dumbledore', 'slept', 'knowing', 'dumbledore',
         'special', 'knowing', 'dumbledore', 'famous', 'knowing', 'dumbledore', 'woken', 'hours', 'dursley', 'scream',
         'dursley', 'opened', 'front', 'door', 'milk', 'bottles', 'dumbledore', 'spend', 'next', 'weeks', 'prodded',
         'pinched', 'dumbledore', 'cousin', 'dudley', 'dumbledore', 'couldn', 'moment', 'people', 'meeting', 'secret',
         'country', 'holding', 'people', 'glasses', 'saying', 'hushed', 'voices', 'harry', 'potter', 'lived'],
        ['vanishing', 'glass', 'nearly', 'ten', 'years', 'passed', 'since', 'dursley', 'dursley', 'dudley', 'dursley',
         'woken', 'dursley', 'dursley', 'dudley', 'dursley', 'nephew', 'front', 'step', 'privet', 'drive', 'hardly',
         'changed'],
        ['sun', 'rose', 'tidy', 'front', 'gardens', 'lit', 'brass', 'number', 'four', 'dursley', 'dursley', 'dudley',
         'dursley', 'front', 'door', 'number', 'crept', 'dursley', 'dursley', 'dudley', 'dursley', 'living', 'room',
         'almost', 'exactly', 'dursley', 'seen', 'fateful', 'news', 'report', 'owls'],
        ['photographs', 'mantelpiece', 'really', 'showed', 'passed'],
        ['ten', 'years', 'ago', 'lots', 'pictures', 'looked', 'like', 'large', 'pink', 'beach', 'ball', 'wearing',
         'different', 'colored', 'bonnets', 'dudley', 'dursley', 'longer', 'baby', 'photographs', 'showed', 'large',
         'blond', 'riding', 'bicycle', 'carousel', 'fair', 'playing', 'computer', 'father', 'hugged', 'kissed',
         'mother'], ['room', 'held', 'sign', 'another', 'lived', 'house']]
    Res2 = [['karkaroff', 'looked', 'extremely', 'worried', 'snape', 'looked', 'angry'],
            ['karkaroff', 'hovered', 'behind', 'snape', 'desk', 'rest', 'double', 'period'],
            ['karkaroff', 'seemed', 'intent', 'preventing', 'snape', 'slipping', 'away', 'class'],
            ['keen', 'karkaroff', 'wanted', 'harry', 'deliberately', 'knocked', 'harry', 'bottle', 'armadillo', 'bile',
             'minutes', 'go', 'bell', 'gave', 'harry', 'excuse', 'duck', 'behind', 'harry', 'cauldron', 'mop', 'rest',
             'class', 'moved', 'noisily', 'toward', 'door'], ['urgent', 'harry', 'heard', 'snape', 'hiss', 'karkaroff'],
            ['karkaroff', 'harry', 'peering', 'edge', 'harry', 'cauldron', 'karkaroff', 'pull', 'left', 'hand',
             'sleeve', 'harry', 'robe', 'snape', 'something', 'harry', 'inner', 'forearm'],
            ['well', 'karkaroff', 'making', 'every', 'effort', 'harry', 'lips']]
    Res3 = [['urgent', 'harry', 'curtly'], ['ooooh', 'urgent'], ['gargoyle', 'high', 'pitched', 'voice'],
            ['well', 'us', 'place', 'hasn'], ['harry', 'knocked'],
            ['harry', 'heard', 'footsteps', 'door', 'opened', 'harry', 'harry', 'face', 'face', 'professor',
             'mcgonagall'], ['given', 'another', 'detention'],
            ['mcgonagall', 'mcgonagall', 'square', 'spectacles', 'flashing', 'alarmingly']]
    assert NAMES_COUNTER1.get_sentences() == Res1
    assert NAMES_COUNTER2.get_sentences() == Res2
    assert NAMES_COUNTER3.get_sentences() == Res3
    assert NAMES_COUNTER4.get_sentences() == Res1
    assert NAMES_COUNTER5.get_sentences() == Res2
    assert NAMES_COUNTER6.get_sentences() == Res3


def test_people_counter():
    res1 = ({'aurelius dumbledore': 32, 'aunt marge dursley': 19}, {'aurelius dumbledore': [0, 2, 2, 2, 5, 5, 9, 10, 10, 11, 12, 14, 15, 17, 18, 19, 19, 20, 21, 22, 22, 22, 22, 24, 25, 25, 25, 25, 25, 25, 25, 25], 'aunt marge dursley': [5, 5, 5, 25, 25, 26, 26, 26, 26, 26, 26, 27, 27, 27, 27, 27, 27, 27, 29]})
    res2 = ({'igor karkaroff': 8}, {'igor karkaroff': [0, 1, 2, 3, 4, 5, 5, 6]})
    res3 = ({'harry potter': 5, 'malcolm mcgonagall': 3}, {'harry potter': [0, 4, 5, 5, 5], 'malcolm mcgonagall': [5, 7, 7]})
    assert NAMES_COUNTER1.count_names() == res1
    assert NAMES_COUNTER4.count_names() == res1
    assert NAMES_COUNTER2.count_names() == res2
    assert NAMES_COUNTER5.count_names() == res2
    assert NAMES_COUNTER3.count_names() == res3
    assert NAMES_COUNTER6.count_names() == res3

def test_compare_json():
    import json

    # Write JSON files (assuming NAMES_COUNTER1 to NAMES_COUNTER6 have been defined earlier)
    NAMES_COUNTER1.write_to_json("text_analyzer/2_examples/Q3_examples/namesCounter1.json")
    NAMES_COUNTER2.write_to_json("text_analyzer/2_examples/Q3_examples/namesCounter2.json")
    NAMES_COUNTER3.write_to_json("text_analyzer/2_examples/Q3_examples/namesCounter3.json")
    NAMES_COUNTER4.write_to_json("text_analyzer/2_examples/Q3_examples/namesCounter4.json")
    NAMES_COUNTER5.write_to_json("text_analyzer/2_examples/Q3_examples/namesCounter5.json")
    NAMES_COUNTER6.write_to_json("text_analyzer/2_examples/Q3_examples/namesCounter6.json")
    assert compare_json("text_analyzer/2_examples/Q3_examples/namesCounter1.json","text_analyzer/2_examples/Q3_examples/example_1/Q3_result1.json")
    assert compare_json("text_analyzer/2_examples/Q3_examples/namesCounter2.json","text_analyzer/2_examples/Q3_examples/example_2/Q3_result2.json")
    assert compare_json("text_analyzer/2_examples/Q3_examples/namesCounter3.json","text_analyzer/2_examples/Q3_examples/example_3/Q3_result3.json")
    assert compare_json("text_analyzer/2_examples/Q3_examples/namesCounter4.json","text_analyzer/2_examples/Q3_examples/example_1/Q3_result1.json")
    assert compare_json("text_analyzer/2_examples/Q3_examples/namesCounter5.json","text_analyzer/2_examples/Q3_examples/example_2/Q3_result2.json")
    assert compare_json("text_analyzer/2_examples/Q3_examples/namesCounter6.json","text_analyzer/2_examples/Q3_examples/example_3/Q3_result3.json")

