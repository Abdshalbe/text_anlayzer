import pytest
from PeopleConnectionGraph import *
from test_PeopleKAssocions import *


class TestGraph:
    def test_node_creation(self):
        # Test node initialization with a string
        node1 = Node("node1")
        assert node1.get_data() == "node1"
        assert len(node1.get_connected_data()) == 0  # No connections initially
        # Test node initialization with a list
        node2 = Node(["node", "two"])
        assert node2.get_data() == ["node", "two"]
        assert len(node2.get_connected_data()) == 0  # No connections initially

    def test_add_connected_data(self):
        # Create nodes
        node1 = Node("node1")
        node2 = Node("node2")
        # Add a connection between node1 and node2
        node1.add_connected_data(node2)
        # Assert that node1 has node2 in its connected data
        assert node2 in node1.get_connected_data()

    def test_graph_creation(self):
        # Create the Graph
        graph = Graph()

        # Add nodes to the graph
        graph.add_node("node1")
        graph.add_node("node2")
        graph.add_node("node3")

        # Assert nodes exist in the graph
        assert graph.get_node("node1") is not None
        assert graph.get_node("node2") is not None
        assert graph.get_node("node3") is not None

        # Assert that a non-existent node returns None
        assert graph.get_node("non_existing_node") is None

    def test_add_edge(self):
        # Create the Graph
        graph = Graph()

        # Add nodes to the graph
        graph.add_node("node1")
        graph.add_node("node2")

        # Add an edge between node1 and node2
        graph.add_edge("node1", "node2")

        # Assert that the edge exists
        assert len(graph.get_edges()) == 1
        edge = graph.get_edges()[0]
        assert edge[0].get_data() == "node1"
        assert edge[1].get_data() == "node2"

        # Add another edge and check that it is sorted correctly
        graph.add_node("node3")
        graph.add_edge("node1", "node3")
        graph.add_edge("node2", "node3")

        # Assert the edges are sorted correctly
        assert graph.get_edges()[0][0].get_data() == "node1"
        assert graph.get_edges()[1][0].get_data() == "node1"
        assert graph.get_edges()[2][0].get_data() == "node2"

    def test_node_str_repr(self):
        # Test __str__ and __repr__ methods for Node
        node1 = Node("node1")
        assert str(node1) == "node1"
        assert repr(node1) == "node1"

    def test_graph_repr(self):
        # Create Graph and add some nodes and edges
        graph = Graph()
        graph.add_node("node1")
        graph.add_node("node2")
        graph.add_edge("node1", "node2")

        # Check the string representation of the graph
        assert repr(graph) == "{'node1': node1, 'node2': node2}"

    def test_edge_uniqueness(self):
        # Create Graph and add nodes and edges
        graph = Graph()
        graph.add_node("node1")
        graph.add_node("node2")
        graph.add_node("node3")

        # Add the same edge multiple times
        graph.add_edge("node1", "node2")
        graph.add_edge("node2", "node1")  # Duplicate edge

        # Assert that the edge is added only once
        assert len(graph.get_edges()) == 1
        edge = graph.get_edges()[0]
        assert edge[0].get_data() == "node1"
        assert edge[1].get_data() == "node2"

    def test_edge_ordering(self):
        # Create Graph and add nodes and edges
        graph = Graph()
        graph.add_node("node1")
        graph.add_node("node2")
        graph.add_node("node3")

        # Add edges with the same nodes in different order
        graph.add_edge("node1", "node2")
        graph.add_edge("node2", "node3")

        # Ensure that edges are sorted by the first node's data
        edges = graph.get_edges()
        assert edges[0][0].get_data() == "node1"
        assert edges[1][0].get_data() == "node2"

    def test_no_connection_for_unconnected_node(self):
        # Create nodes but do not connect them
        node1 = Node("node1")
        node2 = Node("node2")

        # Assert that node1 is not connected to node2
        assert node2 not in node1.get_connected_data()


