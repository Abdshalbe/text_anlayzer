import json
import sys
import re
import typing
import os
from Preprocesser import Preprocessor

class SearchEngine:
    def __init__(self, QNum: int, sentence_input_path: typing.Union[str, os.PathLike] = None,
                 remove_input_path: typing.Union[str, os.PathLike] = None, jsonInputFile: typing.Union[str, os.PathLike] = None,
                 kSeqJson: typing.Union[str, os.PathLike] = None,preprocessed: bool = False):
        """
        Initializes the SearchEngine with necessary paths to input files for questions, sentences, and k-sequences.
        """
        self.__QNum = QNum
        self.__sentence_input_path = sentence_input_path
        self.__remove_input_path = remove_input_path
        self.__jsonInputFile = jsonInputFile
        self.__kSeqJson = kSeqJson
        self.__sentences:list[list[str]] = []
        self.__kSeqData = []
        try:
            # Try to load k-seq data, and based on availability, load either JSON or raw data
            self.loadKseqData()
            if preprocessed:
                self.__load_json_to_sentence()  # Load preprocessed JSON file
            elif sentence_input_path is not None or remove_input_path is not None:
                self.__load_data_by_path()  # Load raw data from input files
            else:
                raise Exception("Requires either jsonInputFile or sentence_input_path and remove_input_path to be availed")
        except (FileNotFoundError, PermissionError, TypeError, Exception) as e:
            print(f"Error: {e}")  # Handle any file-related or other errors
            sys.exit(1)  # Exit program if there's an error

    def buildDataBase(self):
        """"
        Builds the data base from a the supplied sentence
        time complexity : build O(lines_number * line_length**2)
        for search it tack O(1) in average case cause the data structure we use
        is hash dictionary
        """
        resDict = {}
        # Iterate through each sentence in the list
        for sentence in self.__sentences: #O(len(sentence))
            # Iterate through all possible subsequences of the sentence
            for startIdx in range(len(sentence)): # this and the sub is O(n**2)
                for finishIdx in range(startIdx + 1, len(sentence) + 1):
                    # Get the subsequence (either a string or a tuple)
                    sub_seq = tuple(sentence[startIdx:finishIdx])
                    # Check if the subsequence (as a string or tuple) already exists in the dictionary
                    if sub_seq not in resDict: # check take O(1)
                        resDict[sub_seq] = [sentence]
                    else:
                        if sentence not in resDict[sub_seq] :
                            resDict[sub_seq].append(sentence)
        return resDict

    def buildKseqData(self):
        """
        Builds the k-sequence based data

        """
        res = {}
        DataBase = self.buildDataBase()
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
        try:
            with open(filePath, 'w', encoding='utf-8') as f:
                # Create the result dictionary for the "K-Seq Matches"
                result_dict = {
                    f"Question {self.__QNum}": {
                        "K-Seq Matches": []
                    }
                }

                # Prepare the data to be written
                for seq, sentences in self.buildKseqData().items():
                    sequence_key = ' '.join(seq)  # Convert tuple to string for the key
                    result_dict[f"Question {self.__QNum}"]["K-Seq Matches"].append([
                        sequence_key,  # The sequence as a string
                        sentences  # The list of sentences that match the sequence
                    ])

                # Write to the JSON file
                json.dump(result_dict, f, ensure_ascii=False, indent=4)
                return True
        except FileNotFoundError:
            print(f"FileNotFoundError: The path {filePath} was not found.")
        except PermissionError:
            print(f"PermissionError: Permission denied to write to {filePath}.")
        except IOError as e:
            print(f"IOError: An error occurred while writing to {filePath}. Error: {str(e)}")
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")
        return False

    def __load_data_by_path(self):
        """
        Loads raw sentences and names from input files, removing unwanted words as per the remove input file.
        """
        try:
            dataLoader = Preprocessor(1, sentenceInputPath=self.__sentence_input_path, removeInputPath=self.__remove_input_path)
            self.__sentences = dataLoader.getSentences()  # Get processed sentences
            self.__names = dataLoader.get_people()  # Get list of names
        except ValueError:
            raise ValueError("Invalid value provided during data loading.")
        except FileNotFoundError as e:
            raise FileNotFoundError(f"File not found: {e}")
        except PermissionError as e:
            raise PermissionError(f"Permission denied: {e}")
        except Exception as e:
            raise Exception(f"An error occurred while loading data: {str(e)}")
    def loadKseqData(self):
        """
        Loads k-sequence data from a JSON file and processes it by cleaning up words and removing punctuation.
        """
        try:
            with open(self.__kSeqJson, 'r', encoding='utf-8') as f:
                data = json.load(f)  # Load the data from the JSON file
                keys = data.get('keys', [])  # Extract the 'keys' field
                vailedData = []  # List to store cleaned sentences
                for sentence in keys:
                    # Clean each word in the sentence by removing punctuation and extra spaces
                    cleaned_sentence = [re.sub(r'[^\w\s]', '', word.strip().lower()) for word in sentence if word.strip()]
                    if cleaned_sentence:
                        vailedData.append(cleaned_sentence)  # Add cleaned sentence to the result list
            self.__kSeqData = vailedData  # Save cleaned k-sequence data
        except FileNotFoundError:
            raise FileNotFoundError(f"The file {self.__kSeqJson} was not found.")  # Raise specific error if file is not found
        except json.JSONDecodeError:
            raise json.JSONDecodeError(f"The file {self.__kSeqJson} is not a valid JSON file.")  # Error if JSON is invalid
        except PermissionError:
            raise PermissionError(f"Permission denied to read {self.__kSeqJson}.")  # Handle permission issues
        except Exception as e:
            raise Exception(f"An error occurred while loading preprocessed data: {str(e)}")  # Catch any other unexpected errors
    def __load_json_to_sentence(self):
        """
        Loads preprocessed data from a given JSON file and extracts the sentences.
        """
        try:
            with open(self.__jsonInputFile, 'r', encoding='utf-8') as f:
                data = json.load(f)
                question_key = next(key for key in data.keys() if key.lower().startswith('question'))
                self.__sentences = data.get(question_key, {}).get('Processed Sentences', [])  # Extract processed sentences
        except FileNotFoundError:
            raise FileNotFoundError(f"The file {self.__jsonInputFile} was not found.")
        except json.JSONDecodeError:
            raise json.JSONDecodeError(f"The file {self.__jsonInputFile} is not a valid JSON file.")
        except PermissionError:
            raise PermissionError(f"Permission denied to read {self.__jsonInputFile}.")
        except Exception as e:
            raise Exception(f"An error occurred while loading preprocessed data: {str(e)}")


if __name__ == "__main__":
    searchEngine = SearchEngine(4, jsonInputFile="text_analyzer/Q1_result1.json", kSeqJson="text_analyzer/2_examples/Q4_examples/example_1/kseq_query_keys_1.json")
    print(searchEngine.write_to_json("text_analyzer/Q4_result1.json"))
    # print(tuple(["str","hello"]))