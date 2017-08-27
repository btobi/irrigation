import argparse

parser = argparse.ArgumentParser()


def execute(command_string=""):
    args = command_string.split(" ")

    parser.parse_args(args)

    answer = ""

    return answer
