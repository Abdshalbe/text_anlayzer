import json
import os
import typing
from collections import deque

from PeopleConnectionGraph import Graph, PeopleConnectionGraph,Node
import time


# Function to measure the execution time of any function
def measure_execution_time(func, *args, **kwargs):
    """
    Measures the execution time of the given function.

    :param func: The function to measure
    :param args: Positional arguments to pass to the function
    :param kwargs: Keyword arguments to pass to the function
    :return: Tuple containing the execution time and the output of the function
    """
    start_time = time.time()
    output = func(*args, **kwargs)
    end_time = time.time()
    execution_time_measure = end_time - start_time
    return execution_time_measure, output


def extract_keys_from_json(file_path: str) -> list:
    """
    Reads a JSON file and extracts the 'keys' array containing pairs of people.
    :param file_path: Path to the JSON file.
    :return: List of pairs (list of lists) from the 'keys' field in the JSON.
    """
    try:
        # Open and load the JSON data from the file
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Extract the 'keys' field
        if "keys" in data:
            return data["keys"]
        else:
            raise KeyError("'keys' field is missing in the provided JSON file.")
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} was not found.")
    except PermissionError:
        raise PermissionError(f"PermissionError: Permission denied to read the file {file_path}.")
    except json.JSONDecodeError:
        raise json.JSONDecodeError(f"JSONDecodeError: The file {file_path} is not a valid JSON file.")
    except KeyError as e:
        raise KeyError(f"KeyError: {e}")
    except Exception as e:
        raise Exception(f"An unexpected error occurred: {e}")


def build_graph_from_json(file_path: str) -> Graph:
    """
    Builds a __graph from a JSON file.
    :param file_path: Path to the JSON file
    :return: A Graph object with __nodes and edges built from the JSON file
    """
    graph = Graph()

    try:
        # Open and load the JSON data
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Get the question number (assuming the structure matches the example)
        question_key = next(key for key in data.keys() if key.lower().startswith('question'))
        pair_matches = data.get(question_key, {}).get("Pair Matches", [])
        # Add __nodes and edges from the pairs in "Pair Matches"
        for pair in pair_matches:
            person1 = " ".join(pair[0])  # Convert the list of names into a single string
            person2 = " ".join(pair[1])
            graph.add_node(person1)  # Add __nodes to the __graph
            graph.add_node(person2)
            # Add edge if the data pair exists
            graph.add_edge(person1, person2)
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The path {file_path} was not found.")
    except json.JSONDecodeError:
        raise json.JSONDecodeError(f"JSONDecodeError: The file {file_path} is not a valid JSON file.")
    except PermissionError:
        raise PermissionError(f"PermissionError: Permission denied to read {file_path}.")
    except Exception as e:
        raise Exception(f"An error occurred: {str(e)}")
    return graph


