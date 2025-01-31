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
        assert len(graph.get_edge()) == 1
        edge = graph.get_edge()[0]
        assert edge[0].get_data() == "node1"
        assert edge[1].get_data() == "node2"

        # Add another edge and check that it is sorted correctly
        graph.add_node("node3")
        graph.add_edge("node1", "node3")
        graph.add_edge("node2", "node3")

        # Assert the edges are sorted correctly
        assert graph.get_edge()[0][0].get_data() == "node1"
        assert graph.get_edge()[1][0].get_data() == "node1"
        assert graph.get_edge()[2][0].get_data() == "node2"

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
        assert len(graph.get_edge()) == 1
        edge = graph.get_edge()[0]
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
        edges = graph.get_edge()
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

dataSentence1 = create_temp_csv_with_data(data_text, ['sentence'])
data_names_csv = create_temp_csv_with_data(names1, ['Name', 'Other Names'])
datawords = create_temp_csv_with_data(words_to_remove, ['words'])
parsered_json = process_json_data(Parser(1, dataSentence1, datawords, data_names_csv).return_results())


def test_equal_csr():
    assert PeopleConnectionGraph(6, jsonInputFile=parsered_json, preprocessed=True, WindowSize=2,
                                 Threshold=2).return_results() == PeopleConnectionGraph(6,
                                                                                        sentence_input_path=dataSentence1,
                                                                                        people_input_path=data_names_csv,
                                                                                        remove_input_path=datawords,
                                                                                        Threshold=2,
                                                                                        WindowSize=2).return_results()
    assert PeopleConnectionGraph(6, jsonInputFile=parsered_json, preprocessed=True, WindowSize=2,
                                 Threshold=2).return_results() == PeopleConnectionGraph(6,
                                                                                        sentence_input_path=dataSentence1,
                                                                                        people_input_path=data_names_csv,
                                                                                        remove_input_path=datawords,
                                                                                        Threshold=2,
                                                                                        WindowSize=2).return_results()
    assert PeopleConnectionGraph(6, jsonInputFile=parsered_json, preprocessed=True, WindowSize=1,
                                 Threshold=3).return_results() == PeopleConnectionGraph(6,
                                                                                        sentence_input_path=dataSentence1,
                                                                                        people_input_path=data_names_csv,
                                                                                        remove_input_path=datawords,
                                                                                        Threshold=3,
                                                                                        WindowSize=1).return_results()
    assert PeopleConnectionGraph(6, jsonInputFile=parsered_json, preprocessed=True, WindowSize=2,
                                 Threshold=2).return_results() == PeopleConnectionGraph(6,
                                                                                        sentence_input_path=dataSentence1,
                                                                                        people_input_path=data_names_csv,
                                                                                        remove_input_path=datawords,
                                                                                        Threshold=2,
                                                                                        WindowSize=2).return_results()
