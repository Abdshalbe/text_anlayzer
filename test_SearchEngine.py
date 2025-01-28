import json

import pytest
from SearchEngine import SearchEngine

searchEngine1 = SearchEngine(4,
                             sentence_input_path="text_analyzer/2_examples/Q4_examples/example_1/sentences_small_1.csv",
                             remove_input_path="text_analyzer/1_data/Data/REMOVEWORDS.csv",
                             kSeqJson="text_analyzer/2_examples/Q4_examples/example_1/kseq_query_keys_1.json")

searchEngine2 = SearchEngine(4,
                             sentence_input_path="text_analyzer/2_examples/Q4_examples/example_2/sentences_small_2.csv",
                             remove_input_path="text_analyzer/1_data/Data/REMOVEWORDS.csv",
                             kSeqJson="text_analyzer/2_examples/Q4_examples/example_2/kseq_query_keys_2.json")

searchEngine3 = SearchEngine(4,
                             sentence_input_path="text_analyzer/2_examples/Q4_examples/example_3/sentences_small_3.csv",
                             remove_input_path="text_analyzer/1_data/Data/REMOVEWORDS.csv",
                             kSeqJson="text_analyzer/2_examples/Q4_examples/example_3/kseq_query_keys_3.json")

searchEngine4 = SearchEngine(4,
                             sentence_input_path="text_analyzer/2_examples/Q4_examples/example_4/sentences_small_4.csv",
                             remove_input_path="text_analyzer/1_data/Data/REMOVEWORDS.csv",
                             kSeqJson="text_analyzer/2_examples/Q4_examples/example_4/kseq_query_keys_4.json")

searchEngine5 = SearchEngine(4, jsonInputFile="text_analyzer/2_examples/Q1_examples/example_1/Q1_result1.json",
                             preprocessed=True,
                             kSeqJson="text_analyzer/2_examples/Q4_examples/example_1/kseq_query_keys_1.json")

searchEngine6 = SearchEngine(4, jsonInputFile="text_analyzer/2_examples/Q1_examples/example_2/Q1_result2.json",
                             preprocessed=True,
                             kSeqJson="text_analyzer/2_examples/Q4_examples/example_2/kseq_query_keys_2.json")

searchEngine7 = SearchEngine(4, jsonInputFile="text_analyzer/2_examples/Q1_examples/example_3/Q1_result3.json",
                             preprocessed=True,
                             kSeqJson="text_analyzer/2_examples/Q4_examples/example_3/kseq_query_keys_3.json")


