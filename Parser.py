import csv
import json
import os
import string
import typing


# static method she will be shared for all objects so it more memory efficient
def hash_dict_for_punctuation() -> typing.Dict[str, str]:
    """
    Build a dictionary of punctuation characters mapped to "" and letters to lowercase.
    the distention of this dictionary is make replace all letter with the appropriate letters
    :return dict with punctuation characters mapped to "" and letters to lower letter
    """
    # starting hash map
    mapping_hash_map = {}
    for char in range(ord('a'), ord('z') + 1):
        mapping_hash_map[chr(char)] = chr(char)
    for char in range(ord('A'), ord('Z') + 1):
        mapping_hash_map[chr(char)] = chr(char).lower()
    for char in range(ord('A')):
        mapping_hash_map[chr(char)] = ' '
    for char in range(ord('Z') + 1, ord('a')):
        mapping_hash_map[chr(char)] = ' '
    for char in range(ord('z') + 1, 256):
        mapping_hash_map[chr(char)] = ' '
    for char in range(ord('0'), ord('9') + 1):
        mapping_hash_map[chr(char)] = chr(char)
    mapping_hash_map['\n'] = '\n'
    mapping_hash_map['\t'] = '\t'
    return mapping_hash_map


def process_sentence(sentence: str) -> str:
    """
    Process the sentence by converting it to lowercase, removing punctuation,
    and replacing punctuation with whitespace.

    :param sentence: The sentence to be processed
    :return: The processed sentence
    Time complexity: O(len(sentence))
    """

    # Early return for empty string
    if not sentence:
        return sentence

    # Dictionary for punctuation replacement (you can adjust this if needed)
    helperDict = {punc: ' ' for punc in string.punctuation}  # Map punctuation to whitespace

    # Initialize the new sentence with the first character
    new_sentence = ''

    # Process each character in the sentence
    for i, char in enumerate(sentence):
        # Convert uppercase to lowercase and handle punctuation
        if char in helperDict:
            newChar = helperDict[char]  # Replace punctuation with space
        else:
            newChar = char.lower()  # Convert the character to lowercase
        # Prevent consecutive spaces in the sentence
        if newChar == ' ' and (new_sentence.endswith(' ') or not new_sentence):
            continue
        new_sentence += newChar

    return new_sentence.strip()


def convert_to_nested_format(input_dict: dict[str:list[str]]) -> list[list[str]]:
    """
    Converts the input dictionary an appropriate format for the json file
    :param input_dict: dictionary to be converted
    :return: list of dictionaries
    :time complexity: o(len(keys)*len(values))
    """
    result = []
    for mainName, names in input_dict.items():
        subRes = []
        # Split the key into its components and make sure we wrap them in the desired format
        main_names = mainName.split()
        # Add the main __names and any nicknames
        subRes.append(main_names)
        other_names = []
        for name in names:
            if name != "":
                other_names.append(name.split())
        subRes.append(other_names)
        result.append(subRes)
    return result


def writeTojsonFile(filePath: str | os.PathLike, data: typing.Any) -> bool:
    """
    Writes the file to the json file with the given path
    :param data:
    :param filePath: os path where the file is to be written
    :return:
    """
    try:
        with open(filePath, 'w', encoding='utf-8') as f:
            # Try to write the data to the file
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"File {filePath} written successfully.")
    except (FileNotFoundError, PermissionError, IOError) as e:
        # Handle file errors
        print(f"Failed to open or write to the file {filePath}. Error: {str(e)}")
        return False
    return True


def validate_file_path(file_path: str, description: str) -> str:
    """
    Check if the file_path is a non-empty string
    :param description:
    :param file_path: Path to the file to be checked
    :return: the path of the file after checked
    :note : this is a private function that is not contained in the class API
    :throws ValueError: if the file_path is not string or os path
    time complexity : O(1)
    """
    if not isinstance(file_path, str) or not file_path.strip():
        raise ValueError(f"{description} must be a non-empty string.")
    # Check if the file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{description} does not exist: {file_path}")
    # Check if the file is readable
    if not os.access(file_path, os.R_OK):
        raise PermissionError(f"{description} is not readable: {file_path}")
    return file_path


