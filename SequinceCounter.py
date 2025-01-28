import sys
import typing
import os
import json
import Preprocesser


# static method can be used for external use

def generate_k_seqs(sentences, N):
    """
    Generates k-sequences for each k from 1 to N and removes commas after the last word if
    the sequence contains only one word. Additionally, sorts the sequences lexicographically.
    """
    seq_counts = {}
    for k in range(1, N + 1):
        seq_counts[f"{k}_seq"] = {}
    # Generate k-sequences for each sentence
    for sentence in sentences:
        for k in range(1, N + 1):
            for i in range(len(sentence) - k + 1):
                k_seq = tuple(sentence[i:i + k])  # Create the k-seq as a tuple
                seq_counts[f"{k}_seq"][k_seq] = seq_counts[f"{k}_seq"].get(k_seq, 0) + 1
    # Sort the sequences lexicographically by their tuple key
    for k in range(1, N + 1):
        seq_counts[f"{k}_seq"] = sorted(seq_counts[f"{k}_seq"].items(), key=lambda x: x[0])

    return seq_counts


def load_Sentences_names(json_file_path: typing.Union[str, os]) -> (list[list[str]], list[list[str]]):
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
            names = data.get(question_key, {}).get('Processed Names', [])
            Sentences = data.get(question_key, {}).get('Processed Sentences', [])
        # handle errors
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {json_file_path} was not found.")
    except json.JSONDecodeError:
        raise json.JSONDecodeError(f"JSONDecodeError: The file {json_file_path} is not a valid JSON file.")
    except PermissionError:
        raise PermissionError(f"PermissionError: Permission denied to read {json_file_path}.")
    except Exception as e:
        raise Exception(f"An error occurred while loading preprocessed data: {str(e)}")
    return Sentences, names


class SequinceCounter:

    def __init__(self, question_num: int, sentence_input_path: typing.Union[str, os.PathLike] = None,
                 remove_input_path: typing.Union[str, os.PathLike] = None,
                 people_input_path: typing.Union[str, os.PathLike] = None,
                 json_input_path: typing.Union[str, os.PathLike] = None, N: int = 3, preprocessed: bool = False):
        """(constructor)
        Initialize the SequenceCounter class based on input parameters.
        :param sentence_input_path: Path to sentence file (if preprocessed flag is not set)
        :param remove_input_path: Path to the remove words file (if preprocessed flag is not set)
        :param json_input_path: Path to preprocessed JSON file (if preprocessed flag is set)
        :param N: Maximal sequence length
        """
        try:
            if N % 1 != 0 or N <= 0:
                raise ValueError('the N must be a positive integer')
            self.__N: int = N
            self.__questionNum = question_num
            if preprocessed:
                # If JSON input path is provided, load the preprocessed data
                self.__sentences, _ = load_Sentences_names(json_input_path)
            elif sentence_input_path and remove_input_path:
                # If sentence and remove files are provided, load the raw data
                self.__sentences = self.__load_data(sentence_input_path, remove_input_path)
            else:
                raise ValueError("Either --preprocessed or both --sentence_input and --remove_input must be provided.")
        except (FileNotFoundError, PermissionError, TypeError, Exception) as e:
            print(f"Error: {e}")  # Handle any file-related or other errors
            sys.exit(1)  # Exit program if there's an error

    def __load_data(self, sentence_input_path: typing.Union[str, os], remove_input_path: typing.Union[str, os]) -> list[list[str]]:
        """
        Loads __sentences and removes unwanted words based on the provided files.
        :param sentence_input_path: Path to the sentence input file
        :param remove_input_path: Path to the file with words to remove
        :time complexity: O(n)
        """
        try:
            dataLoader = Preprocesser.Preprocessor(1, sentenceInputPath=sentence_input_path,
                                                   removeInputPath=remove_input_path)
            sentences = dataLoader.getSentences()
        except ValueError as e:
            raise ValueError("{0}".format(e))
        except FileNotFoundError as e:
            raise FileNotFoundError("{0}".format(e))
        except PermissionError as e:
            raise PermissionError("{0}".format(e))
        except Exception as e:
            raise Exception("{0}".format(e))
        return sentences

    def count_sequences(self) -> list[list[str|list[list[str|int]]]]:
        """
        Generate k-sequences and count their occurrences.
        """
        return self.__convert_to_json_style(generate_k_seqs(self.__sentences, self.__N))

    def __convert_to_json_style(self, seq_counts: dict[str, list[tuple[tuple[str], int]]]) -> list[
        list[str | list[list[str, int]]]]:
        """
        Convert the sequences to json-style and return it
        :param seq_counts: the sequences to convert into json-style
        :return: the json-style representation of the seq_count ready to print
        """
        result_list = []
        for seq in range(1, self.__N + 1):
            if f"{seq}_seq" not in seq_counts:
                break
            sub_seq = []
            for key in seq_counts[f"{seq}_seq"]:
                text = " ".join(key[0])
                sub_seq.append([text.strip(), key[1]])
            result_list.append([f"{seq}_seq", sub_seq])
        return result_list

    def write_result_to_json(self, filePath: str) -> bool:
        data = {
            f"Question {self.__questionNum}": {
                f"{self.__N}-Seq Counts": self.count_sequences()
            }
        }
        if Preprocesser.writeTojsonFile(filePath, data):
            return True
        else:
            return False


if __name__ == '__main__':
    SEQUENCE_COUNTER1 = SequinceCounter(2,
                                        sentence_input_path="text_analyzer/2_examples/Q2_examples/example_1"
                                                            "/sentences_small_1.csv",
                                        remove_input_path="text_analyzer/1_data/Data/REMOVEWORDS.csv",
                                        N=3)
    SEQUENCE_COUNTER2 = SequinceCounter(2,
                                        sentence_input_path="text_analyzer/2_examples/Q2_examples/example_2"
                                                            "/sentences_small_2.csv",
                                        remove_input_path="text_analyzer/1_data/Data/REMOVEWORDS.csv",
                                        N=4)
    SEQUENCE_COUNTER3 = SequinceCounter(2,
                                        sentence_input_path="text_analyzer/2_examples/Q2_examples/example_3"
                                                            "/sentences_small_3.csv",
                                        remove_input_path="text_analyzer/1_data/Data/REMOVEWORDS.csv",
                                        N=5)
    SEQUENCE_COUNTER4 = SequinceCounter(2,
                                        json_input_path="text_analyzer/2_examples/Q1_examples/example_1/Q1_result1.json",
                                        preprocessed=True, N=3)
    SEQUENCE_COUNTER5 = SequinceCounter(2,
                                        json_input_path="text_analyzer/2_examples/Q1_examples/example_2/Q1_result2.json",
                                        preprocessed=True, N=4)
    SEQUENCE_COUNTER6 = SequinceCounter(2,
                                        json_input_path="text_analyzer/2_examples/Q1_examples/example_3/Q1_result3.json",
                                        preprocessed=True, N=5)
