#! /usr/bin/python

import sys
import os
import argparse
import argparse_actions

#root_path = os.path.dirname(os.path.dirname(__file__))
#if root_path not in sys.path:
#        sys.path.append(root_path)

import client

def execute(args):
    sync_client = client.DbSyncClient(
            args.s,
            args.d,
            args.se,
            args.po,
            args.c,
            )
    sync_client.copy()

def validate_filename(xxx, dest):
    print xxx
    print dest


def main():
    parser = argparse.ArgumentParser(description='Command line tool for db-sync')
    parser.add_argument(
            '-s', 
            metavar='source',
            help='Source file or directory path',
            action='store',
            required=True,
            )
    parser.add_argument(
            '-d', metavar='destination',
            action='store',
            help='Destination file or directory path',
            required=True,
            )
    parser.add_argument(
            '-se', metavar='server',
            action=argparse_actions.ProperIpFormatAction,
            help='Server to connect',
            required=True,
            )
    parser.add_argument(
            '-po', metavar='port',
            action='store',
            help='Port of server to connect to.',
            required=True,
            type=int

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
