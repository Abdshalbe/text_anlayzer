import os
import typing

from PeopleKAssocions import PeopleKAssocions


class Node:
    def __init__(self, name: str):
        self.name = name
        self.connected_people = []

    def add_connected_person(self, person: "Node"):
        if person not in self.connected_people:
            self.connected_people.append(person)

    def get_connected_people(self):
        return self.connected_people

    def __repr__(self):
        return f"Node({self.name})"


class Graph:
    def __init__(self):
        self.nodes = {}

    def add_node(self, name: str):
        if name not in self.nodes:
            self.nodes[name] = Node(name)

    def add_edge(self, person1: str, person2: str):
        if person1 in self.nodes and person2 in self.nodes:
            self.nodes[person1].add_connected_person(self.nodes[person2])
            self.nodes[person2].add_connected_person(self.nodes[person1])

    def get_node(self, name: str):
        return self.nodes.get(name)

    def __repr__(self):
        return str(self.nodes)


class PeopleConnectionGraph(PeopleKAssocions):
    def __init__(self, QNum: int, WindowSize: int, Threshold: int,
                 sentence_input_path: typing.Union[str, os.PathLike] = None,
                 remove_input_path: typing.Union[str, os.PathLike] = None,
                 people_input_path: typing.Union[str, os.PathLike] = None,
                 jsonInputFile: typing.Union[str, os.PathLike] = None, preprocessed: bool = False):
        super().__init__(QNum, sentence_input_path=sentence_input_path, people_input_path=people_input_path,
                         remove_input_path=remove_input_path, json_input_path=jsonInputFile, preprocessed=preprocessed,
                         N=100000)
        self.__windowSize = WindowSize
        self.__Threshold = Threshold
        self.nodes = {}  # Dictionary to hold Node objects by their name

    def count_people_in_window(self):
        """
        Counts the number of distinct windows where each pair of people appear together.
        :return: A dictionary that maps each person to other persons and the number of distinct windows they appeared together.
        """
        personMetsCounter = {
            person: {otherPerson: 0 for otherPerson in self.get_names_apearances_idx().keys() if person != otherPerson}
            for person in self.get_names_apearances_idx().keys()
        }
        # Get the appearance indices of each person
        names_apearances_idx = self.get_names_apearances_idx()
        window_size = self.__windowSize  # Window size for counting occurrences
        total_lines = self.get_lines_number()

        # Loop through each possible window (startIndex)
        for startIndex in range(total_lines - window_size + 1):
            # Set to track unique people appearing in this window
            people_in_window = set()

            # Check each person if they appear in the current window
            for person, indices in names_apearances_idx.items():
                # If any of person's indices fall within the current window, add them to the set
                if any(startIndex <= idx < startIndex + window_size for idx in indices):
                    people_in_window.add(person)

            # Count the "meetings" between people in the current window
            for person in people_in_window:
                for otherPerson in people_in_window:
                    if person != otherPerson:
                        # Increment the counter for the meeting between person and otherPerson
                        personMetsCounter[person][otherPerson] += 1
        return personMetsCounter

    def build_people_graph(self):
        """
        Build a graph based on the main dictionary, where edges are added if the meeting frequency (c_ij) is >= __Threshold.
        :param main_dict: A dictionary where main_dict[i] contains a dictionary of {j: c_ij} representing meetings between persons i and j.
        :return: A Graph object with the constructed nodes and edges.
        """
        main_dict = self.count_people_in_window()
        graph = Graph()
        # Add nodes for all persons in the main dictionary
        for person in main_dict:
            graph.add_node(person)
        # Iterate over all person pairs in the dictionary
        for person in main_dict:
            for other_person, meeting_count in main_dict[person].items():
                if meeting_count >= self.__Threshold:
                    # If the meeting frequency meets the threshold, add an edge between person and other_person
                    graph.add_edge(person, other_person)
        return graph


if __name__ == '__main__':
    graph = PeopleConnectionGraph(6,
                                  people_input_path="text_analyzer/2_examples/Q6_examples/example_1/people_small_1.csv",
                                  sentence_input_path="text_analyzer/2_examples/Q6_examples/example_1/sentences_small_1.csv",
                                  remove_input_path="text_analyzer/1_data/data/REMOVEWORDS.csv", Threshold=4,
                                  WindowSize=4)
    # print(graph.get_names_apearances_idx())
    # print(graph.build_people_graph().get_node("harry potter").get_connected_people())
    print(graph.get_lines_number())
