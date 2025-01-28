import json
import string

import Preprocesser
from Preprocesser import process_sentence
from Preprocesser import Preprocessor

preprocessor_1 = Preprocessor(1,
                              peopleInputPath="text_analyzer/2_examples/Q1_examples/example_1/people_small_1.csv",
                              sentenceInputPath="text_analyzer/2_examples/Q1_examples/example_1/sentences_small_1.csv",
                              removeInputPath="text_analyzer/1_data/Data/REMOVEWORDS.csv")
preprocessor_2 = Preprocessor(1, peopleInputPath="text_analyzer/2_examples/Q1_examples/example_2/people_small_2.csv",
                              sentenceInputPath="text_analyzer/2_examples/Q1_examples/example_2/sentences_small_2.csv",
                              removeInputPath="text_analyzer/1_data/Data/REMOVEWORDS.csv")
preprocessor_3 = Preprocessor(1, peopleInputPath="text_analyzer/2_examples/Q1_examples/example_3/people_small_3.csv",
                              sentenceInputPath="text_analyzer/2_examples/Q1_examples/example_3/sentences_small_3.csv",
                              removeInputPath="text_analyzer/1_data/Data/REMOVEWORDS.csv")


def test_preprocesser_text():
    assert process_sentence("H   i") == "h i"
    assert process_sentence("Mr.Alix") == "mr alix"
    assert process_sentence("mr   dunder") == "mr dunder"
    assert process_sentence(" Mr. Potter ") == "mr potter"
    assert process_sentence("Mr.") == "mr"
    res1 = ("under a tuft of jet black hair over boy forehead dumbledore and mcgonagall could see a curiously shaped "
            "cut like a bolt of lightning")
    input1 = ("Under a tuft of jet- black hair over boy forehead Dumbledore and  McGonagall could see a curiously "
              "shaped cut, like a bolt of lightning.")
    assert process_sentence(input1) == res1
    input2 = ("Ten years ago, there had been lots of pictures of what looked like a large pink beach ball wearing "
              "different- colored bonnets-- but    Dudley Dursley was no longer a baby, and now the photographs "
              "showed a large blond boy riding boy first bicycle, on a carousel at the fair, playing a computer game "
              "with boy father, being hugged and kissed by boy mother.")
    res2 = ("ten years ago there had been lots of pictures of what looked like a large pink beach ball wearing "
            "different colored bonnets but dudley dursley was no longer a baby and now the photographs showed a large "
            "blond boy riding boy first bicycle on a carousel at the fair playing a computer game with boy father "
            "being hugged and kissed by boy mother")
    assert process_sentence(input2) == res2
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
    hashDict = Preprocesser.hash_dict_for_punctuation()

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


# Function to load a JSON file into a Python dictionary
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


def test_csv_file():
    preprocessor_1.write_result_to_json("text_analyzer/res1.json")
    preprocessor_2.write_result_to_json("text_analyzer/res2.json")
    preprocessor_3.write_result_to_json("text_analyzer/res3.json")
    assert (compare_json("text_analyzer/2_examples/Q1_examples/example_1/Q1_result1.json",
                         "text_analyzer/res1.json"))
    assert (compare_json("text_analyzer/2_examples/Q1_examples/example_2/Q1_result2.json",
                         "text_analyzer/res2.json"))
    assert (compare_json("text_analyzer/2_examples/Q1_examples/example_3/Q1_result3.json",
                         "text_analyzer/res3.json"))