def test_SearchEngine():
    assert searchEngine1.search_in_supplied_text(['tuft', 'jet']) == [
        ['tuft', 'jet', 'black', 'forehead', 'dumbledore', 'mcgonagall', 'curiously', 'shaped', 'cut', 'like', 'bolt',
         'lightning']]
    assert searchEngine1.search_in_supplied_text(['hugged', 'kissed']) == [
        ['ten', 'years', 'ago', 'lots', 'pictures', 'looked', 'like', 'large', 'pink', 'beach', 'ball', 'wearing',
         'different', 'colored', 'bonnets', 'dudley', 'dursley', 'longer', 'baby', 'photographs', 'showed', 'large',
         'blond', 'riding', 'bicycle', 'carousel', 'fair', 'playing', 'computer', 'father', 'hugged', 'kissed',
         'mother']]
    assert searchEngine1.search_in_supplied_text(['hello', 'world']) == []
    assert searchEngine1.search_in_supplied_text(["drive"]) == [
        ['dumbledore', 'clicked', 'outer', 'twelve', 'balls', 'light', 'sped', 'balls', 'street', 'lamps', 'privet',
         'drive', 'glowed', 'suddenly', 'orange', 'dumbledore', 'tabby', 'cat', 'slinking', 'corner', 'street'],
        ['breeze', 'ruffled', 'neat', 'hedges', 'privet', 'drive', 'lay', 'silent', 'tidy', 'inky', 'sky', 'place',
         'expect', 'astonishing', 'things'],
        ['vanishing', 'glass', 'nearly', 'ten', 'years', 'passed', 'since', 'dursley', 'dursley', 'dudley', 'dursley',
         'woken', 'dursley', 'dursley', 'dudley', 'dursley', 'nephew', 'front', 'step', 'privet', 'drive', 'hardly',
         'changed']]
    assert searchEngine5.search_in_supplied_text(['tuft', 'jet']) == [
        ['tuft', 'jet', 'black', 'forehead', 'dumbledore', 'mcgonagall', 'curiously', 'shaped', 'cut', 'like', 'bolt',
         'lightning']]
    assert searchEngine5.search_in_supplied_text(['hugged', 'kissed']) == [
        ['ten', 'years', 'ago', 'lots', 'pictures', 'looked', 'like', 'large', 'pink', 'beach', 'ball', 'wearing',
         'different', 'colored', 'bonnets', 'dudley', 'dursley', 'longer', 'baby', 'photographs', 'showed', 'large',
         'blond', 'riding', 'bicycle', 'carousel', 'fair', 'playing', 'computer', 'father', 'hugged', 'kissed',
         'mother']]
    assert searchEngine5.search_in_supplied_text(['hello', 'world']) == []
    assert searchEngine5.search_in_supplied_text(["drive"]) == [
        ['dumbledore', 'clicked', 'outer', 'twelve', 'balls', 'light', 'sped', 'balls', 'street', 'lamps', 'privet',
         'drive', 'glowed', 'suddenly', 'orange', 'dumbledore', 'tabby', 'cat', 'slinking', 'corner', 'street'],
        ['breeze', 'ruffled', 'neat', 'hedges', 'privet', 'drive', 'lay', 'silent', 'tidy', 'inky', 'sky', 'place',
         'expect', 'astonishing', 'things'],
        ['vanishing', 'glass', 'nearly', 'ten', 'years', 'passed', 'since', 'dursley', 'dursley', 'dudley', 'dursley',
         'woken', 'dursley', 'dursley', 'dudley', 'dursley', 'nephew', 'front', 'step', 'privet', 'drive', 'hardly',
         'changed']]
    assert searchEngine2.search_in_supplied_text(["harry"]) == [
        ['keen', 'karkaroff', 'wanted', 'harry', 'deliberately', 'knocked', 'harry', 'bottle', 'armadillo', 'bile',
         'minutes', 'go', 'bell', 'gave', 'harry', 'excuse', 'duck', 'behind', 'harry', 'cauldron', 'mop', 'rest',
         'class', 'moved', 'noisily', 'toward', 'door'], ['urgent', 'harry', 'heard', 'snape', 'hiss', 'karkaroff'],
        ['karkaroff', 'harry', 'peering', 'edge', 'harry', 'cauldron', 'karkaroff', 'pull', 'left', 'hand', 'sleeve',
         'harry', 'robe', 'snape', 'something', 'harry', 'inner', 'forearm'],
        ['well', 'karkaroff', 'making', 'every', 'effort', 'harry', 'lips']]
    assert searchEngine2.search_in_supplied_text(['rest', 'double']) == [
        ['karkaroff', 'hovered', 'behind', 'snape', 'desk', 'rest', 'double', 'period']]
    assert searchEngine2.search_in_supplied_text(["water"]) == []
    assert searchEngine2.search_in_supplied_text(["robe"]) == [
        ['karkaroff', 'harry', 'peering', 'edge', 'harry', 'cauldron', 'karkaroff', 'pull', 'left', 'hand', 'sleeve',
         'harry', 'robe', 'snape', 'something', 'harry', 'inner', 'forearm']]
    assert searchEngine6.search_in_supplied_text(["harry"]) == [
        ['keen', 'karkaroff', 'wanted', 'harry', 'deliberately', 'knocked', 'harry', 'bottle', 'armadillo', 'bile',
         'minutes', 'go', 'bell', 'gave', 'harry', 'excuse', 'duck', 'behind', 'harry', 'cauldron', 'mop', 'rest',
         'class', 'moved', 'noisily', 'toward', 'door'], ['urgent', 'harry', 'heard', 'snape', 'hiss', 'karkaroff'],
        ['karkaroff', 'harry', 'peering', 'edge', 'harry', 'cauldron', 'karkaroff', 'pull', 'left', 'hand', 'sleeve',
         'harry', 'robe', 'snape', 'something', 'harry', 'inner', 'forearm'],
        ['well', 'karkaroff', 'making', 'every', 'effort', 'harry', 'lips']]
    assert searchEngine6.search_in_supplied_text(['rest', 'double']) == [
        ['karkaroff', 'hovered', 'behind', 'snape', 'desk', 'rest', 'double', 'period']]
    assert searchEngine6.search_in_supplied_text(["water"]) == []
    assert searchEngine6.search_in_supplied_text(["robe"]) == [
        ['karkaroff', 'harry', 'peering', 'edge', 'harry', 'cauldron', 'karkaroff', 'pull', 'left', 'hand', 'sleeve',
         'harry', 'robe', 'snape', 'something', 'harry', 'inner', 'forearm']]
    assert searchEngine3.search_in_supplied_text(["harry"]) == [['urgent', 'harry', 'curtly'], ['harry', 'knocked'],
                                                                ['harry', 'heard', 'footsteps', 'door', 'opened',
                                                                 'harry', 'harry', 'face', 'face', 'professor',
                                                                 'mcgonagall']]
    assert searchEngine3.search_in_supplied_text(["mcgonagall"]) == [
        ['harry', 'heard', 'footsteps', 'door', 'opened', 'harry', 'harry', 'face', 'face', 'professor', 'mcgonagall'],
        ['mcgonagall', 'mcgonagall', 'square', 'spectacles', 'flashing', 'alarmingly']]
    assert searchEngine3.search_in_supplied_text(["given"]) == [['given', 'another', 'detention']]
    assert searchEngine3.search_in_supplied_text(["data"]) == []
    assert searchEngine7.search_in_supplied_text(["urgent"]) == [['urgent', 'harry', 'curtly'], ['ooooh', 'urgent']]
    assert searchEngine7.search_in_supplied_text(["mcgonagall"]) == [
        ['harry', 'heard', 'footsteps', 'door', 'opened', 'harry', 'harry', 'face', 'face', 'professor', 'mcgonagall'],
        ['mcgonagall', 'mcgonagall', 'square', 'spectacles', 'flashing', 'alarmingly']]
    assert searchEngine7.search_in_supplied_text(["programs"]) == []
    assert searchEngine7.search_in_supplied_text(["voice"]) == [['gargoyle', 'high', 'pitched', 'voice']]


