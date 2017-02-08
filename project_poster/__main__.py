from project_poster.app import Application
from project_poster.logger import ConsoleLogger


def main(argv):
    Application(logger=ConsoleLogger()).run()


if __name__ == '__main__':
    from sys import argv
    main(argv)

