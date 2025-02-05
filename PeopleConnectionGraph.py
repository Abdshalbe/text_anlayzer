import json
import os
import typing
from PeopleKAssociations import PeopleKAssociations


class Node:
    def __init__(self, node_data: str | list[str]):
        """
        constructor to initialize the Node object
        :param node_data: str representing the main __data
        """
        self.__data: str | list[str] = node_data
        self.__connected_data: list["Node"] = []
        self.__apprance_counter = 0

    def add_connected_data(self, data: "Node") -> None:
        """
        adds a person to the connected people
        :param data: Node representing the person to add
        """
        if data not in self.__connected_data:
            self.__connected_data.append(data)

    def get_connected_node(self) -> list["Node"]:
        """
        returns the connected people that are connected to the __data
        :return: list of Node objects representing the connected people
        """
        return self.__connected_data

    def get_data(self) -> str | list[str]:
        """
        get the main node_data of the Node
        :return: str representing the main node_data
        """
        return self.__data

    def get_apprance_counter(self) -> int:
        return self.__apprance_counter

    def increase_apprance_counter(self):
        self.__apprance_counter += 1

    def __str__(self) -> str:
        """
        the way of printing the Node object
        """
        return f'{self.__data}'

    def __repr__(self) -> str:
        """
        the way of representation of the Node object
        """
        return f"{self.__data}"


class Graph:
    """
    Graph class to represent the graph structure
    nodes is ether a list of str or str
    """

    def __init__(self):
        self.__nodes = {}
        self.__edges = []

    def add_node(self, data: str | tuple[list[str]] | tuple[str]) -> None:
        if data not in self.__nodes:
            self.__nodes[data] = Node(data)
            self.__nodes[data].increase_apprance_counter()
        else:
            self.__nodes[data].increase_apprance_counter()

    def add_edge(self, data1: str | tuple[list[str]], data2: str | tuple[list[str]]) -> None:
        if data1 in self.__nodes and data2 in self.__nodes:
            self.__nodes[data1].add_connected_data(self.__nodes[data2])
            self.__nodes[data2].add_connected_data(self.__nodes[data1])
            sorted_names = sorted([self.__nodes[data1], self.__nodes[data2]], key=lambda person: person.get_data())
            if (sorted_names[0], sorted_names[1]) not in self.__edges and (
                    sorted_names[1], sorted_names[0]) not in self.__edges:
                self.__edges.append((sorted_names[0], sorted_names[1]))
            self.__edges = sorted(self.__edges, key=lambda edge: edge[0].get_data())

    def get_node(self, data: str | list[str]) -> Node | None:
        if data not in self.__nodes:
            return None
        else:
            return self.__nodes.get(data)

    def get_edges(self) -> list[Node]:
        return self.__edges

    def get_nodes(self) -> dict[str, Node]:
        return self.__nodes

    def __repr__(self) -> str:
        return str(self.__nodes)

    def __eq__(self, other: "Graph") -> bool:
        return isinstance(other, Graph) and self.__nodes == other.get_nodes() and self.__edges == other.get_edges()


