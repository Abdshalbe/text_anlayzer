from Parser import Parser
from NamesCounter import NamesCounter
from PeopleKAssociations import PeopleKAssociations
from PeopleConnectionGraph import PeopleConnectionGraph
from CheckConnection import CheckConnection
from SearchEngine import SearchEngine
from SequinceCounter import SequinceCounter
from SentencesGraph import SentenceGraph

import argparse


def readargs(args=None):
    parser = argparse.ArgumentParser(
        prog='Text Analyzer project',
    )
    # General arguments
    parser.add_argument('-t', '--task',
                        help="task number",
                        required=True
                        )
    parser.add_argument('-s', '--sentences',
                        help="Sentence file path",
                        default=None
                        )
    parser.add_argument('-n', '--names',
                        help="Names file path",
                        default=None
                        )
    parser.add_argument('-r', '--removewords',
                        help="Words to remove file path",
                        default=None
                        )
    parser.add_argument('-p', '--preprocessed',
                        action='append',
                        help="json with preprocessed data",
                        default=False
                        )
    # Task specific arguments
    parser.add_argument('--maxk',
                        type=int,
                        help="Max k",
                        default=None
                        )
    parser.add_argument('--fixed_length',
                        type=int,
                        help="fixed length to find",
                        default=-1
                        )
    parser.add_argument('--windowsize',
                        type=int,
                        help="Window size",
                        )
    parser.add_argument('--pairs',
                        help="json file with list of pairs",
                        )
    parser.add_argument('--threshold',
                        type=int,
                        help="graph connection threshold",
                        )
    parser.add_argument('--maximal_distance',
                        type=int,
                        help="maximal distance between nodes in graph",
                        )

    parser.add_argument('--qsek_query_path',
                        help="json file with query path",
                        )
    return parser.parse_args(args)


def main():
    args = readargs()
    try:
        print(args.task)
        if args.task == '1':
            print(f"Running Task {args.task}...")
            # Initialize the preprocessor
            preProcessor = Parser(QuestionNumber=int(args.task),
                                  sentenceInputPath=args.sentences,
                                  removeInputPath=args.removewords,
                                  peopleInputPath=args.names)
            # Call the write_result method and check the result
            result = preProcessor.return_results()
            print(result)  # Print the result
        elif args.task == '2':
            print(f"Running Task {args.task}...")
            # Initialize the preprocessor
            if not isinstance(int(args.maxk), int) or int(args.maxk) < 0:
                raise ValueError("maxk must be a positive integer")
            if args.preprocessed:
                sequinceCounter = SequinceCounter(args.task, json_input_path=args.preprocessed, preprocessed=True, N=int(args.maxk))
            else:
                sequinceCounter = SequinceCounter(args.task, sentence_input_path=args.sentences, remove_input_path=args.removewords, N=int(args.maxk))
            result = sequinceCounter.return_results()
            print(result)

        elif args.task == '3':
            print(f"Running Task {args.task}...")
            if args.preprocessed:
                name_counter = NamesCounter(args.task, json_input_path=args.preprocessed, preprocessed=True)
            else:
                name_counter = NamesCounter(QNum=args.task, sentence_input_path=args.sentences, remove_input_path=args.removewords, people_input_path=args.names)
            result = name_counter.return_results()
            print(result)  # Print the result
        elif args.task == '4':
            print(f"Running Task {args.task}...")
            # Initialize the preprocessor
            if args.preprocessed:
                searchEngine = SearchEngine(QNum=args.task, jsonInputFile=args.preprocessed, preprocessed=True, kSeqJson=args.qsek_query_path)
            else:
                searchEngine = SearchEngine(QNum=args.task, sentence_input_path=args.sentences, remove_input_path=args.removewords, kSeqJson=args.qsek_query_path)
            result = searchEngine.return_results()
            print(result)  # Print the result

        elif args.task == '5':
            print(f"Running Task {args.task}...")
            # Initialize the preprocessor
            if args.preprocessed:
                people_ascions = PeopleKAssociations(QNum=args.task, json_input_path=args.preprocessed, preprocessed=True, N=args.maxk)
            else:
                people_ascions = PeopleKAssociations(QNum=args.task, sentence_input_path=args.sentences, remove_input_path=args.removewords, people_input_path=args.names, N=args.maxk)
            result = people_ascions.return_results()
            print(result)  # Print the result

        elif args.task == '6':
            print(f"Running Task {args.task}...")
            # Initialize the preprocessor
            if args.preprocessed:
                graph = PeopleConnectionGraph(QNum=args.task, jsonInputFile=args.preprocessed, preprocessed=True, WindowSize=args.windowsize, Threshold=args.threshold)
            else:
                graph = PeopleConnectionGraph(QNum=args.task, sentence_input_path=args.sentences,
                                                  remove_input_path=args.removewords, people_input_path=args.names, WindowSize=args.windowsize, Threshold=args.threshold)
            result = graph.return_results()
            print(result)  # Print the result

        elif args.task == '7':
            print(f"Running Task {args.task}...")
            # Initialize the preprocessor
            if args.preprocessed:
                connectionGraph = CheckConnection(QNum=args.task, Maximal_distance=args.maximal_distance, jsonInputFile=args.preprocessed, preprocessed=True, People_connections_to_check=args.pairs)
            else:
                connectionGraph = CheckConnection(QNum=args.task, Maximal_distance=args.maximal_distance, sentence_input_path=args.sentences, remove_input_path=args.removewords, people_input_path=args.names, WindowSize=args.windowsize, Threshold=args.threshold, People_connections_to_check=args.pairs)
            result = connectionGraph.return_results()
            print(result)  # Print the result

        elif args.task == '8':
            print(f"Running Task {args.task}...")
            # Initialize the preprocessor
            if args.preprocessed:
                connectionGraph = CheckConnection(QNum=args.task, k=args.k,
                                                  jsonInputFile=args.preprocessed, preprocessed=True,
                                                  People_connections_to_check=args.pairs, fixed_length=True)
            else:
                connectionGraph = CheckConnection(QNum=args.task, k=args.k,
                                                  sentence_input_path=args.sentences,
                                                  remove_input_path=args.removewords, people_input_path=args.names,
                                                  WindowSize=args.windowsize, Threshold=args.threshold,
                                                  People_connections_to_check=args.pairs, fixed_length=True)
            result = connectionGraph.return_results()
            print(result)  # Print the result

        elif args.task == '9':
            print(f"Running Task {args.task}...")
            # Initialize the preprocessor
            if args.preprocessed:
                sentences_graph = SentenceGraph(question_number=args.task,
                                                json_input_path=args.preprocessed, preprocessed=True, threshold=args.threshold)
            else:
                sentences_graph = SentenceGraph(question_number=args.task,
                                               sentence_input_path=args.sentences,
                                               remove_input_path=args.removewords, threshold=args.threshold)
            result = sentences_graph.return_results()
            print(result)  # Print the result

    except Exception as e:
        print(f"Invalid: {e}")
        return 1  # Return 1 on failure


if __name__ == "__main__":
    main()