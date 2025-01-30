#!/usr/bin/env python3
from Parser import Parser
from NamesCounter import NamesCounter
from PeopleKAssocions import PeopleKAssocions
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
                        )
    parser.add_argument('-n', '--names',
                        help="Names file path",
                        )
    parser.add_argument('-r', '--removewords',
                        help="Words to remove file path",
                        )
    parser.add_argument('-p', '--preprocessed',
                        action='append',
                        help="json with preprocessed data",
                        )
    # Task specific arguments
    parser.add_argument('--maxk',
                        type=int,
                        help="Max k",
                        )
    parser.add_argument('--fixed_length',
                        type=int,
                        help="fixed length to find",
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
        if args.task == 1:
            print(f"Running Task {args.task}...")
            # Initialize the preprocessor
            preProcessor = Parser(QuestionNumber=args.task,
                                  sentenceInputPath=args.sentences,
                                  removeInputPath=args.removewords,
                                  peopleInputPath=args.names)
            # Call the write_result_to_json method and check the result
            if preProcessor.write_result_to_json(f"finalProject/Q{args.task}_result.json"):
                print(f"Result successfully written to Q{args.task}_result.json")
            else:
                print("Failed to write result.")

        elif args.task == 2:
            print(f"Running Task {args.task}...")
            # Initialize the preprocessor
            if args.preprocessed:
                sequinceCounter = SequinceCounter(args.task, json_input_path=args.preprocessed,preprocessed=True,N=args.maxk)
            else:
                sequinceCounter = SequinceCounter(args.task,sentence_input_path=args.sentences,remove_input_path=args.removewords,N=args.maxk)
            # Call the write_result_to_json method and check the result
            result = sequinceCounter.write_result_to_json(f"finalProject/Q{args.task}_result.json")
            if result:
                print(f"Result successfully written to Q{args.task}_result.json")
            else:
                print("Failed to write result.")

        elif args.task == 3:
            print(f"Running Task {args.task}...")
            if args.preprocessed:
                name_counter = NamesCounter(args.task, json_input_path=args.preprocessed,preprocessed=True)
            else:
                name_counter = NamesCounter(QNum=args.task, sentence_input_path=args.sentences, remove_input_path=args.removewords ,people_input_path=args.names)
            # Call the write_result_to_json method and check the result
            if name_counter.write_to_json(f"finalProject/Q{args.task}_result.json"):
                print(f"Result successfully written to Q{args.task}_result.json")
            else:
                print("Failed to write result.")

        if args.task == 4:
            print(f"Running Task {args.task}...")
            # Initialize the preprocessor
            if args.preprocessed:
                searchEngine = SearchEngine(QNum=args.task,jsonInputFile=args.preprocessed,preprocessed=True,kSeqJson=args.qsek_query_path)
            else:
                searchEngine = SearchEngine(QNum=args.task,
                                               sentence_input_path=args.sentences,
                                               remove_input_path=args.removewords,kSeqJson=args.qsek_query_path)
            # Call the write_result_to_json method and check the result
            if searchEngine.write_to_json(f"finalProject/Q{args.task}_result.json"):
                print(f"Result successfully written to Q{args.task}_result.json")
            else:
                print("Failed to write result.")
        if args.task == 5:
            print(f"Running Task {args.task}...")
            # Initialize the preprocessor
            if args.preprocessed:
                people_ascions = PeopleKAssocions(QNum=args.task,json_input_path=args.preprocessed,preprocessed=True,N=args.maxk)
            else:
                people_ascions = PeopleKAssocions(QNum=args.task,sentence_input_path=args.sentences,remove_input_path=args.removewords,N=args.maxk)
            if people_ascions.write_to_json(f"finalProject/Q{args.task}_result.json"):
                print(f"Result successfully written to Q{args.task}_result.json")
            else:
                print("Failed to write result.")

        if args.task == 6:
            print(f"Running Task {args.task}...")
            # Initialize the preprocessor
            if args.preprocessed:
                graph = PeopleConnectionGraph(QNum=args.task, jsonInputFile=args.preprocessed, preprocessed=True,
                                                  WindowSize=args.windowsize, Threshold=args.threshold)
            else:
                graph = PeopleConnectionGraph(QNum=args.task, sentence_input_path=args.sentences,
                                                  remove_input_path=args.removewords,people_input_path=args.names ,WindowSize=args.windowsize, Threshold=args.threshold)
            # Call the write_result_to_json method and check the result
            if graph.write_to_json(f"finalProject/Q{args.task}_result.json"):
                print(f"Result successfully written to Q{args.task}_result.json")
            else:
                print("Failed to write result.")

        if args.task == 7:
            print(f"Running Task {args.task}...")
            # Initialize the preprocessor
            if args.preprocessed:
                connectionGraph = CheckConnection(QNum=args.task, Maximal_distance= args.maximal_distance,jsonInputFile=args.preprocessed,preprocessed=True,People_connections_to_check=args.pairs)
            else:
                connectionGraph = CheckConnection(QNum=args.task,Maximal_distance= args.maximal_distance, sentence_input_path=args.sentences,remove_input_path=args.removewords,people_input_path=args.names ,WindowSize=args.windowsize, Threshold=args.threshold,People_connections_to_check=args.pairs)
            # Call the write_result_to_json method and check the result

            if connectionGraph.write_to_json(f"finalProject/Q{args.task}_result.json"):
                print(f"Result successfully written to Q{args.task}_result.json")
            else:
                print("Failed to write result.")

        if args.task == 8:
            print(f"Running Task {args.task}...")
            # Initialize the preprocessor
            if args.preprocessed:
                connectionGraph = CheckConnection(QNum=args.task, k=args.k,
                                                  jsonInputFile=args.preprocessed, preprocessed=True,
                                                  People_connections_to_check=args.pairs,fixed_length=True)
            else:
                connectionGraph = CheckConnection(QNum=args.task,k=args.k,
                                                  sentence_input_path=args.sentences,
                                                  remove_input_path=args.removewords, people_input_path=args.names,
                                                  WindowSize=args.windowsize, Threshold=args.threshold,
                                                  People_connections_to_check=args.pairs,fixed_length=True)
            # Call the write_result_to_json method and check the result

            if connectionGraph.write_to_json(f"finalProject/Q{args.task}_result.json"):
                print(f"Result successfully written to Q{args.task}_result.json")
            else:
                print("Failed to write result.")
        if args.task == 9:
            print(f"Running Task {args.task}...")
            # Initialize the preprocessor
            if args.preprocessed:
                sentences_graph = SentenceGraph(question_number=args.task,
                                                json_input_path=args.preprocessed,preprocessed=True,threshold=args.threshold)
            else:
                sentences_graph = SentenceGraph(question_number=args.task,
                                               sentence_input_path=args.sentences,
                                               remove_input_path=args.removewords,threshold=args.threshold)
            # Call the write_result_to_json method and check the result
            result = sentences_graph.write_to_json(f"finalProject/Q{args.task}_result.json")
            if result:
                print(f"Result successfully written to Q{args.task}_result.json")
            else:
                print("Failed to write result.")
    except Exception as e:
        print(f"An error occurred: {e}")
        return 1  # Return 1 on failure


if __name__ == "__main__":
    main()
