import os
import sys

import Parser
from Parser import Parser
from PeopleConnectionGraph import Graph, Node
from SequinceCounter import load_Sentences_names
import collections

from Parser import writeTojsonFile
class SentenceGraph:
    def __init__(self, question_number, threshold, remove_input_path: str | os.PathLike = None, json_input_path: str = None, sentence_input_path: str= None, preprocessed: bool = False):
        self.__question_number = question_number
        try:
            if preprocessed:
                self.__sentences, _ = load_Sentences_names(json_input_path)
            else:
                self.__sentences = Parser.Parser(1, sentenceInputPath=sentence_input_path, removeInputPath=remove_input_path).getSentences()
        except (FileNotFoundError, PermissionError, TypeError, Exception) as e:
            raise e # Handle any file-related or other errors
        self.threshold = threshold  # Minimum number of shared words to form an edge
        self.__graph = self.builed_graph() # Adjacency list

    def builed_graph(self):
        graph = Graph()
        def count_mutual(line1:list[str],line2:list[str]):
            return len(set(line1) & set(line2))
        for sentence in self.__sentences:
            graph.add_node(tuple(sentence))
        for i in range(len(self.__sentences)-1):
            for j in range(i+1,len(self.__sentences)):
                if count_mutual(self.__sentences[i],self.__sentences[j])>=self.threshold:
                    graph.add_edge(tuple(self.__sentences[i]),tuple(self.__sentences[j]))
        return graph

    def __dfs(self, node, visited, component):
        visited[node] = True
        component.append(self.__graph.get_node(node).get_data())  # Sort each sentence lexicographically before adding to the component
        for neighbor in self.__graph.get_node(node).get_connected_data():
            neighbor_data = neighbor.get_data()
            if not visited[neighbor_data]:
                self.__dfs(neighbor_data, visited, component)

    def get_groups(self):
        #  Prepare a visited dictionary (you already have this logic)
        visited = {tuple(sentence): False for sentence in self.__sentences}
        groups = []

        #  Perform DFS to find connected components
        for sentence in self.__sentences:
            sentence_tuple = tuple(sentence)
            if not visited[sentence_tuple]:
                component = []
                self.__dfs(sentence_tuple, visited, component)
                groups.append(component)
        for group in groups:
            group.sort(key=lambda sentence: list(sentence))
        groups.sort(key=lambda g: (len(g), g))

        # Construct final result format
        return {
            "Question 9": {
                "group Matches": [
                    [f"Group {i + 1}", group] for i, group in enumerate(groups)
                ]
            }
        }

    def write_to_json(self, path):
        return writeTojsonFile(path,self.get_groups())

if __name__ == "__main__":
    sentencesGraph = SentenceGraph(9,threshold=1,sentence_input_path="text_analyzer/2_examples/Q9_examples/exmaple_3/sentences_small_3.csv",remove_input_path="text_analyzer/1_data/Data/REMOVEWORDS.csv")
    print(sentencesGraph.write_to_json("json91.json"))
    # print(sentencesGraph.build_graph())
    # print(sentencesGraph.get_groups())

