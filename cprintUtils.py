from termcolor import cprint


def dprint(string, *args):
    cprint(string, "yellow")


def eprint(string, *args):
    cprint(string, "red")


def iprint(string, *args):
    cprint(string, "green")