data_text = [[
    '"Under a tuft of jet- black hair over boy forehead Dumbledore and  McGonagall could see a curiously shaped cut, like a bolt of lightning."']
    , ['` Is that where-?` whispered Professor  McGonagall.'],
    [
        "` Yes,` said  Dumbledore.`  Dumbledore'll have that scar forever.` ` Couldn't you do something about scar,  Dumbledore?` ` Even if I could, I wouldn't."],
    ['Scars can come in handy.'],
    ['I have one myself above my left knee that is a perfect map of the London Underground.'],
    [
        ''"Well-- give  Dumbledore here,  Hagrid-- we'd better get this over with.`   Dumbledore took  Harry in  Harry arms and turned toward the   Mr. Dursley and   Mrs. Dursley and    Dudley Dursley' house."''],
    ['"` Could I-- could I say good- bye to  Harry, sir?` asked  Hagrid."'],
    [
        '"Harry bent  Harry great, shaggy head over  Harry and gave head what must have been a very scratchy, whiskery kiss."'],
    ['"Then, suddenly,  Hagrid let out a howl like a wounded dog."'],
    [
        '''"` Shhh!` hissed Professor  McGonagall,` you'll wake the  Muggles!` ` S- s- sorry,` sobbed  Hagrid, taking out a large, spotted handkerchief and burying  Hagrid face in handkerchief.` But I c- c-can't stand handkerchief--  Lily an'  James dead-- an' poor little  Harry off ter live with  Muggles-` ` Yes, yes, handkerchief's all very sad, but get a grip on yourself,  Hagrid, or we'll be found,` Professor  McGonagall whispered, patting  Hagrid gingerly on the arm as  Dumbledore stepped over the low garden wall and walked to the front door."'''],
    [
        "Dumbledore laid  Harry gently on the doorstep, took a letter out of  Dumbledore cloak, tucked letter inside  Harry's blankets, and then came back to the other two."],
    [
        "For a full minute the three of two stood and looked at the little bundle;   Hagrid's shoulders shook, Professor  McGonagall blinked furiously, and the twinkling light that usually shone from  Dumbledore's eyes seemed to have gone out."],
    ["` Well,` said  Dumbledore finally,` that's that."],
    ['''We've no business staying here.'''],
    [
        "We may as well go and join the celebrations.` ` Yeah,` said  Hagrid in a very muffled voice,` I'll be takin'  Sirius  Sirius bike back.G'night, Professor  McGonagall-- Professor  Dumbledore, sir.`  Wiping  Sirius streaming eyes on  Sirius jacket sleeve,  Hagrid swung  Hagrid onto the motorcycle and kicked the engine into life; with a roar engine rose into the air and off into the night."],
    ["` I shall see you soon, I expect, Professor  McGonagall,` said  Dumbledore, nodding to voice."],
    ['Professor  McGonagall blew  McGonagall nose in reply.'],
    ['Dumbledore turned and walked back down the street.'],
    ['On the corner  Dumbledore stopped and took out the silver Put- Outer.'],
    [
        '"Dumbledore clicked Outer once, and twelve balls of light sped back to balls street lamps so that Privet Drive glowed suddenly orange and  Dumbledore could make out a tabby cat slinking around the corner at the other end of the street."']
    , ['"Dumbledore could just see the bundle of blankets on the step of number four."'],
    ["` Good luck,  Harry,`  Dumbledore murmured."],
    ["Dumbledore turned on  Dumbledore heel and with a swish of  Dumbledore cloak,  Dumbledore was gone."],
    [
        "A breeze ruffled the neat hedges of Privet Drive, which lay silent and tidy under the inky sky, the very last place you would expect astonishing things to happen."],
    ['Harry  Potter rolled over inside  Dumbledore blankets without waking up.'],
    [
        "One small hand closed on the letter beside  Dumbledore and  Dumbledore slept on, not knowing  Dumbledore was special, not knowing  Dumbledore was famous, not knowing  Dumbledore would be woken in a few hours' time by   Mrs. Dursley's scream as   Mrs. Dursley opened the front door to put out the milk bottles, nor that  Dumbledore would spend the next few weeks being prodded and pinched by  Dumbledore cousin   Dudley...  Dumbledore couldn't know that at this very moment, people meeting in secret all over the country were holding up people glasses and saying in hushed voices:` To   Harry  Potter-- the boy who lived!"],
    [
        "THE VANISHING GLASS  Nearly ten years had passed since the   Mr. Dursley and   Mrs. Dursley and    Dudley Dursley had woken up to find   Mr. Dursley and   Mrs. Dursley and    Dudley Dursley nephew on the front step, but Privet Drive had hardly changed at all."],
    [
        "The sun rose on the same tidy front gardens and lit up the brass number four on the   Mr. Dursley and   Mrs. Dursley and    Dudley Dursley' front door; number crept into   Mr. Dursley and   Mrs. Dursley and    Dudley Dursley living room, which was almost exactly the same as it had been on the night when   Mr. Dursley had seen that fateful news report about the owls."],
    ['Only the photographs on the mantelpiece really showed how much time had passed.'],
    [
        "Ten years ago, there had been lots of pictures of what looked like a large pink beach ball wearing different- colored bonnets-- but    Dudley Dursley was no longer a baby, and now the photographs showed a large blond boy riding boy first bicycle, on a carousel at the fair, playing a computer game with boy father, being hugged and kissed by boy mother."],
    ["The room held no sign at all that another boy lived in the house, too."]]
