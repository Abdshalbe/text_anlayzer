import json
import os
import sys
import typing

from NamesCounter import NamesCounter
from Parser import writeTojsonFile
from SequinceCounter import generate_k_seqs, load_Sentences_names, load_data


class PeopleKAssociations:
    def __init__(self, QNum: int, N: int, sentence_input_path: typing.Union[str, os.PathLike] = None,
                 remove_input_path: typing.Union[str, os.PathLike] = None,
                 people_input_path: typing.Union[str, os.PathLike] = None,
                 json_input_path: typing.Union[str, os.PathLike] = None, preprocessed: bool = False):

        self.__question_number: int = QNum
        self.__N: int = N
        self.__sentence_input_path: typing.Union[str, os.PathLike] = sentence_input_path
        self.__remove_input_path: typing.Union[str, os] = remove_input_path
        self.__people_input_path: typing.Union[str, os.PathLike] = people_input_path
        self.__json_input_path: typing.Union[str, os.PathLike] = json_input_path
        self.__preprocessed: bool = preprocessed
        try:
            if preprocessed:
                self.__sentences, self.__names = load_Sentences_names(json_input_path)
            else:
                self.__sentences, self.__names = load_data(sentence_input_path=sentence_input_path,
                                                           remove_input_path=remove_input_path,
                                                           people_input_path=people_input_path)
        except (FileNotFoundError, PermissionError, TypeError, Exception) as e:
            raise e(f"Error: {e}")  # Handle any file-related or other errors

    def get_sentences_len(self) -> int:
        """
        Returns the number of sentences is given in the input file text
        :return: int representing the number of sentences
        """
        return len(self.__sentences)

    def create_k_seqs(self) -> list[list[str | list[list[str]]]]:
        """
        Creates the K-Sequences output ready for write to json file
        :return: a list of lists to lists of K-sequences
        """
        try:
            res = []

            def process_sequences(seq_counts: dict[str, list[tuple[str, int]]]) -> list[list[str]]:
                """
                Processes the sequences and combines all sequences of varying lengths.
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

            idx_people = self.get_names_appearances_idx()
            for person in sorted(idx_people.keys()):
                sentences = [line for index, line in enumerate(self.__sentences) if index in idx_people[person]]  # add
                # all the lines with the index in it this name has appeared
                res.append([person, process_sequences(generate_k_seqs(sentences, self.__N))])  # add people with k seq
            return res
        except (FileNotFoundError, PermissionError, TypeError, Exception) as e:
            raise e("error")

    def write_to_json(self, filePath: typing.Union[os, str]) -> bool:
        """
        try to write to a json file the results of the class NamesCounter
        :param filePath: path to json file to save the results to
        :return: True if the file was successfully written, False otherwise
        """

        data = {
            f"Question {self.__question_number}": {
                "Person Contexts and K-Seqs": self.create_k_seqs()
            }
        }
        return writeTojsonFile(filePath, data)

    def return_results(self) -> str:
        """
        Return the results of the search of key to json file
        :return: string represent the results of the sequences in json format
        """
        try:
            data = {
                f"Question {self.__question_number}": {
                    "Person Contexts and K-Seqs": self.create_k_seqs()
                }
            }

            json_data = json.dumps(data, indent=4)
            return json_data
        except (FileNotFoundError, PermissionError, TypeError, Exception) as e:
            raise e("error")

    def get_names_appearances_idx(self) -> dict[str, list[int]]:
        """
        Returns a dictionary mapping each __data to a lines were they appeared
        :return: a dictionary mapping each __data to a lines were they appeared
        """
        try:
            name_counter = NamesCounter(5, preprocessed=self.__preprocessed,
                                        sentence_input_path=self.__sentence_input_path,
                                        remove_input_path=self.__remove_input_path,
                                        people_input_path=self.__people_input_path,
                                        json_input_path=self.__json_input_path)
            _, namesIdx = name_counter.count_names()
        except (FileNotFoundError, PermissionError, TypeError, Exception) as e:
            raise e("error")

        def remove_duplicates(data: dict[str, list[int]]) -> dict[str, list[int]]:
            """
            Removes duplicate values from the lists in the dictionary while maintaining the original order.
            """
            for key, values in data.items():
                data[key] = list(dict.fromkeys(values))  # Using dict.fromkeys to preserve order and remove duplicates
            return data

        return remove_duplicates(namesIdx)


if __name__ == "__main__":
    PeopleKAssocions1 = PeopleKAssociations(5,
                                            people_input_path="text_analyzer/2_examples/Q5_examples/example_1/people_small_1.csv",
                                            sentence_input_path="text_analyzer/2_examples/Q5_examples/example_1/sentences_small_1.csv",
                                            remove_input_path="text_analyzer/1_data/data/REMOVEWORDS.csv", N=3)
    PeopleKAssocions2 = PeopleKAssociations(5,
                                            people_input_path="text_analyzer/2_examples/Q5_examples/example_2/people_small_2.csv",
                                            sentence_input_path="text_analyzer/2_examples/Q5_examples/example_2/sentences_small_2.csv",
                                            remove_input_path="text_analyzer/1_data/data/REMOVEWORDS.csv", N=4)
    PeopleKAssocions3 = PeopleKAssociations(5,
                                            people_input_path="text_analyzer/2_examples/Q5_examples/example_3/people_small_3.csv",
                                            sentence_input_path="text_analyzer/2_examples/Q5_examples/example_3/sentences_small_3.csv",
                                            remove_input_path="text_analyzer/1_data/data/REMOVEWORDS.csv", N=5)
    PeopleKAssocions4 = PeopleKAssociations(5,
                                            people_input_path="text_analyzer/2_examples/Q5_examples/example_4/people_small_4.csv",
                                            sentence_input_path="text_analyzer/2_examples/Q5_examples/example_4/sentences_small_4.csv",
                                            remove_input_path="text_analyzer/1_data/data/REMOVEWORDS.csv", N=6)
    PeopleKAssocions5 = PeopleKAssociations(5,
                                            json_input_path="text_analyzer/2_examples/Q1_examples/example_1/Q1_result1.json",
                                            preprocessed=True, N=3)
    PeopleKAssocions6 = PeopleKAssociations(5,
                                            json_input_path="text_analyzer/2_examples/Q1_examples/example_2/Q1_result2.json",
                                            preprocessed=True, N=4)
    PeopleKAssocions7 = PeopleKAssociations(5,
                                            json_input_path="text_analyzer/2_examples/Q1_examples/example_3/Q1_result3.json",
                                            preprocessed=True, N=5)

    print(PeopleKAssocions1.get_sentences_len())
