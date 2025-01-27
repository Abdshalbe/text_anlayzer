import json
import os
import typing
from PeopleKAssocions import PeopleKAssocions


class Node:
    def __init__(self, name: str):
        """
        constructor to initialize the Node object
        :param name: str representing the main __name
        """
        self.__name = name
        self.__connected_people = []

    def add_connected_person(self, person: "Node"):
        """
        adds a person to the connected people
        :param person: Node representing the person to add
        """
        if person not in self.__connected_people:
            self.__connected_people.append(person)

    def get_connected_people(self):
        """
        returns the connected people that are connected to the __name
        :return: list of Node objects representing the connected people
        """
        return self.__connected_people

    def get_name(self):
        """
        get the main name of the Node
        :return: str representing the main name
        """
        return self.__name

    def __str__(self):
        """
        the way of printing the Node object
        """
        return f'{self.__name}'

    def __repr__(self):
        """
        the way of representation of the Node object
        """
        return f"{self.__name}"


class Graph:
    def __init__(self):
        self.nodes = {}
        self.edges = []

    def add_node(self, name: str):
        if name not in self.nodes:
            self.nodes[name] = Node(name)

    def add_edge(self, person1: str, person2: str):
        if person1 in self.nodes and person2 in self.nodes:
            self.nodes[person1].add_connected_person(self.nodes[person2])
            self.nodes[person2].add_connected_person(self.nodes[person1])
            sorted_names = sorted([self.nodes[person1], self.nodes[person2]], key=lambda person: person.get_name())
            if (sorted_names[0], sorted_names[1]) not in self.edges:
                self.edges.append((sorted_names[0], sorted_names[1]))
            self.edges = sorted(self.edges, key=lambda edge: edge[0].get_name())

    def get_node(self, name: str):
        return self.nodes.get(name)

    def get_edge(self):
        return self.edges

    def __repr__(self):
        return str(self.nodes)


class PeopleConnectionGraph(PeopleKAssocions):
    def __init__(self, QNum: int, WindowSize: int, Threshold: int,
                 sentence_input_path: typing.Union[str, os.PathLike] = None,
                 remove_input_path: typing.Union[str, os.PathLike] = None,
                 people_input_path: typing.Union[str, os.PathLike] = None,
                 jsonInputFile: typing.Union[str, os.PathLike] = None, preprocessed: bool = False):
        super().__init__(QNum, sentence_input_path=sentence_input_path, people_input_path=people_input_path,
                         remove_input_path=remove_input_path, json_input_path=jsonInputFile, preprocessed=preprocessed, N=100000)
        self.__windowSize = WindowSize
        self.__Threshold = Threshold
        self.__question_number = QNum  # Initialize the question number attribute
        self.__graph = self.build_people_graph()

    def write_to_json(self, filePath: typing.Union[os, str]) -> bool:
        """
        Write the graph edges to a JSON file with the required format.
        :param filePath: path to JSON file to save the results to
        :return: True if the file was successfully written, False otherwise
        """
        try:
            with open(filePath, 'w', encoding='utf-8') as f:
                res = False
                data = {
                    f"Question {self.__question_number}": {  # Use the corrected attribute name
                         "Pair Matches": self.__format_edges(self.__graph.edges)
                    }
                }
                # Try to write the data to the file
                json.dump(data, f, ensure_ascii=False, indent=4)
                res = True
        except FileNotFoundError:
            print(f"FileNotFoundError: The path {filePath} was not found.")
        except PermissionError:
            print(f"PermissionError: Permission denied to write to {filePath}.")
        except IOError as e:
            print(f"IOError: An error occurred while writing to {filePath}. Error: {str(e)}")
            return False
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")
        return res


    def count_people_in_window(self):
        """
        Counts the number of distinct windows where each pair of people appear together.
        :return: A dictionary that maps each person to other persons and the number of distinct windows they appeared together.
        """
        personMetsCounter = {
            person: {otherPerson: 0 for otherPerson in self.get_names_apearances_idx().keys() if person != otherPerson}
            for person in self.get_names_apearances_idx().keys()}
        # Get the appearance indices of each person
        names_apearances_idx = self.get_names_apearances_idx()
        window_size = self.__windowSize  # Window size for counting occurrences
        total_lines = self.get_sentences_len()  # Loop through each possible window (startIndex)
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

    def __format_edges(self, edges):
        """
        Converts the edges from tuples of names to lists of names, formatted as required.
        This method ensures that edges are in a fixed order.
        :param edges: List of tuples representing the edges
        :return: List of lists representing the edges
        """
        formatted_edges = []
        for edge in edges:
            person1, person2 = edge
            # Ensure the format is a list of individual words for each person in the edge
            formatted_edges.append([person1.get_name().split(), person2.get_name().split()])

        # Sort edges to ensure the order is as required in the question
        formatted_edges = sorted(formatted_edges, key=lambda x: (x[0], x[1]))

        return formatted_edges
    def build_people_graph(self):
        """
        Build a graph based on the main dictionary, where edges are added if the meeting frequency (c_ij) is >= __Threshold.
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
    # graph = PeopleConnectionGraph(6, people_input_path=r"text_analyzer/2_examples/Q5_examples/example_1/people_small_1.csv",
    #                                      sentence_input_path="text_analyzer/2_examples/Q5_examples/example_1/sentences_small_1.csv",
    #                                      remove_input_path="text_analyzer/1_data/data/REMOVEWORDS.csv",Threshold=4,
    #                               WindowSize=4)
    graph = PeopleConnectionGraph(6, people_input_path="text_analyzer/2_examples/Q6_examples/exmaple_4/people_small_4.csv",
                                         sentence_input_path="text_analyzer/2_examples/Q6_examples/exmaple_4/sentences_small_4.csv",
                                         remove_input_path="text_analyzer/1_data/data/REMOVEWORDS.csv",Threshold=1,
                                  WindowSize=5)
    graph.write_to_json("Q6_example_1.json")
    # print(graph.count_people_in_window())