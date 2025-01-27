import json
import sys
import typing
import os
from NamesCounter import NamesCounter
from Preprocesser import Preprocessor
from SequinceCounter import SequinceCounter
from SequinceCounter import generate_k_seqs


class PeopleKAssocions:
    def __init__(self, QNum: int, N: int, sentence_input_path: typing.Union[str, os.PathLike] = None,
                 remove_input_path: typing.Union[str, os.PathLike] = None,
                 people_input_path: typing.Union[str, os.PathLike] = None,
                 json_input_path: typing.Union[str, os.PathLike] = None, preprocessed: bool = False):

        self.__qustion_number: int = QNum
        self.__N: int = N
        self.__sentence_input_path: typing.Union[str, os.PathLike] = sentence_input_path
        self.__remove_input_path: typing.Union[str, os] = remove_input_path
        self.__people_input_path: typing.Union[str, os.PathLike] = people_input_path
        self.__json_input_path: typing.Union[str, os.PathLike] = json_input_path
        self.__preprocessed: bool = preprocessed
        try:
            if preprocessed:
                self.__names, self.__sentences = self.__get_names_sentences_from_json()
            else:
                self.__names, self.__sentences = self.__get_names_sentences_from_paths()
        except (FileNotFoundError, PermissionError, TypeError, Exception) as e:
            print(f"Error: {e}")  # Handle any file-related or other errors
            sys.exit(1)  # Exit program if there's an error

    def create_k_seqs(self) -> list[str|list[list[str]]]:
        """
        Creates the K-Sequences output ready for write to json file
        :return: a list of lists to lists of K-sequences
        """
        res = []

        def process_sequences(seq_counts: dict[str, list[tuple[str, int]]]) -> list[list[str]]:
            """
            Processes the sequences in `seq_counts` and combines all sequences of varying lengths.
            Then it sorts them lexicographically while maintaining their structure as a list of lists.
            """
            result = []

            # Loop through each sequence type ('1_seq', '2_seq', etc.)
            for key in sorted(seq_counts.keys(),
                              key=lambda x: int(x.split('_')[0])):  # Sort keys like '1_seq', '2_seq', etc.
                seq_list = seq_counts[key]

                # Add the sequences (stored as tuples) into the result list
                for seq, count in seq_list:
                    result.append(list(seq))  # Convert tuple to list and append it

            # Sort all sequences lexicographically
            result.sort()  # This sorts the sequences in lexicographical order

            return result

        idx_people = self.get_names_apearances_idx()
        for person in sorted(idx_people.keys()):
            sentences = [line for index, line in enumerate(self.__sentences) if index in idx_people[person]]
            res.append([person,process_sequences(generate_k_seqs(sentences, self.__N))])
        return res

    def write_to_json(self, filePath: typing.Union[os, str]) -> bool:
        """
        try to write to a json file the results of the class NamesCounter
        :param filePath: path to json file to save the results to
        :return: True if the file was successfully written, False otherwise
        """
        try:
            with open(filePath, 'w', encoding='utf-8') as f:
                res = False
                data = {
                    f"Question {self.__qustion_number}": {
                         "Person Contexts and K-Seqs": self.create_k_seqs()
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

    def get_lines_number(self):
        """
         getter method for the number of lines in the supplied text
        :return: the number of lines in the supplied text
        """
        return len(self.__sentences)

    def get_names_apearances_idx(self) -> dict[str, list[int]]:
        """
        Returns a dictionary mapping each name to a lines were they appeared
        :return: a dictionary mapping each name to a lines were they appeared
        """
        try:
            name_counter = NamesCounter(5, preprocessed=self.__preprocessed,
                                        sentence_input_path=self.__sentence_input_path,
                                        remove_input_path=self.__remove_input_path,
                                        people_input_path=self.__people_input_path,
                                        json_input_path=self.__json_input_path)
            _, namesIdx = name_counter.count_names()
        except (FileNotFoundError, PermissionError, TypeError, Exception) as e:
            print(f"Error: {e}")
            sys.exit(1)

        def remove_duplicates(data: dict[str, list[int]]) -> dict[str, list[int]]:
            """
            Removes duplicate values from the lists in the dictionary while maintaining the original order.
            """
            for key, values in data.items():
                data[key] = list(dict.fromkeys(values))  # Using dict.fromkeys to preserve order and remove duplicates
            return data

        return remove_duplicates(namesIdx)

    def __get_names_sentences_from_json(self) -> (list[list[str]], list[list[list[str]]]):
        """
        Loads preprocessed data from a JSON file.
        :param json_file_path: Path to the preprocessed JSON file
        :time complicity = O(1) because the file is already preprocessed and therefore
         we just want to enter the data
        """
        try:
            with open(self.__json_input_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Dynamically get the first key that matches 'Question' followed by a number
                question_key = next(key for key in data.keys() if key.lower().startswith('question'))
                # Extract __sentences from the dynamic question key
                names = data.get(question_key, {}).get('Processed Names', [])
                sentences = data.get(question_key, {}).get('Processed Sentences', [])
        except FileNotFoundError:
            raise FileNotFoundError(f"FileNotFoundError: The file {self.__json_input_path} was not found.")
        except json.JSONDecodeError:
            raise json.JSONDecodeError(f"JSONDecodeError: The file {self.__json_input_path} is not a valid JSON file.")

        except PermissionError:
            raise PermissionError(f"PermissionError: Permission denied to read {self.__json_input_path}.")

        except Exception as e:
            raise Exception(f"An error occurred while loading preprocessed data: {str(e)}")
        return names, sentences

    def __get_names_sentences_from_paths(self) -> (list[list[str]], list[list[list[str]]]):
        """
        load a list of names and sentences from a geetin file path to process
        :return: lists of names and sentences to be set
        """
        try:
            dataLoader = Preprocessor(1, sentenceInputPath=self.__sentence_input_path,
                                      removeInputPath=self.__remove_input_path,
                                      peopleInputPath=self.__people_input_path)
            sentences = dataLoader.getSentences()
            names = dataLoader.get_people()
        except ValueError:
            raise
        except FileNotFoundError as e:
            raise FileNotFoundError("{0}".format(e))
        except PermissionError as e:
            raise PermissionError("{0}".format(e))
        except Exception as e:
            raise Exception("{0}".format(e))
        return names, sentences


if __name__ == "__main__":
    PeopleKAssocions1 = PeopleKAssocions(6,people_input_path="text_analyzer/2_examples/Q6_examples/example_1/people_small_1.csv",
                          sentence_input_path="text_analyzer/2_examples/Q6_examples/example_1/sentences_small_1.csv ",
                          remove_input_path="text_analyzer/1_data/data/REMOVEWORDS.csv",N = 6)
    print(PeopleKAssocions1.get_names_apearances_idx())
