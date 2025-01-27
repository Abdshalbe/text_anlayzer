import json
import os
import sys
import typing
from collections import deque

from PeopleConnectionGraph import Graph, PeopleConnectionGraph
import time


# Function to measure the execution time of any function
def measure_execution_time(func, *args, **kwargs):
    """
    Measures the execution time of the given function.

    :param func: The function to measure
    :param args: Positional arguments to pass to the function
    :param kwargs: Keyword arguments to pass to the function
    :return: Tuple containing the execution time and the result of the function
    """
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    execution_time= end_time - start_time
    return execution_time, result

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
                 jsonInputFile: typing.Union[str, os.PathLike] = None, k=0, fixed_length: bool = False,
                 preprocessed: bool = False):
        try:
            if preprocessed:
                self.__graph = self.build_graph_from_json(jsonInputFile)
            else:
                self.__graph = PeopleConnectionGraph(QNum=QNum, people_input_path=people_input_path,
                                                     sentence_input_path=sentence_input_path, WindowSize=WindowSize,
                                                     Threshold=Threshold,
                                                     remove_input_path=remove_input_path).get_graph()
            self.__maxDistance = Maximal_distance
            self.__QNum = QNum
            self.__keys = self.extract_keys_from_json(People_connections_to_check)
            self.__k = k
            self.__is_fixed_length = fixed_length
        except (FileNotFoundError, PermissionError, TypeError, Exception) as e:
            print(f"Error: {e}")  # Handle any file-related or other errors
            sys.exit(1)  # Exit program if there's an error
    def bfs_shortest_path(self, start_name: str, target_name: str) -> list[str]:
        """
        Perform BFS to find the shortest path between two people (nodes) in the graph.
        :param start_name: The starting person (node) name.
        :param target_name: The target person (node) name.
        :return: The shortest path between start_name and target_name as a list of names.
        """
        graph = self.__graph
        # Edge case: If start and target are the same
        if start_name == target_name:
            return [start_name]

        # Initialize visited set to keep track of visited nodes
        visited = set()
        # Queue to store nodes to be explored, initialized with the start node
        queue = deque([(start_name, [start_name])])  # (current_node, path_so_far)
        while queue:
            current_node, path = queue.popleft()

            # If we find the target node, return the path taken
            if current_node == target_name:
                return path

            # Mark the current node as visited
            visited.add(current_node)

            # Explore neighbors (connected people) of the current node
            if graph.get_node(current_node) is not None:
                for neighbor in graph.get_node(current_node).get_connected_people():
                    neighbor_name = neighbor.get_name()
                    if neighbor_name not in visited:
                        # Append the neighbor to the path and enqueue it
                        queue.append((neighbor_name, path + [neighbor_name]))
                        visited.add(neighbor_name)

        # If no path is found, return an empty list
        return []

    def extract_keys_from_json(self, file_path: str) -> list:
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

    def build_graph_from_json(self, file_path: str) -> Graph:
        """
        Builds a graph from a JSON file.
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
                graph.add_node(person1)  # Add __nodes to the graph
                graph.add_node(person2)
                # Add edge if the person pair exists
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

    def get_keys(self):
        return self.__keys

    def get_result_without_fixed_length(self):
        result = []
        for realion_to_check in self.__keys:
            realion_to_check = sorted(realion_to_check)
            shortest_path = self.bfs_shortest_path(realion_to_check[0], realion_to_check[1])
            if len(shortest_path) == 0 or len(shortest_path) > self.__maxDistance:
                result.append([realion_to_check[0], realion_to_check[1], False])
            elif 1 <= len(shortest_path) <= self.__maxDistance:
                result.append([realion_to_check[0], realion_to_check[1], True])
        return sorted(result)

    def get_result_with_fixed_length(self):
        result = []
        for realion_to_check in self.__keys:
            realion_to_check = sorted(realion_to_check)
            shortest_path = self.dfs_find_path(realion_to_check[0], realion_to_check[1])
            result.append([realion_to_check[0], realion_to_check[1], shortest_path])
        return sorted(result)

    def write_to_json(self, file_path: typing.Union[str, os.PathLike]) -> bool:
        """
        Writes the provided data into a JSON file in the specified format.

        :param file_path: Path to the JSON file to save the results to.
        :return: True if the file was successfully written, False otherwise.
        """
        try:
            if not self.__is_fixed_length :
                data = self.get_result_without_fixed_length()
            else:
                data = self.get_result_with_fixed_length()
            # Create the dictionary structure based on the desired format
            result = {
                f"Question {self.__QNum}": {
                    "Pair Matches": data
                }
            }

            # Open the file and write the JSON data
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=4)

            return True

        except FileNotFoundError:
            print(f"FileNotFoundError: The path {file_path} was not found.")
        except PermissionError:
            print(f"PermissionError: Permission denied to write to {file_path}.")
        except IOError as e:
            print(f"IOError: An error occurred while writing to {file_path}. Error: {str(e)}")
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")

        return False  # Return False if an error occurred

    def dfs_find_path(self, start: str, target: str, path=None, visited=None) -> bool:
        """
        Checks if there is a path of exact length k between two people in the graph.
        :param start: The starting person's name.
        :param target: The target person's name.
        :param path: The current path (used for recursion).
        :param visited: Set of visited nodes to avoid revisiting.
        :return: True if a path of length k exists, False otherwise.
        """
        graph = self.__graph
        # Initialize path and visited set if not provided
        if path is None:
            path = [start]
        if visited is None:
            visited = set()
        # If the path length is greater than k, return False (we want exactly k)
        if len(path) > self.__k:
            return False
        # If the path length is exactly k and the target is reached, return True
        if len(path) == self.__k and path[-1] == target:
            return True
        # Mark the current node as visited
        visited.add(start)
        if graph.get_node(start):
            # Explore all connected nodes (neighbors)
            for neighbor in graph.get_node(start).get_connected_people():
                neighbor_name = neighbor.get_name()
                if neighbor_name not in visited:
                    # Recursively call DFS with the next node
                    if self.dfs_find_path(neighbor_name, target, path + [neighbor_name], visited):
                        return True

            # Backtrack, remove the current node from the path and visited set
        visited.remove(start)
        return False


if __name__ == '__main__':
    check = CheckConnection(8,
                            sentence_input_path="text_analyzer/2_examples/Q8_examples/exmaple_3/sentences_small_1.csv",
                            people_input_path="text_analyzer/2_examples/Q8_examples/exmaple_3/people_small_1.csv",
                            remove_input_path="text_analyzer/1_data/data/REMOVEWORDS.csv", Threshold=2,
                            WindowSize=3,
                            People_connections_to_check="text_analyzer/2_examples/Q8_examples/exmaple_3/people_connections_1.json",
                            k=3, fixed_length=True)

    execution_time, result = measure_execution_time(check.write_to_json, "W3Th2fl8.json")

    # Print the result and the execution time
    print(execution_time, result)