class CheckConnection:
    def get_graph(self):
        return self.__graph

    def __init__(self, QNum: int,
                 People_connections_to_check: typing.Union[str, os.PathLike],
                 Maximal_distance: int = 0,
                 sentence_input_path: typing.Union[str, os.PathLike] = None,
                 WindowSize: int = None, Threshold: int = None,
                 remove_input_path: typing.Union[str, os.PathLike] = None,
                 people_input_path: typing.Union[str, os.PathLike] = None,
                 jsonInputFile: typing.Union[str, os.PathLike] = None, k=0,
                 fixed_length: bool = False,
                 preprocessed: bool = False):
        try:
            if preprocessed:
                self.__graph = build_graph_from_json(jsonInputFile)
            else:
                self.__graph = PeopleConnectionGraph(QNum=QNum, people_input_path=people_input_path,
                                                     sentence_input_path=sentence_input_path, WindowSize=WindowSize,
                                                     Threshold=Threshold,
                                                     remove_input_path=remove_input_path).get_graph()
            self.__maxDistance = Maximal_distance
            self.__QNum = QNum
            self.__keys = extract_keys_from_json(People_connections_to_check)
            self.__k = k
            self.__is_fixed_length = fixed_length
        except (FileNotFoundError, PermissionError, TypeError, Exception) as e:
            raise Exception(f"Error: {e}")  # Handle any file-related or other errors

    def __bfs_shortest_path_recursive(self, start_name: str, target_name: str) -> list[str]:
        """
        Perform BFS recursively to find the shortest path between two people (nodes) in the graph.
        :param start_name: The starting data (node) node_data.
        :param target_name: The target data (node) node_data.
        :param visited: Set of visited nodes (used for recursion).
        :param path: The current path (used for recursion).
        :return: The shortest path between start_name and target_name as a list of names.
        """
        graph = self.__graph
        # Get the start and end nodes
        start_node = graph.get_node(start_name)
        end_node = graph.get_node(target_name)

        # Check if start or end nodes are not in the graph
        if start_node is None or end_node is None:
            return []

        # Queue for BFS
        queue = deque([start_node])
        # Dictionary to store the parent of each node
        parent = {start_node: None}
        # Set to keep track of visited nodes
        visited = set([start_node])

        # Perform BFS
        while queue:
            current_node = queue.popleft()

            # If we reach the destination, reconstruct the path
            if current_node == end_node:
                path = []
                while current_node is not None:
                    path.append(current_node.get_data())
                    current_node = parent[current_node]
                return path[::-1]  # Reverse the path to get start -> end

            # Explore neighbors
            for neighbor in current_node.get_connected_data():
                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = current_node
                    queue.append(neighbor)

        # If no path is found
        return []

    def __get_result_without_fixed_length(self):
        output = []
        for relationToCheck in self.__keys:
            relationToCheck = sorted(relationToCheck)
            shortest_path = self.__bfs_shortest_path_recursive(relationToCheck[0], relationToCheck[1])
            if len(shortest_path) == 0 or len(shortest_path) > self.__maxDistance:
                output.append([relationToCheck[0], relationToCheck[1], False])
            elif 1 <= len(shortest_path) <= self.__maxDistance:
                output.append([relationToCheck[0], relationToCheck[1], True])
        return sorted(output)

    def __get_result_with_fixed_length(self):
        output = []
        for relationToCheck in self.__keys:
            relationToCheck = sorted(relationToCheck)
            is_connected_with_k_nodes = self.__dfs_find_path(relationToCheck[0], relationToCheck[1])
            output.append([relationToCheck[0], relationToCheck[1], is_connected_with_k_nodes])
        return sorted(output)

    def return_results(self) -> str:
        """
        Return the results of the sequences to json file
        :return: string represent the results of the sequences in json format
        """
        if not self.__is_fixed_length:
            data = self.__get_result_without_fixed_length()
        else:
            data = self.__get_result_with_fixed_length()
        # Create the dictionary structure based on the desired format
        result_data = {
            f"Question {self.__QNum}": {
                "Pair Matches": data
            }
        }
        json_data = json.dumps(result_data, indent=4)
        return json_data

    def __dfs_find_path_exact_length(self, start: str, target: str, path=None, visited=None, length=0) -> bool:
        """
        Use Depth-First Search to find a path of exact length between two people (nodes) in the graph.
        :param start: The starting data's node_data.
        :param target: The target data's node_data.
        :param path: The current path (used for recursion).
        :param visited: Set of visited nodes to avoid revisiting.
        :param length: The current length of the path.
        :return: True if a path of exact length exists, False otherwise.
        """
        graph = self.__graph
        # Initialize path and visited set if not provided
        if path is None:  # base cases
            path = [start]
        if visited is None:
            visited = set()
        # If the path length exceeds the desired length, stop exploring further
        if length > self.__k:
            return False
        # If the path length is exactly k and the target is reached, return True
        if length == self.__k and start == target:
            return True
        # Mark the current node as visited
        visited.add(start)
        # Explore the neighbors (connected people) of the current node
        if graph.get_node(start):
            for neighbor in graph.get_node(start).get_connected_data():
                neighbor_name = neighbor.get_data()
                # If the neighbor has not been visited, recurse
                if neighbor_name not in visited:
                    # Recur for the neighbor and increase the path length
                    if self.__dfs_find_path_exact_length(neighbor_name, target, path + [neighbor_name], visited,
                                                         length + 1):
                        return True
        # Backtrack, remove the current node from the visited set
        visited.remove(start)
        # No path found
        return False


if __name__ == '__main__':
    check = CheckConnection(7,
                            sentence_input_path="text_analyzer/2_examples/Q7_examples/exmaple_2/sentences_small_2.csv",
                            people_input_path="text_analyzer/2_examples/Q7_examples/exmaple_2/people_small_2.csv",
                            remove_input_path="text_analyzer/1_data/Data/REMOVEWORDS.csv", Threshold=2,
                            WindowSize=5,
                            People_connections_to_check="text_analyzer/2_examples/Q7_examples/exmaple_2/people_connections_2.json",
                            Maximal_distance=1000, fixed_length=False)

    # execution_time, result = measure_execution_time(check.write_to_json, "W3Th2fl8.json")

    # Print the result and the execution time
    print(check.return_results())