names1 = [['Over-Attentive Wizard', ''], ['Bertram Aubrey', ''],
          ['Audrey Weasley', ''], ['"Augusta ""Gran"" Longbottom"', ''], ['Augustus Pye', ''],
          ['Augustus Rookwood', ''], ['Augustus Worme', ''],
          ['Auntie Muriel', '']
    , ['Aunt Marge Dursley', '']
    , ['Aurelius Dumbledore', '']
    , ['Aurora Sinistra', '']
    , ['Avery', '']
    , ['Babajide Akingbade', '']
    , ['Babayaga', '']
    , ['Babbitty Rabbitty', '']
    , ['Bagman Sr.', '']
    , ['Ludo Bagman', '']
    , ['Otto Bagman', '']
    , ['Millicent Bagnold', '']
    , ['Bathilda Bagshot', 'Batty']
    , ['Kquewanda Bailey', '']
    , ['Ballyfumble Stranger', '"Quin, Quivering Quintus, Quintus-Of-The-Silly-Name"']
    , ['Harry Potter',
       '"The boy who lived, Undesirable Number One, the Chosen One, Parry Otter, the Chosen Boy, the Mudbloods friend"']
    , ['Aberforth Dumbledore', '']]
names2 = [['Ballyfumble Stranger', '"Quin, Quivering Quintus, Quintus-Of-The-Silly-Name"']
    , ['Harry Potter',
       '"The boy who lived, Undesirable Number One, the Chosen One, Parry Otter, the Chosen Boy, the Mudbloods friend"']
    , ['Aberforth Dumbledore', '']]
data_text2 = [['Dumbledore has been born in the same day Quin born'], ['they born on January 16th'],
              ['Quivering Quintus marred Dumbledore after 20 years']]