def test_SentencePreprocessor():
    """
    Test the SentencePreprocessor processing the sentence
    :return: assert the sentence is equal to the preprocessed sentence
    """
    sentencelist3 = [['urgent', 'harry', 'curtly'], ['ooooh', 'urgent'], ['gargoyle', 'high', 'pitched', 'voice'],
                     ['well', 'us', 'place', 'hasn'], ['harry', 'knocked'],
                     ['harry', 'heard', 'footsteps', 'door', 'opened', 'harry', 'harry', 'face', 'face', 'professor',
                      'mcgonagall'], ['given', 'another', 'detention'],
                     ['mcgonagall', 'mcgonagall', 'square', 'spectacles', 'flashing', 'alarmingly']]
    sentencelist2 = [['karkaroff', 'looked', 'extremely', 'worried', 'snape', 'looked', 'angry'],
                     ['karkaroff', 'hovered', 'behind', 'snape', 'desk', 'rest', 'double', 'period'],
                     ['karkaroff', 'seemed', 'intent', 'preventing', 'snape', 'slipping', 'away', 'class'],
                     ['keen', 'karkaroff', 'wanted', 'harry', 'deliberately', 'knocked', 'harry', 'bottle', 'armadillo',
                      'bile', 'minutes', 'go', 'bell', 'gave', 'harry', 'excuse', 'duck', 'behind', 'harry', 'cauldron',
                      'mop', 'rest', 'class', 'moved', 'noisily', 'toward', 'door'],
                     ['urgent', 'harry', 'heard', 'snape', 'hiss', 'karkaroff'],
                     ['karkaroff', 'harry', 'peering', 'edge', 'harry', 'cauldron', 'karkaroff', 'pull', 'left', 'hand',
                      'sleeve', 'harry', 'robe', 'snape', 'something', 'harry', 'inner', 'forearm'],
                     ['well', 'karkaroff', 'making', 'every', 'effort', 'harry', 'lips']]
    sentencelist1 = [
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
         'lily',
         'james', 'dead', 'poor', 'little', 'harry', 'ter', 'muggles', 'handkerchief', 'sad', 'grip', 'hagrid', 'll',
         'professor', 'mcgonagall', 'whispered', 'patting', 'hagrid', 'gingerly', 'arm', 'dumbledore', 'stepped', 'low',
         'garden', 'wall', 'walked', 'front', 'door'],
        ['dumbledore', 'laid', 'harry', 'gently', 'doorstep', 'took', 'letter', 'dumbledore', 'cloak', 'tucked',
         'letter',
         'inside', 'harry', 'blankets', 'came'],
        ['full', 'minute', 'three', 'stood', 'looked', 'little', 'bundle', 'hagrid', 'shoulders', 'shook', 'professor',
         'mcgonagall', 'blinked', 'furiously', 'twinkling', 'light', 'usually', 'shone', 'dumbledore', 'eyes',
         'seemed'],
        ['well', 'dumbledore', 'finally'], ['ve', 'business', 'staying'],
        ['well', 'go', 'join', 'celebrations', 'hagrid', 'muffled', 'voice', 'll', 'takin', 'sirius', 'sirius', 'bike',
         'professor', 'mcgonagall', 'professor', 'dumbledore', 'sir', 'wiping', 'sirius', 'streaming', 'eyes', 'sirius',
         'jacket', 'sleeve', 'hagrid', 'swung', 'hagrid', 'onto', 'motorcycle', 'kicked', 'engine', 'roar', 'engine',
         'rose', 'air'], ['shall', 'expect', 'professor', 'mcgonagall', 'dumbledore', 'nodding', 'voice'],
        ['professor', 'mcgonagall', 'blew', 'mcgonagall', 'nose', 'reply'],
        ['dumbledore', 'turned', 'walked', 'street'],
        ['corner', 'dumbledore', 'stopped', 'took', 'silver', 'outer'],
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
         'mother'],
        ['room', 'held', 'sign', 'another', 'lived', 'house']]
    assert preprocessor_3.getSentences() == sentencelist3
    assert preprocessor_2.getSentences() == sentencelist2
    assert preprocessor_1.getSentences() == sentencelist1


