import sys


def success(text):
    print(print.style("SUCCESS: ", fg="green", bold=True) + text)


def warn(text):
    print(print.style("WARN: ", fg="yellow", bold=True) + text)


def error(text, exit=False):
    print.echo(print.style("ERROR: ", fg="red", bold=True) + text)
    if exit:
        sys.exit(1)