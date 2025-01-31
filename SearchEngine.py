import json
import os
import sys
import typing
from Parser import writeTojsonFile, process_sentence
from SequinceCounter import load_Sentences_names, load_data


class SearchEngine:
    def __init__(self, QNum: int, sentence_input_path: typing.Union[str, os.PathLike] = None,
                 remove_input_path: typing.Union[str, os.PathLike] = None,
                 jsonInputFile: typing.Union[str, os.PathLike] = None,
                 kSeqJson: typing.Union[str, os.PathLike] = None, preprocessed: bool = False):
        """
        Initializes the SearchEngine with necessary paths to input files for questions, __sentences, and k-sequences.
        """
        if not kSeqJson:
            raise ValueError("The kSeqJson path must be provided.")
        self.__QNum = QNum
        self.__sentence_input_path = sentence_input_path
        self.__remove_input_path = remove_input_path
        self.__jsonInputFile = jsonInputFile
        self.__kSeqJson = kSeqJson
        self.__kSeqData = self.__load_kseq_data()
        try:
            # Try to load k-seq data, and based on availability, load either JSON or raw data
            self.__load_kseq_data()
            if preprocessed:
                self.__sentences, self.__names = load_Sentences_names(
                    json_file_path=jsonInputFile)  # Load preprocessed JSON file
            elif sentence_input_path is not None or remove_input_path is not None:
                self.__sentences, self.__names = load_data(sentence_input_path,
                                                           remove_input_path)  # Load raw data from input files
            else:
                raise ValueError(
                    "Requires either jsonInputFile or sentence_input_path and remove_input_path to be availed")
        except (FileNotFoundError, PermissionError, TypeError, Exception,ValueError) as e:
            raise e(f"Error: {e}")  # Handle any file-related or other errors

    def __buildGenralDataBase(self):
        """"
        Builds the data base from a the supplied sentence
        time complexity : build O(lines_number * line_length**2)
        for search it tack O(1) in average case cause the data structure we use
        is hash dictionary
        """
        resDict = {}
        # Iterate through each sentence in the list
        for sentence in self.__sentences:  # O(len(sentence))
            # Iterate through all possible subsequences of the sentence
            for startIdx in range(len(sentence)):  # this and the sub is O(n**2)
                for finishIdx in range(startIdx + 1, len(sentence) + 1):
                    # Get the subsequence (either a string or a tuple)
                    sub_seq = tuple(sentence[startIdx:finishIdx])
                    # Check if the subsequence (as a string or tuple) already exists in the dictionary
                    if sub_seq not in resDict:  # check take O(1)
                        resDict[sub_seq] = [sentence]
                    else:
                        if sentence not in resDict[sub_seq]:
                            if sentence not in resDict[sub_seq]:
                                resDict[sub_seq].append(sentence)
        return resDict

    def search_in_supplied_text(self, data: list[str]) -> list[list[str]]:
        """
        Searches in the supplied text in o(1) complexity
        :note this function is not needed but this function is a general search function
        to search on full supplied text not only search keys
        :param data: list of sentences to search
        (this search if the supplied text in the text will return the lines were they found )
        :return: list of lines where each line is a sentence that contains the supplied text
        """
        searchDictionary = self.__buildGenralDataBase()
        if tuple(data) not in searchDictionary:
            return []
        else:
            return searchDictionary[tuple(data)]

    def __buildDataBaseForGivenKeys(self):
        """"
        Builds the database for the given keys
        time complexity : build O(lines_number * line_length**2)
        for search it tack O(1) in average case cause the data structure we use
        is hash dictionary tun time complexity : O(1)
        :return : dictionary with all the keys and their corresponding lines
        """
        resDict = {tuple(key): []for key in self.__kSeqData}
        # Iterate through each sentence in the list
        for sentence in self.__sentences:  # O(len(sentence))
            # Iterate through all possible subsequences of the sentence
            for startIdx in range(len(sentence)):  # this and the sub is O(n**2)
                for finishIdx in range(startIdx + 1, len(sentence) + 1):
                    # Get the subsequence (either a string or a tuple)
                    sub_seq = tuple(sentence[startIdx:finishIdx])
                    # Check if the subsequence (as a string or tuple) already exists in the dictionary
                    if sub_seq not in resDict:  # check take O(1)
                        continue
                    else:
                        if sentence not in resDict[sub_seq]:
                            resDict[sub_seq].append(sentence)
        return resDict

    def result_KseqData(self):
        """
        Builds the k-sequence based data
        :return : dictionary with all the keys that appeared and their corresponding lines
        """
        res = {}
        DataBase = self.__buildDataBaseForGivenKeys()
        for value in self.__kSeqData:
            sub_seq = tuple(value)
            if sub_seq in DataBase:
                res[sub_seq] = DataBase[sub_seq]
        # Sorting the dictionary by keys and the lists inside the keys
        sorted_res_dict = dict(sorted(res.items(), key=lambda item: item[0]))
        # Now, sort the lists inside each key
        for key in sorted_res_dict:
            sorted_res_dict[key] = sorted(sorted_res_dict[key], key=lambda x: x)
        return sorted_res_dict

    def write_to_json(self, filePath: typing.Union[os.PathLike, str]) -> bool:
        """
        Writes the sequence matches to a JSON file.
        :param filePath: path to the JSON file to save the results to
        :return: True if the file was successfully written, False otherwise
        """
        result_dict = {
            f"Question {self.__QNum}": {
                "K-Seq Matches": []
            }
        }

        # Prepare the data to be written
        for seq, sentences in self.result_KseqData().items():
            if not sentences:
                continue
            sequence_key = ' '.join(seq)  # Convert tuple to string for the key
            result_dict[f"Question {self.__QNum}"]["K-Seq Matches"].append([
                sequence_key,  # The sequence as a string
                sentences  # The list of __sentences that match the sequence
            ])
        return writeTojsonFile(filePath, result_dict)

    def return_results(self) -> str:
        """
        Return the results of the search of key to json file
        :return: string represent the results of the sequences in json format
        """
        result_dict = {
            f"Question {self.__QNum}": {
                "K-Seq Matches": []
            }
        }
        # Prepare the data to be written
        for seq, sentences in self.result_KseqData().items():
            if not sentences:
                continue
            sequence_key = ' '.join(seq)  # Convert tuple to string for the key
            result_dict[f"Question {self.__QNum}"]["K-Seq Matches"].append([
                sequence_key,  # The sequence as a string
                sentences  # The list of __sentences that match the sequence
            ])
        json_data = json.dumps(result_dict, indent=4)
        return json_data

    def __load_kseq_data(self) -> list[list[str]]:
        """
        Loads k-sequence data from a JSON file and processes it by cleaning up words and removing punctuation.
        :return: A list of cleaned sentences (as lists of words)
        """
        try:
            # Open the file and load its content
            with open(self.__kSeqJson, 'r', encoding='utf-8') as f:
                data = json.load(f)  # Load the data from the JSON file
                keys = data.get('keys', [])  # Extract the 'keys' field
                availedData = []  # List to store cleaned __sentences

                # Clean each sentence by processing the words
                for sentence in keys:
                    # Clean each word in the sentence by removing punctuation and extra spaces
                    cleaned_sentence = [process_sentence(word) for word in sentence if word.strip()]
                    if cleaned_sentence:
                        availedData.append(cleaned_sentence)  # Add cleaned sentence to the result list
        except FileNotFoundError:
            raise FileNotFoundError(f"The file {self.__kSeqJson} was not found.")
        except json.JSONDecodeError:
            raise json.JSONDecodeError(
                f"The file {self.__kSeqJson} is not a valid JSON file.")  # Error if JSON is invalid
        except PermissionError:
            raise PermissionError(f"Permission denied to read {self.__kSeqJson}.")  # Handle permission issues
        except Exception as e:
            raise Exception(
                f"An error occurred while loading preprocessed data: {str(e)}")  # Catch any other unexpected errors

        return availedData  # Return the cleaned k-sequences