def test_preprocessor_people_proccesing():
    peopleList1 = [[['attentive', 'wizard'], []], [['bertram', 'aubrey'], []], [['audrey', 'weasley'], []],
                   [['augusta', 'gran', 'longbottom'], []], [['augustus', 'pye'], []], [['augustus', 'rookwood'], []],
                   [['augustus', 'worme'], []], [['auntie', 'muriel'], []], [['aunt', 'marge', 'dursley'], []],
                   [['aurelius', 'dumbledore'], []], [['aurora', 'sinistra'], []], [['avery'], []],
                   [['babajide', 'akingbade'], []], [['babayaga'], []], [['babbitty', 'rabbitty'], []],
                   [['bagman', 'sr'], []], [['ludo', 'bagman'], []], [['otto', 'bagman'], []],
                   [['millicent', 'bagnold'], []], [['bathilda', 'bagshot'], [['batty']]],
                   [['kquewanda', 'bailey'], []],
                   [['ballyfumble', 'stranger'], [['quin'], ['quivering', 'quintus'], ['quintusofthesillyname']]]]
    peopleList2 = [[['ignatia', 'wildsmith'], []], [['ignatius', 'prewett'], []], [['ignatius', 'tuft'], []],
                   [['ignotus', 'peverell'], []], [['igor', 'karkaroff'], []], [['illyius'], []],
                   [['ingolfr', 'iambic'], []]]
    peopleList3 = [[['magnus', 'dent', 'macdonald'], []], [['magorian'], []], [['maisie', 'cattermole'], []],
                   [['malcolm'], []], [['malcolm', 'baddock'], []], [['malcolm', 'mcgonagall'], []],
                   [['harold', 'skively'], []], [['harper'], []], [['harry', 'potter'],
                                                                   [['lived'], ['undesirable', 'number'], ['chosen'],
                                                                    ['parry', 'otter'], ['chosen'],
                                                                    ['mudbloods', 'friend']]],
                   [['harvey', 'ridgebit'], []], [['hassan', 'mostafa'], []]]

    assert preprocessor_1.get_people() == peopleList1
    assert preprocessor_2.get_people() == peopleList2
    assert preprocessor_3.get_people() == peopleList3


