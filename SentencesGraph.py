import json
import os
from Parser import Parser
from PeopleConnectionGraph import Graph
from SequenceCounter import load_Sentences_names


class SentenceGraph:
    """
    This class represents to creat a connection groups in which sentence are connected
    """
    def __init__(self, question_number, threshold: int, remove_input_path: str | os.PathLike = None,
                 json_input_path: str = None, sentence_input_path: str = None, preprocessed: bool = False):
        self.__question_number = question_number
        try:
            if preprocessed:
                self.__sentences, _ = load_Sentences_names(json_input_path)
            else:
                self.__sentences = Parser(1, sentenceInputPath=sentence_input_path,
                                          removeInputPath=remove_input_path).getSentences()
        except (FileNotFoundError, PermissionError, TypeError, Exception) as e:
            raise e(f"Error: {e}")  # Handle any file-related or other errors
        self.__threshold = threshold  # Minimum number of shared words to form an edge
        self.__graph = self.__build_graph()  # Adjacency list

    def __build_graph(self):
        """
        Builds the graph from the sentences in the sentences and connect to node if there hava at least __threshold
        mutual words :return: graph representing the sentence connection graph
        """
        graph = Graph()

        def count_mutual(line1: list[str], line2: list[str]):
            return len(set(line1) & set(line2))

        for sentence in self.__sentences:
            graph.add_node(tuple(sentence))
        for i in range(len(self.__sentences) - 1):
            for j in range(i + 1, len(self.__sentences)):
                if count_mutual(self.__sentences[i], self.__sentences[j]) >= self.__threshold:
                    graph.add_edge(tuple(self.__sentences[i]), tuple(self.__sentences[j]))
        return graph

    def __dfs(self, node, visited, component):
        """
        find all the connected nodes in the graph that connected to node        :param node:  representing the
        current node :param visited: dict of visited nodes if visited will be true else false :param component: list
        of list to nodes"""
        visited[node] = True
        component.append([self.__graph.get_node(node).get_data(), self.__graph.get_node(node).get_apprance_counter()])  # Sort each sentence lexicographically before adding to the component
        for neighbor in self.__graph.get_node(node).get_connected_node():
            neighbor_data = neighbor.get_data()
            if not visited[neighbor_data]:
                self.__dfs(neighbor_data, visited, component)

    def __get_groups(self):
        """
        fined all the components of the graph, so we can use to fined all the components
        :return: all components of the graph, so we can use it in final result
        """
        #  Prepare a visited dictionary (you already have this logic)
        visited = {tuple(sentence): False for sentence in self.__sentences}
        groups = []
        #  Perform DFS to find connected components
        for sentence in self.__sentences:
            sentence_tuple = tuple(sentence)
            if not visited[sentence_tuple]:
                component = []
                self.__dfs(sentence_tuple, visited, component)
                if len(component) == 1:
                    if self.__threshold > len(component[0]):

                        for _ in range(component[0][1]):
                            groups.append([component[0][0]])
                    else:
                        groups.append([component[0][0] for _ in range(component[0][1])])
                else:
                    result = []
                    for component in component:
                        for _ in range(component[1]):
                            result.append(component[0])
                    groups.append(result)
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

    def return_results(self) -> str:
        """
        Return the results of the groups to json formate
        :return: string represent the results of the groups in json format
        """
        json_data = json.dumps(self.__get_groups(), indent=4)
        return json_data


if __name__ == "__main__":
    sentencesGraph = SentenceGraph(9, threshold=2,
                                   sentence_input_path="text_analyzer/2_examples/Q9_examples/exmaple_3"
                                                       "/sentences_small_3.csv",
                                   remove_input_path="text_analyzer/1_data/Data/REMOVEWORDS.csv")

    print(sentencesGraph.return_results())