words_to_remove = [
    ['a'], ['about'], ['above'], ['actual'], ['after'], ['again'], ['against'], ['all'], ['alreadi'], ['also'],
    ['alway'], ['am'], ['amp'], ['an'], ['and'], ['ani'], ['anoth'], ['any'], ['anyth'], ['are'], ['around'],
    ['as'], ['at'], ['aww'], ['babi'], ['back'], ['be'], ['becaus'], ['because'], ['bed'], ['been'], ['befor'],
    ['before'], ['being'], ['below'], ['between'], ['birthday'], ['bit'], ['book'], ['both'], ['boy'], ['but'],
    ['by'], ['call'], ['can'], ['cannot'], ['cant'], ['car'], ['check'], ['com'], ['come'], ['could'], ['day'],
    ['did'], ['didn'], ['dinner'], ['do'], ['doe'], ['does'], ['doesn'], ['doing'], ['don'], ['done'], ['dont'],
    ['down'], ['during'], ['each'], ['eat'], ['end'], ['even'], ['ever'], ['everyon'], ['exam'], ['famili'],
    ['feel'], ['few'], ['final'], ['find'], ['first'], ['follow'], ['for'], ['found'], ['friday'], ['from'],
    ['further'], ['game'], ['get'], ['girl'], ['give'], ['gone'], ['gonna'], ['got'], ['gotta'], ['guess'],
    ['guy'], ['had'], ['hair'], ['happen'], ['has'], ['have'], ['haven'], ['having'], ['he'], ['head'], ['hear'],
    ['her'], ['here'], ['hers'], ['herself'], ['hey'], ['him'], ['himself'], ['his'], ['home'], ['hour'], ['hous'],
    ['how'], ['http'], ['i'], ['if'], ['im'], ['in'], ['into'], ['is'], ['isn'], ['it'], ['its'], ['itself'], ['job'],
    ['just'], ['keep'], ['know'], ['last'], ['later'], ['least'], ['leav'], ['let'], ['life'], ['listen'], ['littl'],
    ['live'], ['look'], ['lot'], ['lunch'], ['made'], ['make'], ['man'], ['mani'], ['may'], ['mayb'], ['me'], ['mean'],
    ['meet'], ['might'], ['mom'], ['monday'], ['month'], ['more'], ['morn'], ['most'], ['move'], ['movi'], ['much'],
    ['must'], ['my'], ['myself'], ['need'], ['never'], ['new'], ['night'], ['no'], ['nor'], ['not'], ['noth'], ['now'],
    ['of'], ['off'], ['on'], ['once'], ['one'], ['onli'], ['only'], ['or'], ['other'], ['ought'], ['our'], ['ours'],
    ['ourselves'], ['out'], ['over'], ['own'], ['peopl'], ['phone'], ['pic'], ['pictur'], ['play'], ['post'], ['put'],
    ['quot'], ['rain'], ['read'], ['readi'], ['realli'], ['run'], ['said'], ['same'], ['saw'], ['say'], ['school'],
    ['see'], ['seem'], ['she'], ['shop'], ['should'], ['show'], ['sinc'], ['sleep'], ['so'], ['some'], ['someon'],
    ['someth'], ['song'], ['soon'], ['sound'], ['start'], ['stay'], ['still'], ['studi'], ['stuff'], ['such'],
    ['summer'], ['sunday'], ['sure'], ['take'], ['talk'], ['tell'], ['than'], ['thank'], ['that'], ['the'], ['their'],
    ['theirs'], ['them'], ['themselves'], ['then'], ['there'], ['these'], ['they'], ['thing'], ['think'], ['this'],
    ['those'], ['though'], ['thought'], ['through'], ['time'], ['to'], ['today'], ['tomorrow'], ['tonight'], ['too'],
    ['total'], ['tri'], ['tweet'], ['twitpic'], ['twitter'], ['two'], ['u'], ['under'], ['until'], ['up'], ['updat'],
    ['use'], ['veri'], ['very'], ['video'], ['wait'], ['wanna'], ['want'], ['was'], ['watch'], ['way'], ['we'],
    ['weather'], ['week'], ['weekend'], ['went'], ['were'], ['what'], ['when'], ['where'], ['whi'], ['which'],
    ['while'], ['who'], ['whom'], ['why'], ['will'], ['with'], ['woke'], ['won'], ['work'], ['world'], ['would'],
    ['www'], ['yay'], ['yeah'], ['year'], ['yes'], ['yesterday'], ['yet'], ['you'], ['your'], ['yours'], ['yourself'],
    ['yourselves'], ['a'], ['b'], ['c'], ['d'], ['e'], ['f'], ['g'], ['h'], ['i'], ['j'], ['k'], ['l'], ['m'], ['n'],
    ['o'], ['p'], ['k'], ['r'], ['s'], ['t'], ['u'], ['v'], ['w'], ['x'], ['u'], ['z'], ['mr'], ['miss'], ['mrs'],
    ['ms']
]

people_names1_file = create_temp_csv(names_list1, ["Name", "Other Names"])
people_names2_file = create_temp_csv(names_list2, ["Name", "Other Names"])
people_names3_file = create_temp_csv(names_list3, ["Name", "Other Names"])
csv_sentence1 = create_temp_csv(text1, ["sentence"])
csv_sentence2 = create_temp_csv(text2, ["sentence"])
csv_sentence3 = create_temp_csv(text3, ["sentence"])
csv_remved = create_temp_csv(remvoe_words, ["words"])

dataSentence1 = create_temp_csv_with_data(data_text, ['sentence'])
data_names_csv = create_temp_csv_with_data(names1, ['Name', 'Other Names'])
dataSentence2 = create_temp_csv_with_data(data_text2, ['sentence'])
data_names_csv2 = create_temp_csv_with_data(names2, ['Name', 'Other Names'])
datawords = create_temp_csv_with_data(words_to_remove, ['words'])
parsered_json = process_json_data(Parser(1, dataSentence1, datawords, data_names_csv).return_results())

graph1 = PeopleConnectionGraph(6, jsonInputFile=parsered_json, preprocessed=True, WindowSize=2, Threshold=2)
graph2 = PeopleConnectionGraph(6, sentence_input_path=dataSentence1, people_input_path=data_names_csv,
                               remove_input_path=datawords, Threshold=2, WindowSize=2)