def test_result_KseqData():
    assert searchEngine7.result_KseqData() == {('another',): [['given', 'another', 'detention']], ('harry', 'heard'): [
        ['harry', 'heard', 'footsteps', 'door', 'opened', 'harry', 'harry', 'face', 'face', 'professor', 'mcgonagall']],
                                               ('knocked',): [['harry', 'knocked']],
                                               ('well', 'go', 'join', 'celebrations'): []}
    assert searchEngine3.result_KseqData() == {('another',): [['given', 'another', 'detention']], ('harry', 'heard'): [
        ['harry', 'heard', 'footsteps', 'door', 'opened', 'harry', 'harry', 'face', 'face', 'professor', 'mcgonagall']],
                                               ('knocked',): [['harry', 'knocked']],
                                               ('well', 'go', 'join', 'celebrations'): []}
    assert searchEngine6.result_KseqData() == {
        ('harry', 'heard'): [['urgent', 'harry', 'heard', 'snape', 'hiss', 'karkaroff']], ('karkaroff',): [
            ['karkaroff', 'harry', 'peering', 'edge', 'harry', 'cauldron', 'karkaroff', 'pull', 'left', 'hand',
             'sleeve', 'harry', 'robe', 'snape', 'something', 'harry', 'inner', 'forearm'],
            ['karkaroff', 'hovered', 'behind', 'snape', 'desk', 'rest', 'double', 'period'],
            ['karkaroff', 'looked', 'extremely', 'worried', 'snape', 'looked', 'angry'],
            ['karkaroff', 'seemed', 'intent', 'preventing', 'snape', 'slipping', 'away', 'class'],
            ['keen', 'karkaroff', 'wanted', 'harry', 'deliberately', 'knocked', 'harry', 'bottle', 'armadillo', 'bile',
             'minutes', 'go', 'bell', 'gave', 'harry', 'excuse', 'duck', 'behind', 'harry', 'cauldron', 'mop', 'rest',
             'class', 'moved', 'noisily', 'toward', 'door'], ['urgent', 'harry', 'heard', 'snape', 'hiss', 'karkaroff'],
            ['well', 'karkaroff', 'making', 'every', 'effort', 'harry', 'lips']],
        ('lips',): [['well', 'karkaroff', 'making', 'every', 'effort', 'harry', 'lips']],
        ('snape', 'looked'): [['karkaroff', 'looked', 'extremely', 'worried', 'snape', 'looked', 'angry']],
        ('well', 'go', 'join', 'celebrations'): []}
    assert searchEngine2.result_KseqData() == {
        ('harry', 'heard'): [['urgent', 'harry', 'heard', 'snape', 'hiss', 'karkaroff']], ('karkaroff',): [
            ['karkaroff', 'harry', 'peering', 'edge', 'harry', 'cauldron', 'karkaroff', 'pull', 'left', 'hand',
             'sleeve', 'harry', 'robe', 'snape', 'something', 'harry', 'inner', 'forearm'],
            ['karkaroff', 'hovered', 'behind', 'snape', 'desk', 'rest', 'double', 'period'],
            ['karkaroff', 'looked', 'extremely', 'worried', 'snape', 'looked', 'angry'],
            ['karkaroff', 'seemed', 'intent', 'preventing', 'snape', 'slipping', 'away', 'class'],
            ['keen', 'karkaroff', 'wanted', 'harry', 'deliberately', 'knocked', 'harry', 'bottle', 'armadillo', 'bile',
             'minutes', 'go', 'bell', 'gave', 'harry', 'excuse', 'duck', 'behind', 'harry', 'cauldron', 'mop', 'rest',
             'class', 'moved', 'noisily', 'toward', 'door'], ['urgent', 'harry', 'heard', 'snape', 'hiss', 'karkaroff'],
            ['well', 'karkaroff', 'making', 'every', 'effort', 'harry', 'lips']],
        ('lips',): [['well', 'karkaroff', 'making', 'every', 'effort', 'harry', 'lips']],
        ('snape', 'looked'): [['karkaroff', 'looked', 'extremely', 'worried', 'snape', 'looked', 'angry']],
        ('well', 'go', 'join', 'celebrations'): []}
    assert searchEngine5.result_KseqData() == {('breeze', 'ruffled'): [
        ['breeze', 'ruffled', 'neat', 'hedges', 'privet', 'drive', 'lay', 'silent', 'tidy', 'inky', 'sky', 'place',
         'expect', 'astonishing', 'things']], ('dumbledore',): [
        ['corner', 'dumbledore', 'stopped', 'took', 'silver', 'outer'],
        ['dumbledore', 'bundle', 'blankets', 'step', 'number', 'four'],
        ['dumbledore', 'clicked', 'outer', 'twelve', 'balls', 'light', 'sped', 'balls', 'street', 'lamps', 'privet',
         'drive', 'glowed', 'suddenly', 'orange', 'dumbledore', 'tabby', 'cat', 'slinking', 'corner', 'street'],
        ['dumbledore', 'dumbledore', 'll', 'scar', 'forever', 'couldn', 'something', 'scar', 'dumbledore', 'wouldn'],
        ['dumbledore', 'laid', 'harry', 'gently', 'doorstep', 'took', 'letter', 'dumbledore', 'cloak', 'tucked',
         'letter', 'inside', 'harry', 'blankets', 'came'],
        ['dumbledore', 'turned', 'dumbledore', 'heel', 'swish', 'dumbledore', 'cloak', 'dumbledore'],
        ['dumbledore', 'turned', 'walked', 'street'],
        ['full', 'minute', 'three', 'stood', 'looked', 'little', 'bundle', 'hagrid', 'shoulders', 'shook', 'professor',
         'mcgonagall', 'blinked', 'furiously', 'twinkling', 'light', 'usually', 'shone', 'dumbledore', 'eyes',
         'seemed'], ['good', 'luck', 'harry', 'dumbledore', 'murmured'],
        ['harry', 'potter', 'rolled', 'inside', 'dumbledore', 'blankets', 'without', 'waking'],
        ['shall', 'expect', 'professor', 'mcgonagall', 'dumbledore', 'nodding', 'voice'],
        ['shhh', 'hissed', 'professor', 'mcgonagall', 'll', 'wake', 'muggles', 'sorry', 'sobbed', 'hagrid', 'taking',
         'large', 'spotted', 'handkerchief', 'burying', 'hagrid', 'face', 'handkerchief', 'stand', 'handkerchief',
         'lily', 'james', 'dead', 'poor', 'little', 'harry', 'ter', 'muggles', 'handkerchief', 'sad', 'grip', 'hagrid',
         'll', 'professor', 'mcgonagall', 'whispered', 'patting', 'hagrid', 'gingerly', 'arm', 'dumbledore', 'stepped',
         'low', 'garden', 'wall', 'walked', 'front', 'door'],
        ['small', 'hand', 'closed', 'letter', 'beside', 'dumbledore', 'dumbledore', 'slept', 'knowing', 'dumbledore',
         'special', 'knowing', 'dumbledore', 'famous', 'knowing', 'dumbledore', 'woken', 'hours', 'dursley', 'scream',
         'dursley', 'opened', 'front', 'door', 'milk', 'bottles', 'dumbledore', 'spend', 'next', 'weeks', 'prodded',
         'pinched', 'dumbledore', 'cousin', 'dudley', 'dumbledore', 'couldn', 'moment', 'people', 'meeting', 'secret',
         'country', 'holding', 'people', 'glasses', 'saying', 'hushed', 'voices', 'harry', 'potter', 'lived'],
        ['tuft', 'jet', 'black', 'forehead', 'dumbledore', 'mcgonagall', 'curiously', 'shaped', 'cut', 'like', 'bolt',
         'lightning'], ['well', 'dumbledore', 'finally'],
        ['well', 'dumbledore', 'hagrid', 'better', 'dumbledore', 'took', 'harry', 'harry', 'arms', 'turned', 'toward',
         'dursley', 'dursley', 'dudley', 'dursley', 'house'],
        ['well', 'go', 'join', 'celebrations', 'hagrid', 'muffled', 'voice', 'll', 'takin', 'sirius', 'sirius', 'bike',
         'professor', 'mcgonagall', 'professor', 'dumbledore', 'sir', 'wiping', 'sirius', 'streaming', 'eyes', 'sirius',
         'jacket', 'sleeve', 'hagrid', 'swung', 'hagrid', 'onto', 'motorcycle', 'kicked', 'engine', 'roar', 'engine',
         'rose', 'air']], ('dumbledore', 'finally'): [['well', 'dumbledore', 'finally']],
                                               ('hagrid', 'muffled', 'voice'): [
                                                   ['well', 'go', 'join', 'celebrations', 'hagrid', 'muffled', 'voice',
                                                    'll', 'takin', 'sirius', 'sirius', 'bike', 'professor',
                                                    'mcgonagall', 'professor', 'dumbledore', 'sir', 'wiping', 'sirius',
                                                    'streaming', 'eyes', 'sirius', 'jacket', 'sleeve', 'hagrid',
                                                    'swung', 'hagrid', 'onto', 'motorcycle', 'kicked', 'engine', 'roar',
                                                    'engine', 'rose', 'air']], ('small', 'hand', 'closed'): [
            ['small', 'hand', 'closed', 'letter', 'beside', 'dumbledore', 'dumbledore', 'slept', 'knowing',
             'dumbledore', 'special', 'knowing', 'dumbledore', 'famous', 'knowing', 'dumbledore', 'woken', 'hours',
             'dursley', 'scream', 'dursley', 'opened', 'front', 'door', 'milk', 'bottles', 'dumbledore', 'spend',
             'next', 'weeks', 'prodded', 'pinched', 'dumbledore', 'cousin', 'dudley', 'dumbledore', 'couldn', 'moment',
             'people', 'meeting', 'secret', 'country', 'holding', 'people', 'glasses', 'saying', 'hushed', 'voices',
             'harry', 'potter', 'lived']], ('well', 'go', 'join', 'celebrations'): [
            ['well', 'go', 'join', 'celebrations', 'hagrid', 'muffled', 'voice', 'll', 'takin', 'sirius', 'sirius',
             'bike', 'professor', 'mcgonagall', 'professor', 'dumbledore', 'sir', 'wiping', 'sirius', 'streaming',
             'eyes', 'sirius', 'jacket', 'sleeve', 'hagrid', 'swung', 'hagrid', 'onto', 'motorcycle', 'kicked',
             'engine', 'roar', 'engine', 'rose', 'air']]}
    assert searchEngine1.result_KseqData() == {('breeze', 'ruffled'): [
        ['breeze', 'ruffled', 'neat', 'hedges', 'privet', 'drive', 'lay', 'silent', 'tidy', 'inky', 'sky', 'place',
         'expect', 'astonishing', 'things']], ('dumbledore',): [
        ['corner', 'dumbledore', 'stopped', 'took', 'silver', 'outer'],
        ['dumbledore', 'bundle', 'blankets', 'step', 'number', 'four'],
        ['dumbledore', 'clicked', 'outer', 'twelve', 'balls', 'light', 'sped', 'balls', 'street', 'lamps', 'privet',
         'drive', 'glowed', 'suddenly', 'orange', 'dumbledore', 'tabby', 'cat', 'slinking', 'corner', 'street'],
        ['dumbledore', 'dumbledore', 'll', 'scar', 'forever', 'couldn', 'something', 'scar', 'dumbledore', 'wouldn'],
        ['dumbledore', 'laid', 'harry', 'gently', 'doorstep', 'took', 'letter', 'dumbledore', 'cloak', 'tucked',
         'letter', 'inside', 'harry', 'blankets', 'came'],
        ['dumbledore', 'turned', 'dumbledore', 'heel', 'swish', 'dumbledore', 'cloak', 'dumbledore'],
        ['dumbledore', 'turned', 'walked', 'street'],
        ['full', 'minute', 'three', 'stood', 'looked', 'little', 'bundle', 'hagrid', 'shoulders', 'shook', 'professor',
         'mcgonagall', 'blinked', 'furiously', 'twinkling', 'light', 'usually', 'shone', 'dumbledore', 'eyes',
         'seemed'], ['good', 'luck', 'harry', 'dumbledore', 'murmured'],
        ['harry', 'potter', 'rolled', 'inside', 'dumbledore', 'blankets', 'without', 'waking'],
        ['shall', 'expect', 'professor', 'mcgonagall', 'dumbledore', 'nodding', 'voice'],
        ['shhh', 'hissed', 'professor', 'mcgonagall', 'll', 'wake', 'muggles', 'sorry', 'sobbed', 'hagrid', 'taking',
         'large', 'spotted', 'handkerchief', 'burying', 'hagrid', 'face', 'handkerchief', 'stand', 'handkerchief',
         'lily', 'james', 'dead', 'poor', 'little', 'harry', 'ter', 'muggles', 'handkerchief', 'sad', 'grip', 'hagrid',
         'll', 'professor', 'mcgonagall', 'whispered', 'patting', 'hagrid', 'gingerly', 'arm', 'dumbledore', 'stepped',
         'low', 'garden', 'wall', 'walked', 'front', 'door'],
        ['small', 'hand', 'closed', 'letter', 'beside', 'dumbledore', 'dumbledore', 'slept', 'knowing', 'dumbledore',
         'special', 'knowing', 'dumbledore', 'famous', 'knowing', 'dumbledore', 'woken', 'hours', 'dursley', 'scream',
         'dursley', 'opened', 'front', 'door', 'milk', 'bottles', 'dumbledore', 'spend', 'next', 'weeks', 'prodded',
         'pinched', 'dumbledore', 'cousin', 'dudley', 'dumbledore', 'couldn', 'moment', 'people', 'meeting', 'secret',
         'country', 'holding', 'people', 'glasses', 'saying', 'hushed', 'voices', 'harry', 'potter', 'lived'],
        ['tuft', 'jet', 'black', 'forehead', 'dumbledore', 'mcgonagall', 'curiously', 'shaped', 'cut', 'like', 'bolt',
         'lightning'], ['well', 'dumbledore', 'finally'],
        ['well', 'dumbledore', 'hagrid', 'better', 'dumbledore', 'took', 'harry', 'harry', 'arms', 'turned', 'toward',
         'dursley', 'dursley', 'dudley', 'dursley', 'house'],
        ['well', 'go', 'join', 'celebrations', 'hagrid', 'muffled', 'voice', 'll', 'takin', 'sirius', 'sirius', 'bike',
         'professor', 'mcgonagall', 'professor', 'dumbledore', 'sir', 'wiping', 'sirius', 'streaming', 'eyes', 'sirius',
         'jacket', 'sleeve', 'hagrid', 'swung', 'hagrid', 'onto', 'motorcycle', 'kicked', 'engine', 'roar', 'engine',
         'rose', 'air']], ('dumbledore', 'finally'): [['well', 'dumbledore', 'finally']],
                                               ('hagrid', 'muffled', 'voice'): [
                                                   ['well', 'go', 'join', 'celebrations', 'hagrid', 'muffled', 'voice',
                                                    'll', 'takin', 'sirius', 'sirius', 'bike', 'professor',
                                                    'mcgonagall', 'professor', 'dumbledore', 'sir', 'wiping', 'sirius',
                                                    'streaming', 'eyes', 'sirius', 'jacket', 'sleeve', 'hagrid',
                                                    'swung', 'hagrid', 'onto', 'motorcycle', 'kicked', 'engine', 'roar',
                                                    'engine', 'rose', 'air']], ('small', 'hand', 'closed'): [
            ['small', 'hand', 'closed', 'letter', 'beside', 'dumbledore', 'dumbledore', 'slept', 'knowing',
             'dumbledore', 'special', 'knowing', 'dumbledore', 'famous', 'knowing', 'dumbledore', 'woken', 'hours',
             'dursley', 'scream', 'dursley', 'opened', 'front', 'door', 'milk', 'bottles', 'dumbledore', 'spend',
             'next', 'weeks', 'prodded', 'pinched', 'dumbledore', 'cousin', 'dudley', 'dumbledore', 'couldn', 'moment',
             'people', 'meeting', 'secret', 'country', 'holding', 'people', 'glasses', 'saying', 'hushed', 'voices',
             'harry', 'potter', 'lived']], ('well', 'go', 'join', 'celebrations'): [
            ['well', 'go', 'join', 'celebrations', 'hagrid', 'muffled', 'voice', 'll', 'takin', 'sirius', 'sirius',
             'bike', 'professor', 'mcgonagall', 'professor', 'dumbledore', 'sir', 'wiping', 'sirius', 'streaming',
             'eyes', 'sirius', 'jacket', 'sleeve', 'hagrid', 'swung', 'hagrid', 'onto', 'motorcycle', 'kicked',
             'engine', 'roar', 'engine', 'rose', 'air']]}
    assert searchEngine4.result_KseqData() == {('another',): [], ('break',): [
        ['frog', 'allowed', 'remain', 'inside', 'break', 'due', 'downpour', 'outside']], ('harry', 'heard'): [],
                                               ('three', 'weeks'): [
                                                   ['realise', 're', 'three', 'weeks', 'away', 'match']],
                                               ('together',): [['ron', 'harry', 'together']]}