class Parser:
    """
    Parser class to preprocess the text and return it as required.
    """

    def __init__(self, QuestionNumber: int, sentenceInputPath: typing.Union[str, os.PathLike],
                 removeInputPath: typing.Union[str, os.PathLike],
                 peopleInputPath: typing.Union[str, os.PathLike] = None):
        """
        class constructor for Parser
        :param QuestionNumber: a number of the question being processed to print in the file
        :param sentenceInputPath:
        :param peopleInputPath:
        :param removeInputPath:
        """
        try:
            self.__PeopleInputPath = None
            self.__SentenceInputPath = validate_file_path(sentenceInputPath, "Sentence Input Path")
            if peopleInputPath is not None:
                self.__PeopleInputPath = validate_file_path(peopleInputPath, "People Input Path")
            self.__RemoveInputPath = validate_file_path(removeInputPath, "Remove Input Path")
        except (FileNotFoundError, PermissionError, TypeError, Exception) as e:
            raise e(f"Error: {e}")  # Handle any file-related or other errors
        self.__QuestionNumber = QuestionNumber
        # Initialize Removals dictionary before processing __sentences
        processedWords = [sentence for sentence in
                          self.__read_csv_to_list(self.__RemoveInputPath)]
        self.__Removes = {key: True for key in processedWords}  # hash dictionary time complicity O(1) when when
        # check membership
        # Process __sentences after __Removes has been initialized
        self.__Sentences = [self.__removeUnwantedWords(process_sentence(line)).split() for line in
                            self.__read_csv_to_list(self.__SentenceInputPath) if
                            len(self.__removeUnwantedWords(process_sentence(line)).split()) > 0]
        # Build the people dictionary after the __sentences and removals are set
        self.__People = self.__buildPeopleDict()

    def __removeUnwantedWords(self, sentence: str) -> str:
        """
        Remove unwanted words from the sentence inout
        :param sentence: sentence to be processed
        :return: the processed sentence after removing unwanted words
        time complexity : O(len(sentence))
        :note : this is a private function that is not contained in the class API
        """
        resSentence = ""
        for word in sentence.split():
            # Ensure self.__Removes exists and has been properly initialized
            if word not in self.__Removes:
                resSentence += f"{word} "
        return resSentence.strip()

    @staticmethod
    def __read_csv_to_list(file_path: str) -> list[str]:
        """
        Read the CSV file into a list of strings representing the lines of the file
        :param file_path: str path to the CSV file to be read
        :return: list of strings representing the lines of the CSV file
        time complexity : O(file lines)
        :note : this is a private function that is not contained in the class API
        """
        lines = []
        rowCounter = 0
        with open(file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                # Join the elements of the row into a single string and append it to the list
                if rowCounter == 0:
                    rowCounter += 1
                else:
                    lines.append(','.join(row))
        return lines

    def __buildPeopleDict(self) -> dict[str:list[str]]:
        """
        Builds the people dictionary from the input file with main __names and nicknames
        :return: dictionary with main __names as keys and list of nicknames as values
        time complexity : O(lineNumbers * numberOfNicknames)
        :note : this is a private function that is not contained in the class API
        """
        namesDict = {}
        if self.__PeopleInputPath is None:
            return {}
        peopleList = self.__readPeopleFile(self.__PeopleInputPath)
        for person in peopleList:
            mainName = self.__removeUnwantedWords(process_sentence(person[0]))
            if mainName not in namesDict and mainName != "":
                namesDict[mainName] = []
                nickNames = person[1].split(",")
                for nickName in nickNames:
                    if len(nickName) == 0:
                        continue
                    if self.__removeUnwantedWords(process_sentence(nickName)) != "":
                        namesDict[mainName].append(self.__removeUnwantedWords(process_sentence(nickName)))
            else:
                continue
        return namesDict

    @staticmethod
    def __readPeopleFile(filePath: str) -> list:
        """
        Reads the file and returns a list with all the lines in the file
        :param filePath: input file path of the file to be read
        :return: list of lines in the file
        time complexity : O(lineNumerOfRows)
        :note : this is a private function that is not contained in the class API
        """
        resList = []
        rowCounter = 0
        with open(filePath, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if rowCounter == 0:
                    rowCounter += 1
                else:
                    if row == '':  # Skip empty rows
                        pass
                    resList.append(row)
        return resList

    def write_result_to_json(self, filePath: str) -> bool:
        data = {
            "Question 1": {
                "Processed Sentences": self.__Sentences,
                "Processed Names": convert_to_nested_format(self.__People)
            }
        }
        if writeTojsonFile(filePath, data):
            return True
        else:
            return False

    def return_results(self) -> str:
        """
        returns a dictionary with all the results of the question 1
        :return: string with all the results of the question 1 as needed
        """
        data = {
            "Question 1": {
                "Processed Sentences": self.__Sentences,
                "Processed Names": convert_to_nested_format(self.__People)
            }
        }
        json_data = json.dumps(data, indent=4)
        return json_data

    def getSentences(self) -> list[list[str]]:
        """
        Returns a list of lists every sublist represent
        a line after processing and remove word
        :return : a list of lists every sublist represent a list of words
        : note this function is public and in the API
        """
        return self.__Sentences

    def get_people(self) -> list[list[str]]:
        """
        A dictionary representing the people and their other __names
        :return: dictionary of the people and their other __names after processing
        """
        return convert_to_nested_format(self.__People)

    def get_remove_words(self) -> dict[str, bool]:
        """
        A dictionary representing the words to remove mapped to True (not necessary value)
        :return: a dictionary of the words to remove mapped to True
        """
        return self.__Removes


if __name__ == '__main__':
    preprocessor_1 = Parser(1,
                            peopleInputPath="text_analyzer/2_examples/Q1_examples/example_1/people_small_1.csv",
                            sentenceInputPath="text_analyzer/2_examples/Q1_examples/example_1/sentences_small_1.csv",
                            removeInputPath="text_analyzer/1_data/Data/REMOVEWORDS.csv")
    preprocessor_2 = Parser(1,
                            peopleInputPath="text_analyzer/2_examples/Q1_examples/example_2/people_small_2.csv",
                            sentenceInputPath="text_analyzer/2_examples/Q1_examples/example_2/sentences_small_2.csv",
                            removeInputPath="text_analyzer/1_data/Data/REMOVEWORDS.csv")
    preprocessor_3 = Parser(1,
                            peopleInputPath="text_analyzer/2_examples/Q1_examples/example_3/people_small_3.csv",
                            sentenceInputPath="text_analyzer/2_examples/Q1_examples/example_3/sentences_small_3.csv",
                            removeInputPath="text_analyzer/1_data/Data/REMOVEWORDS.csv")
    # print(preprocessor_2.write_result_to_json("11.json"))
    print(preprocessor_3.write_result_to_json("1.json"))