class PeopleConnectionGraph(PeopleKAssociations):
    """
    analyze how people are connected based on their proximity in the document by constructing a graph.
    People are considered connected if they are mentioned within the same window of sentences
    """

    def __init__(self, QNum: int, WindowSize: int, Threshold: int,
                 sentence_input_path: typing.Union[str, os.PathLike] = None,
                 remove_input_path: typing.Union[str, os.PathLike] = None,
                 people_input_path: typing.Union[str, os.PathLike] = None,
                 jsonInputFile: typing.Union[str, os.PathLike] = None, preprocessed: bool = False):
        try:
            #  inherits from PeopleKAssociations class to not duplicate codes
            super().__init__(QNum, sentence_input_path=sentence_input_path, people_input_path=people_input_path,
                             remove_input_path=remove_input_path, json_input_path=jsonInputFile,
                             preprocessed=preprocessed,
                             N=1000000000)
            self.__windowSize = WindowSize
            self.__Threshold = Threshold
            self.__question_number = QNum  # Initialize the question number attribute
            self.__graph = self.__build_people_graph()
            if self.get_sentences_len() < self.__windowSize:
                raise ValueError("The window size should be less than the sentence size.")
        except (FileNotFoundError, PermissionError, TypeError, Exception) as e:
            raise e(f"Error: {e}")

    def return_results(self) -> str:
        """
        Return the results of the connection graph to json file
        :return: string represent the results of the connection graph  in json format
        """
        try:
            def format_edges(edges: list[Node]) -> list[str | list[str]]:
                """
                Converts the __edges from tuples of names to lists of names, formatted as required.
                This method ensures that __edges are in a fixed order.
                :param edges: List of tuples representing the __edges
                :return: List of lists representing the __edges
                """
                formatted_edges = []
                for edge in edges:
                    person1, person2 = edge
                    # Ensure the format is a list of individual words for each data in the edge
                    formatted_edges.append([person1.get_data().split(), person2.get_data().split()])
                # Sort __edges to ensure the order is as required in the question
                formatted_edges = sorted(formatted_edges, key=lambda x: (x[0], x[1]))
                return formatted_edges

            data = {
                f"Question {self.__question_number}": {  # Use the corrected attribute node_data
                    "Pair Matches": format_edges(self.__graph.get_edges())
                }
            }

            json_data = json.dumps(data, indent=4)
            return json_data
        except (FileNotFoundError, PermissionError, TypeError, Exception) as e:
            raise e("error")

    def __count_people_in_windows(self) -> dict[str, dict[str, int]]:
        """
        Counts the number of distinct windows where each pair of people appear together. :return: A dictionary that
        maps each data to other persons and the number of distinct windows they appeared together.
        returns: A dictionary that maps each data to other persons and
        """
        try:
            personMetsCounter = {
                person: {otherPerson: 0 for otherPerson in self.get_names_appearances_idx().keys() if
                         person != otherPerson}
                for person in self.get_names_appearances_idx().keys()}
            # Get the appearance indices of each data
            names_appearances_idx = self.get_names_appearances_idx()
            window_size = self.__windowSize  # Window size for counting occurrences
            total_lines = self.get_sentences_len()  # Loop through each possible window (startIndex)
            for startIndex in range(total_lines - window_size + 1):
                # Set to track unique people appearing in this window
                people_in_window = set()
                # Check each data if they appear in the current window
                for person, indices in names_appearances_idx.items():
                    # If any of data's indices fall within the current window, add them to the set
                    if any(startIndex <= idx < startIndex + window_size for idx in indices):
                        people_in_window.add(person)
                # Count the "meetings" between people in the current window
                for person in people_in_window:
                    for otherPerson in people_in_window:
                        if person != otherPerson:
                            # Increment the counter for the meeting between data and otherPerson
                            personMetsCounter[person][otherPerson] += 1
            return personMetsCounter
        except (FileNotFoundError, PermissionError, TypeError, Exception) as e:
            raise e("error")

    def get_graph(self) -> Graph:
        """
        This method is used to get the graph of the people connections
        :return: graph OF people connections between the people connections
        """
        return self.__graph

    def __build_people_graph(self) -> Graph:
        """
        Build a __graph based on the main dictionary, where __edges are added if the meeting frequency (c_ij) is >=
        __Threshold. :return: A Graph object with the constructed __nodes and __edges.
        """
        try:
            main_dict = self.__count_people_in_windows()
            people_graph = Graph()
            # Add __nodes for all persons in the main dictionary
            for person in main_dict:
                people_graph.add_node(person)
            # Iterate over all data pairs in the dictionary
            for person in main_dict:
                for other_person, meeting_count in main_dict[person].items():
                    if meeting_count >= self.__Threshold:
                        # If the meeting frequency meets the __threshold, add an edge between data and other_person
                        people_graph.add_edge(person, other_person)
            return people_graph
        except (FileNotFoundError, PermissionError, TypeError, Exception) as e:
            raise e("error")