def test_buildDataBaseForGivenKeys():
    assert searchEngine1.buildDataBaseForGivenKeys() == {('breeze', 'ruffled'): [
        ['breeze', 'ruffled', 'neat', 'hedges', 'privet', 'drive', 'lay', 'silent', 'tidy', 'inky', 'sky', 'place',
         'expect', 'astonishing', 'things']], ('small', 'hand', 'closed'): [
        ['small', 'hand', 'closed', 'letter', 'beside', 'dumbledore', 'dumbledore', 'slept', 'knowing', 'dumbledore',
         'special', 'knowing', 'dumbledore', 'famous', 'knowing', 'dumbledore', 'woken', 'hours', 'dursley', 'scream',
         'dursley', 'opened', 'front', 'door', 'milk', 'bottles', 'dumbledore', 'spend', 'next', 'weeks', 'prodded',
         'pinched', 'dumbledore', 'cousin', 'dudley', 'dumbledore', 'couldn', 'moment', 'people', 'meeting', 'secret',
         'country', 'holding', 'people', 'glasses', 'saying', 'hushed', 'voices', 'harry', 'potter', 'lived']],
                                                         ('dumbledore', 'finally'): [['well', 'dumbledore', 'finally']],
                                                         ('dumbledore',): [
                                                             ['tuft', 'jet', 'black', 'forehead', 'dumbledore',
                                                              'mcgonagall', 'curiously', 'shaped', 'cut', 'like',
                                                              'bolt', 'lightning'],
                                                             ['dumbledore', 'dumbledore', 'll', 'scar', 'forever',
                                                              'couldn', 'something', 'scar', 'dumbledore', 'wouldn'],
                                                             ['well', 'dumbledore', 'hagrid', 'better', 'dumbledore',
                                                              'took', 'harry', 'harry', 'arms', 'turned', 'toward',
                                                              'dursley', 'dursley', 'dudley', 'dursley', 'house'],
                                                             ['shhh', 'hissed', 'professor', 'mcgonagall', 'll', 'wake',
                                                              'muggles', 'sorry', 'sobbed', 'hagrid', 'taking', 'large',
                                                              'spotted', 'handkerchief', 'burying', 'hagrid', 'face',
                                                              'handkerchief', 'stand', 'handkerchief', 'lily', 'james',
                                                              'dead', 'poor', 'little', 'harry', 'ter', 'muggles',
                                                              'handkerchief', 'sad', 'grip', 'hagrid', 'll',
                                                              'professor', 'mcgonagall', 'whispered', 'patting',
                                                              'hagrid', 'gingerly', 'arm', 'dumbledore', 'stepped',
                                                              'low', 'garden', 'wall', 'walked', 'front', 'door'],
                                                             ['dumbledore', 'laid', 'harry', 'gently', 'doorstep',
                                                              'took', 'letter', 'dumbledore', 'cloak', 'tucked',
                                                              'letter', 'inside', 'harry', 'blankets', 'came'],
                                                             ['full', 'minute', 'three', 'stood', 'looked', 'little',
                                                              'bundle', 'hagrid', 'shoulders', 'shook', 'professor',
                                                              'mcgonagall', 'blinked', 'furiously', 'twinkling',
                                                              'light', 'usually', 'shone', 'dumbledore', 'eyes',
                                                              'seemed'], ['well', 'dumbledore', 'finally'],
                                                             ['well', 'go', 'join', 'celebrations', 'hagrid', 'muffled',
                                                              'voice', 'll', 'takin', 'sirius', 'sirius', 'bike',
                                                              'professor', 'mcgonagall', 'professor', 'dumbledore',
                                                              'sir', 'wiping', 'sirius', 'streaming', 'eyes', 'sirius',
                                                              'jacket', 'sleeve', 'hagrid', 'swung', 'hagrid', 'onto',
                                                              'motorcycle', 'kicked', 'engine', 'roar', 'engine',
                                                              'rose', 'air'],
                                                             ['shall', 'expect', 'professor', 'mcgonagall',
                                                              'dumbledore', 'nodding', 'voice'],
                                                             ['dumbledore', 'turned', 'walked', 'street'],
                                                             ['corner', 'dumbledore', 'stopped', 'took', 'silver',
                                                              'outer'],
                                                             ['dumbledore', 'clicked', 'outer', 'twelve', 'balls',
                                                              'light', 'sped', 'balls', 'street', 'lamps', 'privet',
                                                              'drive', 'glowed', 'suddenly', 'orange', 'dumbledore',
                                                              'tabby', 'cat', 'slinking', 'corner', 'street'],
                                                             ['dumbledore', 'bundle', 'blankets', 'step', 'number',
                                                              'four'],
                                                             ['good', 'luck', 'harry', 'dumbledore', 'murmured'],
                                                             ['dumbledore', 'turned', 'dumbledore', 'heel', 'swish',
                                                              'dumbledore', 'cloak', 'dumbledore'],
                                                             ['harry', 'potter', 'rolled', 'inside', 'dumbledore',
                                                              'blankets', 'without', 'waking'],
                                                             ['small', 'hand', 'closed', 'letter', 'beside',
                                                              'dumbledore', 'dumbledore', 'slept', 'knowing',
                                                              'dumbledore', 'special', 'knowing', 'dumbledore',
                                                              'famous', 'knowing', 'dumbledore', 'woken', 'hours',
                                                              'dursley', 'scream', 'dursley', 'opened', 'front', 'door',
                                                              'milk', 'bottles', 'dumbledore', 'spend', 'next', 'weeks',
                                                              'prodded', 'pinched', 'dumbledore', 'cousin', 'dudley',
                                                              'dumbledore', 'couldn', 'moment', 'people', 'meeting',
                                                              'secret', 'country', 'holding', 'people', 'glasses',
                                                              'saying', 'hushed', 'voices', 'harry', 'potter',
                                                              'lived']], ('well', 'go', 'join', 'celebrations'): [
            ['well', 'go', 'join', 'celebrations', 'hagrid', 'muffled', 'voice', 'll', 'takin', 'sirius', 'sirius',
             'bike', 'professor', 'mcgonagall', 'professor', 'dumbledore', 'sir', 'wiping', 'sirius', 'streaming',
             'eyes', 'sirius', 'jacket', 'sleeve', 'hagrid', 'swung', 'hagrid', 'onto', 'motorcycle', 'kicked',
             'engine', 'roar', 'engine', 'rose', 'air']], ('hagrid', 'muffled', 'voice'): [
            ['well', 'go', 'join', 'celebrations', 'hagrid', 'muffled', 'voice', 'll', 'takin', 'sirius', 'sirius',
             'bike', 'professor', 'mcgonagall', 'professor', 'dumbledore', 'sir', 'wiping', 'sirius', 'streaming',
             'eyes', 'sirius', 'jacket', 'sleeve', 'hagrid', 'swung', 'hagrid', 'onto', 'motorcycle', 'kicked',
             'engine', 'roar', 'engine', 'rose', 'air']]}
    assert searchEngine2.buildDataBaseForGivenKeys() == {
        ('snape', 'looked'): [['karkaroff', 'looked', 'extremely', 'worried', 'snape', 'looked', 'angry']],
        ('harry', 'heard'): [['urgent', 'harry', 'heard', 'snape', 'hiss', 'karkaroff']],
        ('karkaroff',): [['karkaroff', 'looked', 'extremely', 'worried', 'snape', 'looked', 'angry'],
                         ['karkaroff', 'hovered', 'behind', 'snape', 'desk', 'rest', 'double', 'period'],
                         ['karkaroff', 'seemed', 'intent', 'preventing', 'snape', 'slipping', 'away', 'class'],
                         ['keen', 'karkaroff', 'wanted', 'harry', 'deliberately', 'knocked', 'harry', 'bottle',
                          'armadillo', 'bile', 'minutes', 'go', 'bell', 'gave', 'harry', 'excuse', 'duck', 'behind',
                          'harry', 'cauldron', 'mop', 'rest', 'class', 'moved', 'noisily', 'toward', 'door'],
                         ['urgent', 'harry', 'heard', 'snape', 'hiss', 'karkaroff'],
                         ['karkaroff', 'harry', 'peering', 'edge', 'harry', 'cauldron', 'karkaroff', 'pull', 'left',
                          'hand', 'sleeve', 'harry', 'robe', 'snape', 'something', 'harry', 'inner', 'forearm'],
                         ['well', 'karkaroff', 'making', 'every', 'effort', 'harry', 'lips']],
        ('well', 'go', 'join', 'celebrations'): [],
        ('lips',): [['well', 'karkaroff', 'making', 'every', 'effort', 'harry', 'lips']]}
    assert searchEngine3.buildDataBaseForGivenKeys() == {('another',): [['given', 'another', 'detention']],
                                                         ('harry', 'heard'): [
                                                             ['harry', 'heard', 'footsteps', 'door', 'opened', 'harry',
                                                              'harry', 'face', 'face', 'professor', 'mcgonagall']],
                                                         ('well', 'go', 'join', 'celebrations'): [],
                                                         ('knocked',): [['harry', 'knocked']]}
    assert searchEngine4.buildDataBaseForGivenKeys() == {('another',): [], ('harry', 'heard'): [], ('break',): [
        ['frog', 'allowed', 'remain', 'inside', 'break', 'due', 'downpour', 'outside']],
                                                         ('together',): [['ron', 'harry', 'together']],
                                                         ('three', 'weeks'): [
                                                             ['realise', 're', 'three', 'weeks', 'away', 'match']]}
    assert searchEngine5.buildDataBaseForGivenKeys() == {('breeze', 'ruffled'): [
        ['breeze', 'ruffled', 'neat', 'hedges', 'privet', 'drive', 'lay', 'silent', 'tidy', 'inky', 'sky', 'place',
         'expect', 'astonishing', 'things']], ('small', 'hand', 'closed'): [
        ['small', 'hand', 'closed', 'letter', 'beside', 'dumbledore', 'dumbledore', 'slept', 'knowing', 'dumbledore',
         'special', 'knowing', 'dumbledore', 'famous', 'knowing', 'dumbledore', 'woken', 'hours', 'dursley', 'scream',
         'dursley', 'opened', 'front', 'door', 'milk', 'bottles', 'dumbledore', 'spend', 'next', 'weeks', 'prodded',
         'pinched', 'dumbledore', 'cousin', 'dudley', 'dumbledore', 'couldn', 'moment', 'people', 'meeting', 'secret',
         'country', 'holding', 'people', 'glasses', 'saying', 'hushed', 'voices', 'harry', 'potter', 'lived']],
                                                         ('dumbledore', 'finally'): [['well', 'dumbledore', 'finally']],
                                                         ('dumbledore',): [
                                                             ['tuft', 'jet', 'black', 'forehead', 'dumbledore',
                                                              'mcgonagall', 'curiously', 'shaped', 'cut', 'like',
                                                              'bolt', 'lightning'],
                                                             ['dumbledore', 'dumbledore', 'll', 'scar', 'forever',
                                                              'couldn', 'something', 'scar', 'dumbledore', 'wouldn'],
                                                             ['well', 'dumbledore', 'hagrid', 'better', 'dumbledore',
                                                              'took', 'harry', 'harry', 'arms', 'turned', 'toward',
                                                              'dursley', 'dursley', 'dudley', 'dursley', 'house'],
                                                             ['shhh', 'hissed', 'professor', 'mcgonagall', 'll', 'wake',
                                                              'muggles', 'sorry', 'sobbed', 'hagrid', 'taking', 'large',
                                                              'spotted', 'handkerchief', 'burying', 'hagrid', 'face',
                                                              'handkerchief', 'stand', 'handkerchief', 'lily', 'james',
                                                              'dead', 'poor', 'little', 'harry', 'ter', 'muggles',
                                                              'handkerchief', 'sad', 'grip', 'hagrid', 'll',
                                                              'professor', 'mcgonagall', 'whispered', 'patting',
                                                              'hagrid', 'gingerly', 'arm', 'dumbledore', 'stepped',
                                                              'low', 'garden', 'wall', 'walked', 'front', 'door'],
                                                             ['dumbledore', 'laid', 'harry', 'gently', 'doorstep',
                                                              'took', 'letter', 'dumbledore', 'cloak', 'tucked',
                                                              'letter', 'inside', 'harry', 'blankets', 'came'],
                                                             ['full', 'minute', 'three', 'stood', 'looked', 'little',
                                                              'bundle', 'hagrid', 'shoulders', 'shook', 'professor',
                                                              'mcgonagall', 'blinked', 'furiously', 'twinkling',
                                                              'light', 'usually', 'shone', 'dumbledore', 'eyes',
                                                              'seemed'], ['well', 'dumbledore', 'finally'],
                                                             ['well', 'go', 'join', 'celebrations', 'hagrid', 'muffled',
                                                              'voice', 'll', 'takin', 'sirius', 'sirius', 'bike',
                                                              'professor', 'mcgonagall', 'professor', 'dumbledore',
                                                              'sir', 'wiping', 'sirius', 'streaming', 'eyes', 'sirius',
                                                              'jacket', 'sleeve', 'hagrid', 'swung', 'hagrid', 'onto',
                                                              'motorcycle', 'kicked', 'engine', 'roar', 'engine',
                                                              'rose', 'air'],
                                                             ['shall', 'expect', 'professor', 'mcgonagall',
                                                              'dumbledore', 'nodding', 'voice'],
                                                             ['dumbledore', 'turned', 'walked', 'street'],
                                                             ['corner', 'dumbledore', 'stopped', 'took', 'silver',
                                                              'outer'],
                                                             ['dumbledore', 'clicked', 'outer', 'twelve', 'balls',
                                                              'light', 'sped', 'balls', 'street', 'lamps', 'privet',
                                                              'drive', 'glowed', 'suddenly', 'orange', 'dumbledore',
                                                              'tabby', 'cat', 'slinking', 'corner', 'street'],
                                                             ['dumbledore', 'bundle', 'blankets', 'step', 'number',
                                                              'four'],
                                                             ['good', 'luck', 'harry', 'dumbledore', 'murmured'],
                                                             ['dumbledore', 'turned', 'dumbledore', 'heel', 'swish',
                                                              'dumbledore', 'cloak', 'dumbledore'],
                                                             ['harry', 'potter', 'rolled', 'inside', 'dumbledore',
                                                              'blankets', 'without', 'waking'],
                                                             ['small', 'hand', 'closed', 'letter', 'beside',
                                                              'dumbledore', 'dumbledore', 'slept', 'knowing',
                                                              'dumbledore', 'special', 'knowing', 'dumbledore',
                                                              'famous', 'knowing', 'dumbledore', 'woken', 'hours',
                                                              'dursley', 'scream', 'dursley', 'opened', 'front', 'door',
                                                              'milk', 'bottles', 'dumbledore', 'spend', 'next', 'weeks',
                                                              'prodded', 'pinched', 'dumbledore', 'cousin', 'dudley',
                                                              'dumbledore', 'couldn', 'moment', 'people', 'meeting',
                                                              'secret', 'country', 'holding', 'people', 'glasses',
                                                              'saying', 'hushed', 'voices', 'harry', 'potter',
                                                              'lived']], ('well', 'go', 'join', 'celebrations'): [
            ['well', 'go', 'join', 'celebrations', 'hagrid', 'muffled', 'voice', 'll', 'takin', 'sirius', 'sirius',
             'bike', 'professor', 'mcgonagall', 'professor', 'dumbledore', 'sir', 'wiping', 'sirius', 'streaming',
             'eyes', 'sirius', 'jacket', 'sleeve', 'hagrid', 'swung', 'hagrid', 'onto', 'motorcycle', 'kicked',
             'engine', 'roar', 'engine', 'rose', 'air']], ('hagrid', 'muffled', 'voice'): [
            ['well', 'go', 'join', 'celebrations', 'hagrid', 'muffled', 'voice', 'll', 'takin', 'sirius', 'sirius',
             'bike', 'professor', 'mcgonagall', 'professor', 'dumbledore', 'sir', 'wiping', 'sirius', 'streaming',
             'eyes', 'sirius', 'jacket', 'sleeve', 'hagrid', 'swung', 'hagrid', 'onto', 'motorcycle', 'kicked',
             'engine', 'roar', 'engine', 'rose', 'air']]}
    assert searchEngine6.buildDataBaseForGivenKeys() == {
        ('snape', 'looked'): [['karkaroff', 'looked', 'extremely', 'worried', 'snape', 'looked', 'angry']],
        ('harry', 'heard'): [['urgent', 'harry', 'heard', 'snape', 'hiss', 'karkaroff']],
        ('karkaroff',): [['karkaroff', 'looked', 'extremely', 'worried', 'snape', 'looked', 'angry'],
                         ['karkaroff', 'hovered', 'behind', 'snape', 'desk', 'rest', 'double', 'period'],
                         ['karkaroff', 'seemed', 'intent', 'preventing', 'snape', 'slipping', 'away', 'class'],
                         ['keen', 'karkaroff', 'wanted', 'harry', 'deliberately', 'knocked', 'harry', 'bottle',
                          'armadillo', 'bile', 'minutes', 'go', 'bell', 'gave', 'harry', 'excuse', 'duck', 'behind',
                          'harry', 'cauldron', 'mop', 'rest', 'class', 'moved', 'noisily', 'toward', 'door'],
                         ['urgent', 'harry', 'heard', 'snape', 'hiss', 'karkaroff'],
                         ['karkaroff', 'harry', 'peering', 'edge', 'harry', 'cauldron', 'karkaroff', 'pull', 'left',
                          'hand', 'sleeve', 'harry', 'robe', 'snape', 'something', 'harry', 'inner', 'forearm'],
                         ['well', 'karkaroff', 'making', 'every', 'effort', 'harry', 'lips']],
        ('well', 'go', 'join', 'celebrations'): [],
        ('lips',): [['well', 'karkaroff', 'making', 'every', 'effort', 'harry', 'lips']]}
    assert searchEngine7.buildDataBaseForGivenKeys() == {('another',): [['given', 'another', 'detention']],
                                                         ('harry', 'heard'): [
                                                             ['harry', 'heard', 'footsteps', 'door', 'opened', 'harry',
                                                              'harry', 'face', 'face', 'professor', 'mcgonagall']],
                                                         ('well', 'go', 'join', 'celebrations'): [],
                                                         ('knocked',): [['harry', 'knocked']]}