graph3 = PeopleConnectionGraph(6, jsonInputFile=parsered_json, preprocessed=True, WindowSize=7, Threshold=3)
graph4 = PeopleConnectionGraph(6, sentence_input_path=dataSentence1, people_input_path=data_names_csv,
                               remove_input_path=datawords, Threshold=3, WindowSize=7)
graph5 = PeopleConnectionGraph(6, jsonInputFile=parsered_json, preprocessed=True, WindowSize=1, Threshold=5)
graph6 = PeopleConnectionGraph(6, sentence_input_path=dataSentence1, people_input_path=data_names_csv,
                               remove_input_path=datawords, Threshold=5, WindowSize=1)
graph7 = PeopleConnectionGraph(6, jsonInputFile=parsered_json, preprocessed=True, WindowSize=31, Threshold=2)
graph8 = PeopleConnectionGraph(6, sentence_input_path=dataSentence1, people_input_path=data_names_csv,
                               remove_input_path=datawords, Threshold=2, WindowSize=31)
graph9 = PeopleConnectionGraph(6, sentence_input_path=csv_sentence1, people_input_path=people_names1_file,
                               remove_input_path=datawords, Threshold=3, WindowSize=3)
graph10 = PeopleConnectionGraph(6, sentence_input_path=csv_sentence2, people_input_path=people_names1_file,
                                remove_input_path=datawords, Threshold=4, WindowSize=7)
graph11 = PeopleConnectionGraph(6, sentence_input_path=csv_sentence3, people_input_path=people_names1_file,
                                remove_input_path=datawords, Threshold=1, WindowSize=1)
graph12 = PeopleConnectionGraph(6, sentence_input_path=csv_sentence1, people_input_path=people_names2_file,
                                remove_input_path=datawords, Threshold=2, WindowSize=2)
graph13 = PeopleConnectionGraph(6, sentence_input_path=csv_sentence2, people_input_path=people_names2_file,
                                remove_input_path=datawords, Threshold=7, WindowSize=2)
graph14 = PeopleConnectionGraph(6, sentence_input_path=csv_sentence3, people_input_path=people_names2_file,
                                remove_input_path=datawords, Threshold=1, WindowSize=3)
graph15 = PeopleConnectionGraph(6, sentence_input_path=csv_sentence1, people_input_path=people_names3_file,
                                remove_input_path=datawords, Threshold=1, WindowSize=4)
graph16 = PeopleConnectionGraph(6, sentence_input_path=csv_sentence2, people_input_path=people_names3_file,
                                remove_input_path=datawords, Threshold=3, WindowSize=2)
graph17 = PeopleConnectionGraph(6, sentence_input_path=csv_sentence3, people_input_path=people_names3_file,
                                remove_input_path=datawords, Threshold=1, WindowSize=1)
graph18 = PeopleConnectionGraph(6, sentence_input_path=csv_sentence3, people_input_path=people_names2_file,
                                remove_input_path=datawords, Threshold=2, WindowSize=2)
graph19 = PeopleConnectionGraph(6, sentence_input_path=dataSentence2, people_input_path=data_names_csv2,
                                remove_input_path=datawords, Threshold=2, WindowSize=2)


def test_equal_csr():
    """
    Test that two CSRs are equal to each other if the data is equal
    """
    assert graph2.return_results() != graph5.return_results()
    assert graph8.return_results() != graph6.return_results()
    assert graph3.return_results() != graph7.return_results()
    assert graph1.return_results() == graph2.return_results()
    assert graph3.return_results() == graph4.return_results()
    assert graph5.return_results() == graph6.return_results()
    assert graph7.return_results() == graph8.return_results()


def test_build_graph():
    """
    Test that two graphs with empty inputs return empty graph
    """
    empty_graph = Graph()
    assert graph17.get_graph() == empty_graph
    assert graph16.get_graph() == empty_graph
    assert graph15.get_graph() == empty_graph
    assert graph13.get_graph() == empty_graph
    assert graph11.get_graph() == empty_graph
    assert graph10.get_graph() == empty_graph


