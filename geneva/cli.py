import argparse
from geneva import engine


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    run_parser = subparsers.add_parser("engine", parents=[engine.parser], add_help=False)
    run_parser.set_defaults(func=engine.main)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
