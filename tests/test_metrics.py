import os

import argparse_actions

from src.client import DbSyncClient
import argparse


def execute(args):
    source_filename_list = ["test_10m",
                            "test_100m",
                            "test_250m",
                            ]

    source_path = "/app/"
    destination_path = os.getcwd()
    server = args.se # TODO : argument
    chunk_size = args.c # TODO : argument
    timeout_seconds = 300  # TODO : argument
    port = 80

    for file in source_filename_list:
        source_file = os.path.join(source_path, file)
        destination_file = os.path.join(destination_path, file)
        sync_client = DbSyncClient(source=source_file,
                                   destination=destination_file,
                                   server=server,
                                   port=port,
                                   chunk_size=chunk_size,
                                   )
        sync_client.copy()


def main():
    parser = argparse.ArgumentParser(description='Test ')
    parser.add_argument(
            '-se', metavar='server',
            action=argparse_actions.ProperIpFormatAction,
            help='Server to connect',
            required=True,
            )
    parser.add_argument(
            '-c', metavar='chunk-size',
            action='store',
            choices=(1024, 2048, 4096, 8192),
            help='Size of each chunk',
            required=True,
            type=int,
            )

    try:
        args = parser.parse_args()
        execute(args)
    except argparse_actions.NonFolderError as e:
        print e


if __name__ == '__main__':
    main()
