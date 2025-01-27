import os
import sys
import typing
import json
from Preprocesser import Preprocessor


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
        :param json_input_path: file path for json input to get name from him (default value None)
        """
        self.__QNum = QNum
        self.__json_input_path = json_input_path
        self.__remove_input_path = remove_input_path
        self.__sentence_input_path = sentence_input_path
        self.__people_input_path = people_input_path
        self.__names = []
        self.__sentences = []
        try:
            if preprocessed:
                self.__load_json(self.__json_input_path)
            elif self.__remove_input_path is not None and self.__sentence_input_path is not None and self.__people_input_path is not None:
                self.__load_data(self.__sentence_input_path, self.__people_input_path, self.__remove_input_path)
            else:
                raise ValueError(
                    "either json_input_path or remove_input_path and sentence_input_path or people_input_path must be provided")
        except (FileNotFoundError, PermissionError, TypeError, Exception) as e:
            print(f"Error: {e}")  # Handle any file-related or other errors
            sys.exit(1)  # Exit program if there's an error

    def __load_json(self, json_file_path: typing.Union[str, os]) -> Exception | None:
        """
            Loads preprocessed data from a JSON file.
            :param json_file_path: Path to the preprocessed JSON file
            :time complicity = O(1) because the file is already preprocessed and therefore
             we just want to enter the data
            """
        try:
            with open(json_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Dynamically get the first key that matches 'Question' followed by a number
                question_key = next(key for key in data.keys() if key.lower().startswith('question'))
                # Extract __sentences from the dynamic question key
                self.__names = data.get(question_key, {}).get('Processed Names', [])
                self.__sentences = data.get(question_key, {}).get('Processed Sentences', [])
            # handle errors
        except FileNotFoundError:
            raise FileNotFoundError(f"FileNotFoundError: The file {json_file_path} was not found.")
        except json.JSONDecodeError:
            raise json.JSONDecodeError(f"JSONDecodeError: The file {json_file_path} is not a valid JSON file.")
        except PermissionError:
            raise PermissionError(f"PermissionError: Permission denied to read {json_file_path}.")
        except Exception as e:
            raise Exception(f"An error occurred while loading preprocessed data: {str(e)}")

    def __load_data(self, sentence_input_path: typing.Union[str, os], people_input_path: typing.Union[str, os],
                    remove_input_path: typing.Union[str, os]) -> None:
        """
        Loads __sentences and removes unwanted words based on the provided files.
        :param sentence_input_path: Path to the sentence input file
        :param people_input_path: Path to the people input file
        :param remove_input_path: Path to the file with words to remove
        :time complexity: O(n)
        """
        try:
            dataLoader = Preprocessor(1, sentenceInputPath=sentence_input_path, removeInputPath=remove_input_path,
                                      peopleInputPath=people_input_path)
            self.__sentences = dataLoader.getSentences()
            self.__names = dataLoader.get_people()
        except ValueError:
            raise
        except FileNotFoundError as e:
            raise FileNotFoundError("{0}".format(e))
        except PermissionError as e:
            raise PermissionError("{0}".format(e))
        except Exception as e:
            raise Exception("{0}".format(e))

    def build_names_dictionary(self) -> (dict[str, str], dict[str, bool]):
        """
        Builds the names dictionary based on the provided people list.
        :return: A tuple containing two dictionaries:
                 - A dictionary mapping individual words to the main name they belong to.
                 - A dictionary indicating whether the word has a partial match (True/False).
        :note: This function optimizes runtime by making name searches efficient (O(1) for each search).
        :time complexity: search = O(1), build = O(Len(names) * len(other names)).
        """
        mapToMain = {}
        have_conutnue = {}
        join_words = lambda words: ' '.join(words)  # lambda function
        for names in self.__names:
            value = join_words(names[0]).strip()  # creat the main name sequence
            for name in names[0]:
                if name not in mapToMain:  # map every part of main to the name mapper and add thim to a list
                    mapToMain[name] = [value]
                else:
                    if value not in mapToMain[name]:
                        mapToMain[name].append(value)
                have_conutnue[name] = False  # there is no need to the name to be continued to count
            for name in names[1]:  # add nick names to dictionary
                if join_words(name) in mapToMain:  # check member ship of nick name connected
                    if value not in mapToMain[join_words(name)]:# check if the main name in the res so we didnt count twice
                        mapToMain[join_words(name)].append(value)
                else:
                    mapToMain[join_words(name)] = [value]
                have_conutnue[join_words(name)] = False # set as have no continue
                res = ""
                for word in name[:-1]:
                    res += word
                    have_conutnue[res] = True # set every sub name of the nick name as have continue
                    res += " "
        return mapToMain, have_conutnue

    def count_names(self) -> (dict[str, int],dict[str,list[int]]):
        """
        Count the number of sentences that contain each name or part of a name from the names list.
        :param sentence_list: List of sentences, where each sentence is a list of words.
        :return: A dictionary where each key is a name/part and the value is the count of sentences
                 containing that name/part.
        """
        counter = {}
        names_appear_lines = {}
        join_words = lambda words: ' '.join(words).strip()  # lambda function
        mapToMain, have_conutnue = self.build_names_dictionary() # get the dictionary's that we have been built befor
        for index, sentence in enumerate(self.__sentences): # pass over the lines
            sentence_len = len(sentence)
            for pos in range(sentence_len):# search in the lines
                word = sentence[pos]
                if word in have_conutnue: # check if the word is member in the have continue
                    if have_conutnue[str(word)]: # if have a conitnue we search if the continue is the same
                        endIdx = 1
                        while endIdx + pos < sentence_len and join_words(sentence[pos:pos + endIdx]).strip() in have_conutnue and \
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
        try:
            with open(filePath, 'w', encoding='utf-8') as f:
                res = False
                names_counter, _ = self.count_names()
                data = {
                    f"Question {self.__QNum}": {
                        "Name Mentions": [[key, names_counter[key]] for key in names_counter.keys()]
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

    def get_names(self) -> list:
        """
        get the names list
        :return: list
        """
        return self.__names

    def get_sentences(self) -> list:
        """
        get the sentences list
        :return: list of sentences
        """
        return self.__sentences


if __name__ == '__main__':
    # names_counter = NamesCounter(3,people_input_path="text_analyzer/2_examples/Q3_examples/example_2/people_small_2.csv",sentence_input_path= "text_analyzer/2_examples/Q3_examples/example_2/sentences_small_2.csv",remove_input_path="text_analyzer/1_data/data/REMOVEWORDS.csv")
    # print(names_counter.count_names())
    NAMES_COUNTER1 = NamesCounter(3, json_input_path="text_analyzer/Q1_result1.json")
    NAMES_COUNTER2 = NamesCounter(3, json_input_path="text_analyzer/Q1_result2.json")
    NAMES_COUNTER3 = NamesCounter(3, json_input_path="text_analyzer/Q1_result3.json")
    NAMES_COUNTER4 = NamesCounter(3,
                                  people_input_path="text_analyzer/2_examples/Q3_examples/example_1/people_small_1.csv",
                                  sentence_input_path="Q2resEx1",
                                  remove_input_path="text_analyzer/1_data/data/REMOVEWORDS.csv")
    # print(NAMES_COUNTER4.build_names_dictionary())
    print(NAMES_COUNTER3.get_sentences())