def test_result():
    """
    Test that the result of the graph is correct and sorted as should
    IN THIS TEst i tested many cases "people counted once for every window" and
    other cases like empty file and sorted result
    I TESTED : No Person Pairs in the Same Window: If no pair of people appears together in any window, the result should be empty.
    Small Threshold (t = 1): This will result in many edges, so it should be tested with edge cases for performance.
    No People Mentioned: If none of the people from the list appear in any sentences, the graph should have no edges.
    Duplicate Edges: Ensure that the graph does not contain duplicate edges between the same pair of people.
    """
    res1 = ('{\n'
            '    "Question 6": {\n'
            '        "Pair Matches": [\n'
            '            [\n'
            '                [\n'
            '                    "aberforth",\n'
            '                    "dumbledore"\n'
            '                ],\n'
            '                [\n'
            '                    "aunt",\n'
            '                    "marge",\n'
            '                    "dursley"\n'
            '                ]\n'
            '            ],\n'
            '            [\n'
            '                [\n'
            '                    "aberforth",\n'
            '                    "dumbledore"\n'
            '                ],\n'
            '                [\n'
            '                    "aurelius",\n'
            '                    "dumbledore"\n'
            '                ]\n'
            '            ],\n'
            '            [\n'
            '                [\n'
            '                    "aberforth",\n'
            '                    "dumbledore"\n'
            '                ],\n'
            '                [\n'
            '                    "harry",\n'
            '                    "potter"\n'
            '                ]\n'
            '            ],\n'
            '            [\n'
            '                [\n'
            '                    "aunt",\n'
            '                    "marge",\n'
            '                    "dursley"\n'
            '                ],\n'
            '                [\n'
            '                    "aurelius",\n'
            '                    "dumbledore"\n'
            '                ]\n'
            '            ],\n'
            '            [\n'
            '                [\n'
            '                    "aunt",\n'
            '                    "marge",\n'
            '                    "dursley"\n'
            '                ],\n'
            '                [\n'
            '                    "harry",\n'
            '                    "potter"\n'
            '                ]\n'
            '            ],\n'
            '            [\n'
            '                [\n'
            '                    "aurelius",\n'
            '                    "dumbledore"\n'
            '                ],\n'
            '                [\n'
            '                    "harry",\n'
            '                    "potter"\n'
            '                ]\n'
            '            ]\n'
            '        ]\n'
            '    }\n'
            '}')
    res2 = ('{\n'
            '    "Question 6": {\n'
            '        "Pair Matches": [\n'
            '            [\n'
            '                [\n'
            '                    "aberforth",\n'
            '                    "dumbledore"\n'
            '                ],\n'
            '                [\n'
            '                    "aurelius",\n'
            '                    "dumbledore"\n'
            '                ]\n'
            '            ],\n'
            '            [\n'
            '                [\n'
            '                    "aberforth",\n'
            '                    "dumbledore"\n'
            '                ],\n'
            '                [\n'
            '                    "harry",\n'
            '                    "potter"\n'
            '                ]\n'
            '            ],\n'
            '            [\n'
            '                [\n'
            '                    "aurelius",\n'
            '                    "dumbledore"\n'
            '                ],\n'
            '                [\n'
            '                    "harry",\n'
            '                    "potter"\n'
            '                ]\n'
            '            ]\n'
            '        ]\n'
            '    }\n'
            '}')
    res3 = '{\n    "Question 6": {\n        "Pair Matches": []\n    }\n}'
    res4 = ('{\n'
            '    "Question 6": {\n'
            '        "Pair Matches": [\n'
            '            [\n'
            '                [\n'
            '                    "malcolm",\n'
            '                    "baddock"\n'
            '                ],\n'
            '                [\n'
            '                    "malcolm",\n'
            '                    "mcgonagall"\n'
            '                ]\n'
            '            ]\n'
            '        ]\n'
            '    }\n'
            '}')
    res5 = ('{\n'
            '    "Question 6": {\n'
            '        "Pair Matches": [\n'
            '            [\n'
            '                [\n'
            '                    "aberforth",\n'
            '                    "dumbledore"\n'
            '                ],\n'
            '                [\n'
            '                    "ballyfumble",\n'
            '                    "stranger"\n'
            '                ]\n'
            '            ]\n'
            '        ]\n'
            '    }\n'
            '}')
    assert graph1.return_results() == res1
    assert graph3.return_results() == res1
    assert graph5.return_results() == res2
    assert graph7.return_results() == res3
    assert graph8.return_results() == res3
    assert graph9.return_results() == res3
    assert graph10.return_results() == res3
    assert graph11.return_results() == res3
    assert graph12.return_results() == res4
    assert graph13.return_results() == res3
    assert graph14.return_results() == res3
    assert graph15.return_results() == res3
    assert graph16.return_results() == res3
    assert graph17.return_results() == res3
    assert graph18.return_results() == res3
    assert graph19.return_results() == res5  # check only nickname appear