def test_load_kseq_data():
    assert searchEngine1.load_kseq_data() == [['breeze', 'ruffled'], ['small', 'hand', 'closed'], ['dumbledore', 'finally'], ['dumbledore'], ['well', 'go', 'join', 'celebrations'], ['hagrid', 'muffled', 'voice']]
    assert searchEngine5.load_kseq_data() == [['breeze', 'ruffled'], ['small', 'hand', 'closed'], ['dumbledore', 'finally'], ['dumbledore'], ['well', 'go', 'join', 'celebrations'], ['hagrid', 'muffled', 'voice']]
    assert searchEngine2.load_kseq_data() == [['snape', 'looked'], ['harry', 'heard'], ['karkaroff'], ['well', 'go', 'join', 'celebrations'], ['lips']]
    assert searchEngine6.load_kseq_data() == [['snape', 'looked'], ['harry', 'heard'], ['karkaroff'], ['well', 'go', 'join', 'celebrations'], ['lips']]
    assert searchEngine3.load_kseq_data() ==[['another'], ['harry', 'heard'], ['another'], ['well', 'go', 'join', 'celebrations'], ['knocked']]
    assert searchEngine7.load_kseq_data() == [['another'], ['harry', 'heard'], ['another'], ['well', 'go', 'join', 'celebrations'], ['knocked']]
    assert searchEngine4.load_kseq_data() == [['another'], ['harry', 'heard'], ['break'], ['together'], ['three', 'weeks']]

