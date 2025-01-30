import os
import sys
import typing
from Parser import writeTojsonFile
from Parser import Parser
from SequinceCounter import load_Sentences_names, load_data


class NamesCounter:
    def __init__(self, QNum: int, sentence_input_path: typing.Union[str, os.PathLike] = None,
                 remove_input_path: typing.Union[str, os.PathLike] = None,
                 people_input_path: typing.Union[str, os.PathLike] = None,
                 json_input_path: typing.Union[str, os.PathLike] = None, preprocessed: bool = False):
        """
        constructor for NamesCounter
        :param QNum: the number of questions to get printed into json file
        :param sentence_input_path: file path for sentence input(default value None)
        :param remove_input_path: file path for sentence input after preprocessing and removing(default value None)
        :param people_input_path: path for people input  (default value None)
        :param json_input_path: file path for json input to get __data from him (default value None)
        """
        self.__QNum = QNum
        self.__json_input_path = json_input_path
        self.__remove_input_path = remove_input_path
        self.__sentence_input_path = sentence_input_path
        self.__people_input_path = people_input_path
        try:
            if preprocessed:
                self.__sentences, self.__names = load_Sentences_names(self.__json_input_path)
            elif self.__remove_input_path is not None and self.__sentence_input_path is not None and self.__people_input_path is not None:
                self.__sentences, self.__names = load_data(self.__sentence_input_path,
                                                           self.__remove_input_path, self.__people_input_path)
            else:
                raise ValueError(
                    "either json_input_path or remove_input_path and sentence_input_path or people_input_path must be provided")
        except (FileNotFoundError, PermissionError, TypeError, Exception) as e:
            raise e(f"Error: {e}")  # Handle any file-related or other errors


    def build_names_dictionary(self) -> (dict[str, str], dict[str, bool]):
        """
        Builds the names dictionary based on the provided people list.
        :return: A tuple containing two dictionaries:
                 - A dictionary mapping individual words to the main __data they belong to.
                 - A dictionary indicating whether the word has a partial match (True/False).
        :note: This function optimizes runtime by making __data searches efficient (O(1) for each search).
        :time complexity: search = O(1), build = O(Len(names) * len(other names)).
        """
        mapToMain = {}
        join_words = lambda words: ' '.join(words).strip()  # lambda function

        for names in self.__names:
            value = join_words(names[0]).strip()  # create the main __data sequence

            for name in names[0]:
                # Join the characters in name to form a single string (word)
                word = ''.join(name)
                mapToMain[word] = [value]  # Use the word string as the key

            for name in names[1]:  # add nicknames to dictionary
                word = ' '.join(name)  # Join the characters of the nickname
                if word in mapToMain:  # check if the word exists in the dictionary
                    if value not in mapToMain[word]:  # avoid adding duplicates
                        mapToMain[word].append(value)
                else:
                    mapToMain[word] = [value]  # add the nickname as a new key

        return mapToMain

    def count_names(self) -> (dict[str, int], dict[str, list[int]]):
        """
        Count the number of __sentences that contain each __data or part of a __data from the names list.
        :return: A dictionary where each key is a __data/part and the value is the count of __sentences
                 containing that __data/part.
        """
        counter = {}
        names_appear_lines = {}
        mapToMain = self.build_names_dictionary()  # get the dictionary's that we have been built befor
        for index, sentence in enumerate(self.__sentences):  # pass over the lines
            sentence_len = len(sentence)
            for startIdx in range(sentence_len):
                for endIdx in range(startIdx+1,sentence_len+1):
                    check_name = ' '.join(sentence[startIdx:endIdx])
                    if check_name in mapToMain:
                        for name in mapToMain[check_name]:
                            counter[name] = counter.get(name,0)+1
                            if name in names_appear_lines:
                                names_appear_lines[name].append(index)
                            else:
                                names_appear_lines[name] = [index]
        return counter, names_appear_lines

    def write_to_json(self, filePath: typing.Union[os, str]) -> bool:
        """
        try to write to a json file the results of the class NamesCounter
        :param filePath: path to json file to save the results to
        :return: True if the file was successfully written, False otherwise
        """
        names_counter, _ = self.count_names()
        data = {
            f"Question {self.__QNum}": {
                "Name Mentions": sorted([[key, names_counter[key]] for key in names_counter.keys()])
            }
        }
        return writeTojsonFile(filePath, data)

    def get_names(self) -> list[list[str]]:
        """
        get the names list
        :return: list of
        """
        return self.__names

    def get_sentences(self) -> list[list[list[str]]]:
        """
        get the __sentences list
        :return: list of __sentences
        """
        return self.__sentences


if __name__ == '__main__':
    # names_counter = NamesCounter(3,people_input_path="text_analyzer/2_examples/Q3_examples/example_2/people_small_2
    # .csv",sentence_input_path= "text_analyzer/2_examples/Q3_examples/example_2/sentences_small_2.csv",
    # remove_input_path="text_analyzer/1_data/data/REMOVEWORDS.csv") print(names_counter.count_names())

    # NAMES_COUNTER1 = NamesCounter(3, json_input_path="text_analyzer/Q1_result1.json", preprocessed=True)
    # NAMES_COUNTER2 = NamesCounter(3, json_input_path="text_analyzer/Q1_result2.json", preprocessed=True)
    # NAMES_COUNTER3 = NamesCounter(3, json_input_path="text_analyzer/Q1_result3.json", preprocessed=True)
    NAMES_COUNTER4 = NamesCounter(3,
                                  people_input_path="text_analyzer/2_examples/Q3_examples/example_1/people_small_1.csv",
                                  remove_input_path="text_analyzer/1_data/data/REMOVEWORDS.csv",
                                  sentence_input_path="text_analyzer/2_examples/Q3_examples/example_1/sentences_small_1.csv")
    NAMES_COUNTER5 = NamesCounter(3,
                                  people_input_path="text_analyzer/2_examples/Q3_examples/example_2/people_small_2.csv",
                                  remove_input_path="text_analyzer/1_data/data/REMOVEWORDS.csv",
                                  sentence_input_path="text_analyzer/2_examples/Q3_examples/example_2/sentences_small_2.csv")
    NAMES_COUNTER6 = NamesCounter(3,
                                  people_input_path="text_analyzer/2_examples/Q3_examples/example_3/people_small_3.csv",
                                  remove_input_path="text_analyzer/1_data/data/REMOVEWORDS.csv",
                                  sentence_input_path="text_analyzer/2_examples/Q3_examples/example_3/sentences_small_3.csv")
    NAMES_COUNTER7 = NamesCounter(3,
                                  people_input_path="text_analyzer/2_examples/Q3_examples/example_4/people_small_4.csv",
                                  remove_input_path="text_analyzer/1_data/data/REMOVEWORDS.csv",
                                  sentence_input_path="text_analyzer/2_examples/Q3_examples/example_4/sentences_small_4.csv")

    print(NAMES_COUNTER4.count_names())