def test_preprocessor_words_to_remove():
    removesDict = {'a': True, 'about': True, 'above': True, 'actual': True, 'after': True, 'again': True, 'against': True, 'all': True, 'alreadi': True, 'also': True, 'alway': True, 'am': True, 'amp': True, 'an': True, 'and': True, 'ani': True, 'anoth': True, 'any': True, 'anyth': True, 'are': True, 'around': True, 'as': True, 'at': True, 'aww': True, 'babi': True, 'back': True, 'be': True, 'becaus': True, 'because': True, 'bed': True, 'been': True, 'befor': True, 'before': True, 'being': True, 'below': True, 'between': True, 'birthday': True, 'bit': True, 'book': True, 'both': True, 'boy': True, 'but': True, 'by': True, 'call': True, 'can': True, 'cannot': True, 'cant': True, 'car': True, 'check': True, 'com': True, 'come': True, 'could': True, 'day': True, 'did': True, 'didn': True, 'dinner': True, 'do': True, 'doe': True, 'does': True, 'doesn': True, 'doing': True, 'don': True, 'done': True, 'dont': True, 'down': True, 'during': True, 'each': True, 'eat': True, 'end': True, 'even': True, 'ever': True, 'everyon': True, 'exam': True, 'famili': True, 'feel': True, 'few': True, 'final': True, 'find': True, 'first': True, 'follow': True, 'for': True, 'found': True, 'friday': True, 'from': True, 'further': True, 'game': True, 'get': True, 'girl': True, 'give': True, 'gone': True, 'gonna': True, 'got': True, 'gotta': True, 'guess': True, 'guy': True, 'had': True, 'hair': True, 'happen': True, 'has': True, 'have': True, 'haven': True, 'having': True, 'he': True, 'head': True, 'hear': True, 'her': True, 'here': True, 'hers': True, 'herself': True, 'hey': True, 'him': True, 'himself': True, 'his': True, 'home': True, 'hour': True, 'hous': True, 'how': True, 'http': True, 'i': True, 'if': True, 'im': True, 'in': True, 'into': True, 'is': True, 'isn': True, 'it': True, 'its': True, 'itself': True, 'job': True, 'just': True, 'keep': True, 'know': True, 'last': True, 'later': True, 'least': True, 'leav': True, 'let': True, 'life': True, 'listen': True, 'littl': True, 'live': True, 'look': True, 'lot': True, 'lunch': True, 'made': True, 'make': True, 'man': True, 'mani': True, 'may': True, 'mayb': True, 'me': True, 'mean': True, 'meet': True, 'might': True, 'mom': True, 'monday': True, 'month': True, 'more': True, 'morn': True, 'most': True, 'move': True, 'movi': True, 'much': True, 'must': True, 'my': True, 'myself': True, 'need': True, 'never': True, 'new': True, 'night': True, 'no': True, 'nor': True, 'not': True, 'noth': True, 'now': True, 'of': True, 'off': True, 'on': True, 'once': True, 'one': True, 'onli': True, 'only': True, 'or': True, 'other': True, 'ought': True, 'our': True, 'ours': True, 'ourselves': True, 'out': True, 'over': True, 'own': True, 'peopl': True, 'phone': True, 'pic': True, 'pictur': True, 'play': True, 'post': True, 'put': True, 'quot': True, 'rain': True, 'read': True, 'readi': True, 'realli': True, 'run': True, 'said': True, 'same': True, 'saw': True, 'say': True, 'school': True, 'see': True, 'seem': True, 'she': True, 'shop': True, 'should': True, 'show': True, 'sinc': True, 'sleep': True, 'so': True, 'some': True, 'someon': True, 'someth': True, 'song': True, 'soon': True, 'sound': True, 'start': True, 'stay': True, 'still': True, 'studi': True, 'stuff': True, 'such': True, 'summer': True, 'sunday': True, 'sure': True, 'take': True, 'talk': True, 'tell': True, 'than': True, 'thank': True, 'that': True, 'the': True, 'their': True, 'theirs': True, 'them': True, 'themselves': True, 'then': True, 'there': True, 'these': True, 'they': True, 'thing': True, 'think': True, 'this': True, 'those': True, 'though': True, 'thought': True, 'through': True, 'time': True, 'to': True, 'today': True, 'tomorrow': True, 'tonight': True, 'too': True, 'total': True, 'tri': True, 'tweet': True, 'twitpic': True, 'twitter': True, 'two': True, 'u': True, 'under': True, 'until': True, 'up': True, 'updat': True, 'use': True, 'veri': True, 'very': True, 'video': True, 'wait': True, 'wanna': True, 'want': True, 'was': True, 'watch': True, 'way': True, 'we': True, 'weather': True, 'week': True, 'weekend': True, 'went': True, 'were': True, 'what': True, 'when': True, 'where': True, 'whi': True, 'which': True, 'while': True, 'who': True, 'whom': True, 'why': True, 'will': True, 'with': True, 'woke': True, 'won': True, 'work': True, 'world': True, 'would': True, 'www': True, 'yay': True, 'yeah': True, 'year': True, 'yes': True, 'yesterday': True, 'yet': True, 'you': True, 'your': True, 'yours': True, 'yourself': True, 'yourselves': True, 'b': True, 'c': True, 'd': True, 'e': True, 'f': True, 'g': True, 'h': True, 'j': True, 'k': True, 'l': True, 'm': True, 'n': True, 'o': True, 'p': True, 'r': True, 's': True, 't': True, 'v': True, 'w': True, 'x': True, 'z': True, 'mr': True, 'miss': True, 'mrs': True, 'ms': True}


    assert preprocessor_1.get_remove_words() == removesDict
    assert preprocessor_2.get_remove_words() == removesDict
    assert preprocessor_3.get_remove_words() == removesDict
