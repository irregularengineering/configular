#! /usr/local/bin/python3
"""
Read from config and/or environment variables using configular logic and export as environment
variables

Usage: some_env_var=$(./configular/cli <section> <parameter>)
"""

from argparse import ArgumentParser
from configular import Configular


def main():
    parser = ArgumentParser()
    parser.add_argument('config_file', help='Config file name')
    parser.add_argument('section', help='Section name')
    parser.add_argument('parameter', help='Argument name')
    parser.add_argument('-o', '--override-file',  help='Config file override file name')
    args = parser.parse_args()

    configular = Configular(args.config_file, override_filename=args.override_file)
    print(configular.get(args.section, args.parameter))


if __name__ == '__main__':
    main()
