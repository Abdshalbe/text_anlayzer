import os
import sys

import Preprocesser
from Preprocesser import Preprocessor
from PeopleConnectionGraph import Graph, Node
from SequinceCounter import load_Sentences_names
import collections

from Preprocesser import writeTojsonFile
class SentenceGraph:
    def __init__(self,question_number , threshold, remove_input_path: str | os.PathLike = None, json_input_path: str = None, sentence_input_path: str= None, preprocessed: bool = False):
        self.__question_number = question_number
        try:
            if preprocessed:
                self.__sentences, _ = load_Sentences_names(json_input_path)
            else:
                self.__sentences = Preprocesser.Preprocessor(1,sentenceInputPath=sentence_input_path,removeInputPath=remove_input_path).getSentences()
        except (FileNotFoundError, PermissionError, TypeError, Exception) as e:
            print(f"Error: {e}")  # Handle any file-related or other errors
            sys.exit(1)  # Exit program if there's an error
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

    def _dfs(self, node, visited, component):
        visited[node] = True
        component.append(sorted(self.__graph.get_node(node).get_data()))  # Sort each sentence lexicographically before adding to the component
        for neighbor in self.__graph.get_node(node).get_connected_data():
            neighbor_data = neighbor.get_data()
            if not visited[neighbor_data]:
                self._dfs(neighbor_data, visited, component)

    def get_groups(self):
        visited = {tuple(sentence): False for sentence in self.__sentences}
        groups = []

        for sentence in self.__sentences:
            sentence_tuple = tuple(sentence)
            if not visited[sentence_tuple]:
                component = []
                self._dfs(sentence_tuple, visited, component)
                groups.append(component)

        groups = sorted(groups, key=lambda x: len(x))  # Sort groups by size
        for group in groups:
            group.sort()  # Sort sentences lexicographically within each group

        result = {f"Group {i + 1}": group for i, group in enumerate(groups)}

        # Final result format as required
        return {
            "Question 9": {
                "Group Matches": [
                    [f"Group {i + 1}", group] for i, group in enumerate(groups)
                ]
            }
        }


    def write_to_json(self, path):
        return writeTojsonFile(path,self.get_groups())

if __name__ == "__main__":
    sentencesGraph = SentenceGraph(9,threshold=3,sentence_input_path="text_analyzer/2_examples/Q9_examples/exmaple_2/sentences_small_2.csv",remove_input_path="text_analyzer/1_data/Data/REMOVEWORDS.csv")
    print(sentencesGraph.write_to_json("json91.json"))
    # print(sentencesGraph.build_graph())
    # print(sentencesGraph.get_groups())

