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
                        default=-1
                        )
    parser.add_argument('--pairs',
                        help="json file with list of pairs",
                        default=None
                        )
    parser.add_argument('--threshold',
                        type=int,
                        help="graph connection threshold",
                        default=-1
                        )
    parser.add_argument('--maximal_distance',
                        type=int,
                        help="maximal distance between nodes in graph",
                        default=-1
                        )

    parser.add_argument('--qsek_query_path',
                        help="json file with query path",
                        default=None
                        )
    return parser.parse_args(args)


def main():
    args = readargs()
    try:
        if args.task == '1':
            # Initialize the preprocessor
            if args.sentences is None or args.removewords is None or args.names is None:
                raise ValueError("Please provide sentences file and names file and remove words file ")
            preProcessor = Parser(QuestionNumber=int(args.task),
                                  sentenceInputPath=args.sentences,
                                  removeInputPath=args.removewords,
                                  peopleInputPath=args.names)
            # Call the write_result method and check the result
            result = preProcessor.return_results()
            print(result)  # Print the result
        elif args.task == '2':
            # Initialize the preprocessor
            if not isinstance(int(args.maxk), int) or int(args.maxk) < 0:
                raise ValueError("maxk must be a positive integer")
            if args.preprocessed:
                sequenceCounter = SequinceCounter(int(args.task), json_input_path=args.preprocessed, preprocessed=True, N=int(args.maxk))
            else:
                if args.sentences is None or args.removewords is None:
                    raise ValueError("Please provide sentences file and removewords file ")
                sequenceCounter = SequinceCounter(int(args.task), sentence_input_path=args.sentences, remove_input_path=args.removewords, N=int(args.maxk))
            result = sequenceCounter.return_results()
            print(result)

        elif args.task == '3':
            if args.preprocessed:
                name_counter = NamesCounter(int(args.task), json_input_path=args.preprocessed, preprocessed=True)
            else:
                if args.sentences is None or args.removewords is None or args.names is None:
                    raise ValueError("Please provide sentences file and names file and remove words file ")
                name_counter = NamesCounter(QNum=int(args.task), sentence_input_path=args.sentences, remove_input_path=args.removewords, people_input_path=args.names)
            result = name_counter.return_results()
            print(result)  # Print the result

        elif args.task == '4':
            # Initialize the preprocessor
            if not args.qsek_query_path:
                raise ValueError("qsek jsom file should be provided")
            if args.preprocessed:
                searchEngine = SearchEngine(QNum=int(args.task), jsonInputFile=args.preprocessed, preprocessed=True, kSeqJson=args.qsek_query_path)
            else:
                if args.sentences is None or args.removewords is None or args.names is None:
                    raise ValueError("Please provide sentences file and names file and remove words file ")
                searchEngine = SearchEngine(QNum=int(args.task), sentence_input_path=args.sentences, remove_input_path=args.removewords, kSeqJson=args.qsek_query_path)
            result = searchEngine.return_results()
            print(result)  # Print the result

        elif args.task == '5':
            # Initialize the preprocessor
            if not isinstance(int(args.maxk), int) or int(args.maxk) < 0:
                raise ValueError("maxk must be a positive integer")
            if args.preprocessed:
                people_scions = PeopleKAssociations(QNum=int(args.task), json_input_path=args.preprocessed, preprocessed=True, N=args.maxk)
            else:
                if args.sentences is None or args.removewords is None or args.names is None:
                    raise ValueError("Please provide sentences file and names file and remove words file ")
                people_scions = PeopleKAssociations(QNum=int(args.task), sentence_input_path=args.sentences, remove_input_path=args.removewords, people_input_path=args.names, N=args.maxk)
            result = people_scions.return_results()
            print(result)  # Print the result

        elif args.task == '6':
            # Initialize the preprocessor
            if not isinstance(int(args.windowsize), int) or int(args.windowsize) < 0:
                raise ValueError("windowsize must be a positive integer")
            if not isinstance(int(args.threshold), int) or int(args.threshold) < 0:
                raise ValueError("threshold must be a positive integer")
            if args.preprocessed:
                graph = PeopleConnectionGraph(QNum=int(args.task), jsonInputFile=args.preprocessed, preprocessed=True, WindowSize=args.windowsize, Threshold=args.threshold)
            else:
                if args.sentences is None or args.removewords is None or args.names is None:
                    raise ValueError("Please provide sentences file and names file and remove words file ")
                graph = PeopleConnectionGraph(QNum=int(args.task), sentence_input_path=args.sentences,
                                                  remove_input_path=args.removewords, people_input_path=args.names, WindowSize=args.windowsize, Threshold=args.threshold)
            result = graph.return_results()
            print(result)  # Print the result

        elif args.task == '7':
            # Initialize the preprocessor
            if not args.pairs:
                raise ValueError("pairs file is required ")
            if not isinstance(int(args.maximal_distance), int) or int(args.maximal_distance) < 0:
                raise ValueError("maximal_distance must be a positive integer")
            if args.preprocessed:
                connectionGraph = CheckConnection(QNum=int(args.task), Maximal_distance=args.maximal_distance, jsonInputFile=args.preprocessed, preprocessed=True, People_connections_to_check=args.pairs)
            else:
                if not args.names or not args.sentences or not args.removewords or int(args.windowsize)<1 or int(args.threshold)<0 :
                    raise ValueError("one of supplied data from argumint is not availed or required")
                connectionGraph = CheckConnection(QNum=int(args.task), Maximal_distance=args.maximal_distance, sentence_input_path=args.sentences, remove_input_path=args.removewords, people_input_path=args.names, WindowSize=int(args.windowsize), Threshold=int(args.threshold), People_connections_to_check=args.pairs)
            result = connectionGraph.return_results()
            print(result)  # Print the result

        elif args.task == '8':
            # Initialize the preprocessor
            if not args.pairs:
                raise ValueError("pairs file is required ")
            if not isinstance(int(args.k), int) or int(args.k) < 0:
                raise ValueError("k must be a positive integer")
            if args.preprocessed:
                connectionGraph = CheckConnection(QNum=int(args.task), k=int(args.k),
                                                  jsonInputFile=args.preprocessed, preprocessed=True,
                                                  People_connections_to_check=args.pairs, fixed_length=True)
            else:
                if not args.names or not args.sentences or not args.removewords or int(args.windowsize)<1 or int(args.threshold)<0 :
                    raise ValueError("one of supplied data from argumint is not availed or required")
                connectionGraph = CheckConnection(QNum=int(args.task), k=int(args.k),
                                                  sentence_input_path=args.sentences,
                                                  remove_input_path=args.removewords, people_input_path=args.names,
                                                  WindowSize=args.windowsize, Threshold=args.threshold,
                                                  People_connections_to_check=args.pairs, fixed_length=True)
            result = connectionGraph.return_results()
            print(result)  # Print the result

        elif args.task == '9':
            # Initialize the preprocessor
            if not isinstance(int(args.threshold), int) or int(args.threshold) < 0:
                raise ValueError("threshold must be a positive integer")
            if args.preprocessed:
                sentences_graph = SentenceGraph(question_number=int(args.task),
                                                json_input_path=args.preprocessed, preprocessed=True, threshold=int(args.threshold))
            else:
                if not args.sentences or not args.removewords:
                    raise ValueError("sentences and removewords must be provided")
                sentences_graph = SentenceGraph(question_number=int(args.task),
                                               sentence_input_path=args.sentences,
                                               remove_input_path=args.removewords, threshold=int(args.threshold))
            result = sentences_graph.return_results()
            print(result)  # Print the result

        else:
            raise ValueError("must provide task number between 1 and 9")

    except (FileNotFoundError, PermissionError, TypeError, Exception) as e:
        print(f"Invalid: {e}")
        return 1  # Return 1 on failure


if __name__ == "__main__":
    main()