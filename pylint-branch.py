#!/usr/bin/env python

from __future__ import print_function

import re
import subprocess

NA_SCORE = "N/A"

pylint_score = re.compile('Your code has been rated at (\S+)/(\S+)')

# TODO change working directory to repo root?

try:
    files = subprocess.check_output(["git", "diff", "--name-only", "origin/master..."]).strip().split("\n")
except subprocess.CalledProcessError:
    files = []

# TODO better sorting?
files.sort()

table = []

for f in files:
    try:
        analysis = subprocess.check_output(
                ["pylint", "--rcfile=.pylintrc", f],
                stderr=subprocess.STDOUT,
                universal_newlines = True)
    except subprocess.CalledProcessError as x:
        analysis = x.output

    scorematch = re.search(pylint_score, analysis)

    if scorematch:
        numer = scorematch.group(1)
        denom = scorematch.group(2)

        score = numer + "/" + denom

        if float(numer) == 10.00:
            score = score + " :star: :100:"
        elif float(numer) >= 8.00:
            score = score + " :star:"
        elif float(numer) < 0:
            score = score + " :x:"

    # Empty file (only has message line indicating config file)
    elif len(analysis.strip().split("\n")) <= 1 and analysis.startswith("Using config file "):
        score = NA_SCORE

    else:
        # Unknown circumstance (non-empty, non-Python code?)
        score = "???"

    escaped_fname = re.sub('_', '\\_', f)
    table.append((escaped_fname, score))


max_fname = max([3, len("File Name"), max([len(t[0]) for t in table])])
max_score = max([3, len("Pylint Score"), max([len(t[1]) for t in table])])

# Header
print("| {0} | {1} |".format(
    str.ljust("File Name", max_fname),
    str.ljust("Pylint Score", max_score)))

# Divider
print("| {0} | {1} |".format(
    '-' * max_fname,
    '-' * max_score))

for t in table:
    print("| {0} | {1} |".format(
        str.ljust(t[0], max_fname),
        str.ljust(t[1], max_score)))
