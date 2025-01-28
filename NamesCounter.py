import os
import sys
import typing
from Preprocesser import writeTojsonFile
from Preprocesser import Preprocessor
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
            print(f"Error: {e}")  # Handle any file-related or other errors
            sys.exit(1)

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
        have_conutnue = {}
        join_words = lambda words: ' '.join(words)  # lambda function
        for names in self.__names:
            value = join_words(names[0]).strip()  # creat the main __data sequence
            for name in names[0]:
                if name not in mapToMain:  # map every part of main to the __data mapper and add thim to a list
                    mapToMain[name] = [value]
                else:
                    if value not in mapToMain[name]:
                        mapToMain[name].append(value)
                have_conutnue[name] = False  # there is no need to the __data to be continued to count
            for name in names[1]:  # add nicknames to dictionary
                if join_words(name) in mapToMain:  # check membership of nick __data connected
                    if value not in mapToMain[
                        join_words(name)]:  # check if the main __data in the res so we didnt count twice
                        mapToMain[join_words(name)].append(value)
                else:
                    mapToMain[join_words(name)] = [value]
                have_conutnue[join_words(name)] = False  # set as have no continue
                res = ""
                for word in name[:-1]:
                    res += word
                    have_conutnue[res] = True  # set every sub __data of the nick __data as have continue
                    res += " "
        return mapToMain, have_conutnue

    def count_names(self) -> (dict[str, int], dict[str, list[int]]):
        """
        Count the number of __sentences that contain each __data or part of a __data from the names list.
        :return: A dictionary where each key is a __data/part and the value is the count of __sentences
                 containing that __data/part.
        """
        counter = {}
        names_appear_lines = {}
        join_words = lambda words: ' '.join(words).strip()  # lambda function
        mapToMain, have_conutnue = self.build_names_dictionary()  # get the dictionary's that we have been built befor
        for index, sentence in enumerate(self.__sentences):  # pass over the lines
            sentence_len = len(sentence)
            for pos in range(sentence_len):  # search in the lines
                word = sentence[pos]
                if word in have_conutnue:  # check if the word is member in the have continue
                    if have_conutnue[str(word)]:  # if have a conitnue we search if the continue is the same
                        endIdx = 1
                        while endIdx + pos < sentence_len and join_words(
                                sentence[pos:pos + endIdx]).strip() in have_conutnue and \
                                have_conutnue[join_words(sentence[pos:pos + endIdx]).strip()]:
                            if join_words(sentence[pos:pos + endIdx + 1]).strip() in mapToMain:
                                for key in mapToMain[join_words(sentence[pos:pos + endIdx + 1])]:
                                    counter[str(key)] = counter.get(str(key), 0) + 1
                                    if key in names_appear_lines:
                                        names_appear_lines[key].append(index)
                                    else:
                                        names_appear_lines[key] = [index]
                                break
                            else:
                                endIdx += 1
                    else:
                        if str(word) in mapToMain:
                            for key in mapToMain[str(word)]:
                                counter[str(key)] = counter.get(str(key), 0) + 1
                                if key in names_appear_lines:
                                    names_appear_lines[key].append(index)
                                else:
                                    names_appear_lines[key] = [index]
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

    print(NAMES_COUNTER7.get_names())
