from PeopleConnectionGraph import Graph, PeopleConnectionGraph,Node

def test_Node_get_value():
    node1 = Node("node1")
    node2 = Node("node2")
    node3 = Node("node3")
    node4 = Node(['hello','world'])
    assert node1.get_data() == "node1"
    assert node2.get_data() == "node2"
    assert node3.get_data() == "node3"
    assert node4.get_data() == ['hello','world']

def test_Node_get_children():
    node1 = Node("node1")
    node2 = Node("node2")
    node3 = Node("node3")
    node4 = Node(['hello','world'])
    node1.add_connected_data(node2)
    node1.add_connected_data(node3)
    assert node1.get_connected_data() == [node2,node3]
    node1.add_connected_data(node4)
    assert node1.get_connected_data() == [node2,node3,node4]


def test_Graph_get_value():
    pass