if __name__ == "__main__":
    searchEngine1 = SearchEngine(4,
                                 sentence_input_path="text_analyzer/2_examples/Q4_examples/example_1/sentences_small_1.csv",
                                 remove_input_path="text_analyzer/1_data/Data/REMOVEWORDS.csv",
                                 kSeqJson="text_analyzer/2_examples/Q4_examples/example_1/kseq_query_keys_1.json")

    searchEngine2 = SearchEngine(4,
                                 sentence_input_path="text_analyzer/2_examples/Q4_examples/example_2/sentences_small_2.csv",
                                 remove_input_path="text_analyzer/1_data/Data/REMOVEWORDS.csv",
                                 kSeqJson="text_analyzer/2_examples/Q4_examples/example_2/kseq_query_keys_2.json")

    searchEngine3 = SearchEngine(4,
                                 sentence_input_path="text_analyzer/2_examples/Q4_examples/example_3/sentences_small_3.csv",
                                 remove_input_path="text_analyzer/1_data/Data/REMOVEWORDS.csv",
                                 kSeqJson="text_analyzer/2_examples/Q4_examples/example_3/kseq_query_keys_3.json")

    searchEngine4 = SearchEngine(4,
                                 sentence_input_path="text_analyzer/2_examples/Q4_examples/example_4/sentences_small_4.csv",
                                 remove_input_path="text_analyzer/1_data/Data/REMOVEWORDS.csv",
                                 kSeqJson="text_analyzer/2_examples/Q4_examples/example_4/kseq_query_keys_4.json")

    searchEngine5 = SearchEngine(4, jsonInputFile="text_analyzer/2_examples/Q1_examples/example_1/Q1_result1.json",
                                 preprocessed=True,
                                 kSeqJson="text_analyzer/2_examples/Q4_examples/example_1/kseq_query_keys_1.json")

    searchEngine6 = SearchEngine(4, jsonInputFile="text_analyzer/2_examples/Q1_examples/example_2/Q1_result2.json",
                                 preprocessed=True,
                                 kSeqJson="text_analyzer/2_examples/Q4_examples/example_2/kseq_query_keys_2.json")

    searchEngine7 = SearchEngine(4, jsonInputFile="text_analyzer/2_examples/Q1_examples/example_3/Q1_result3.json",
                                 preprocessed=True,
                                 kSeqJson="text_analyzer/2_examples/Q4_examples/example_3/kseq_query_keys_3.json")

    # print(searchEngine4.write_to_json("q4_result1.json"))
