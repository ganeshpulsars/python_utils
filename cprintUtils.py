from termcolor import cprint as tc_cprint


def dprint(string, *args, **kwargs):
    tc_cprint(string, "yellow", *args, **kwargs)


def eprint(string, *args, **kwargs):
    tc_cprint(string, "red", *args, **kwargs)


def iprint(string, *args, **kwargs):
    tc_cprint(string, "green", *args, **kwargs)


def cprint(string, *args, **kwargs):
    tc_cprint(string, *args, **kwargs)
