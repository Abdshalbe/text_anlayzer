import os
import sys
import typing

from NamesCounter import NamesCounter
from Parser import writeTojsonFile
from SequinceCounter import generate_k_seqs, load_Sentences_names, load_data


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
                self.__sentences, self.__names = load_Sentences_names(json_input_path)
            else:
                self.__sentences, self.__names = load_data(sentence_input_path=sentence_input_path,remove_input_path= remove_input_path,people_input_path=people_input_path)
        except (FileNotFoundError, PermissionError, TypeError, Exception) as e:
            print(f"Error: {e}")  # Handle any file-related or other errors
            sys.exit(1)  # Exit program if there's an error

    def get_sentences_len(self) -> int:
        return len(self.__sentences)


    def create_k_seqs(self) -> list[list[str | list[list[str]]]]:
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

        idx_people = self.get_names_appearances_idx()
        for person in sorted(idx_people.keys()):
            sentences = [line for index, line in enumerate(self.__sentences) if index in idx_people[person]]
            res.append([person, process_sequences(generate_k_seqs(sentences, self.__N))])
        return res

    def write_to_json(self, filePath: typing.Union[os, str]) -> bool:
        """
        try to write to a json file the results of the class NamesCounter
        :param filePath: path to json file to save the results to
        :return: True if the file was successfully written, False otherwise
        """

        data = {
            f"Question {self.__qustion_number}": {
                "Person Contexts and K-Seqs": self.create_k_seqs()
            }
        }
        return writeTojsonFile(filePath, data)

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



if __name__ == "__main__":

    PeopleKAssocions1 = PeopleKAssocions(5,
                                         people_input_path="text_analyzer/2_examples/Q5_examples/example_1/people_small_1.csv",
                                         sentence_input_path="text_analyzer/2_examples/Q5_examples/example_1/sentences_small_1.csv",
                                         remove_input_path="text_analyzer/1_data/data/REMOVEWORDS.csv", N=3)
    PeopleKAssocions2 = PeopleKAssocions(5,
                                         people_input_path="text_analyzer/2_examples/Q5_examples/example_2/people_small_2.csv",
                                         sentence_input_path="text_analyzer/2_examples/Q5_examples/example_2/sentences_small_2.csv",
                                         remove_input_path="text_analyzer/1_data/data/REMOVEWORDS.csv", N=4)
    PeopleKAssocions3 = PeopleKAssocions(5,
                                         people_input_path="text_analyzer/2_examples/Q5_examples/example_3/people_small_3.csv",
                                         sentence_input_path="text_analyzer/2_examples/Q5_examples/example_3/sentences_small_3.csv",
                                         remove_input_path="text_analyzer/1_data/data/REMOVEWORDS.csv", N=5)
    PeopleKAssocions4 = PeopleKAssocions(5,
                                         people_input_path="text_analyzer/2_examples/Q5_examples/example_4/people_small_4.csv",
                                         sentence_input_path="text_analyzer/2_examples/Q5_examples/example_4/sentences_small_4.csv",
                                         remove_input_path="text_analyzer/1_data/data/REMOVEWORDS.csv", N=6)
    PeopleKAssocions5 = PeopleKAssocions(5,json_input_path="text_analyzer/2_examples/Q1_examples/example_1/Q1_result1.json",preprocessed=True, N=3)
    PeopleKAssocions6 = PeopleKAssocions(5,json_input_path="text_analyzer/2_examples/Q1_examples/example_2/Q1_result2.json",preprocessed=True, N=4)
    PeopleKAssocions7 = PeopleKAssocions(5,json_input_path="text_analyzer/2_examples/Q1_examples/example_3/Q1_result3.json",preprocessed=True, N=5)

    print(PeopleKAssocions1.get_sentences_len())