def test_write_to_json():
    searchEngine1.write_to_json("text_analyzer/2_examples/Q4_examples/q4_example1.json")
    searchEngine2.write_to_json("text_analyzer/2_examples/Q4_examples/q4_example2.json")
    searchEngine3.write_to_json("text_analyzer/2_examples/Q4_examples/q4_example3.json")
    searchEngine4.write_to_json("text_analyzer/2_examples/Q4_examples/q4_example4.json")
    searchEngine5.write_to_json("text_analyzer/2_examples/Q4_examples/q4_example5.json")
    searchEngine6.write_to_json("text_analyzer/2_examples/Q4_examples/q4_example6.json")
    searchEngine7.write_to_json("text_analyzer/2_examples/Q4_examples/q4_example7.json")

    def load_json(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
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

        assert compare_files("text_analyzer/2_examples/Q4_examples/q4_example1.json", "text_analyzer/2_examples/Q4_examples/example_1/Q4_result1.json")
        assert compare_files("text_analyzer/2_examples/Q4_examples/q4_example2.json", "text_analyzer/2_examples/Q4_examples/example_2/Q4_result2.json")
        assert compare_files("text_analyzer/2_examples/Q4_examples/q4_example3.json", "text_analyzer/2_examples/Q4_examples/example_3/Q4_result3.json")
        assert compare_files("text_analyzer/2_examples/Q4_examples/q4_example4.json", "text_analyzer/2_examples/Q4_examples/example_4/Q4_result4.json")
        assert compare_files("text_analyzer/2_examples/Q4_examples/q4_example5.json", "text_analyzer/2_examples/Q4_examples/example_1/Q4_result1.json")
        assert compare_files("text_analyzer/2_examples/Q4_examples/q4_example6.json", "text_analyzer/2_examples/Q4_examples/example_2/Q4_result2.json")
        assert compare_files("text_analyzer/2_examples/Q4_examples/q4_example7.json", "text_analyzer/2_examples/Q4_examples/example_3/Q4_result3.json")
