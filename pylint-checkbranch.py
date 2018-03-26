#!/usr/bin/env python

# Fred Spreen <fspreen@logikos.com>
# 23 March 2018

from __future__ import print_function

import re
import subprocess

NA_SCORE = "N/A"

pylintScore = re.compile(r'Your code has been rated at (\S+)/(\S+)')

# TODO change working directory to repo root?

try:
    repoRoot = subprocess.check_output(["git", "rev-parse", "--show-toplevel"])\
            .strip()
except subprocess.CalledProcessError:
    repoRoot = None

try:
    lines = subprocess.check_output(
            ["git", "diff", "--name-status", "origin/master..."],
            cwd=repoRoot
            ).strip().split("\n")
    files = [x.split(None,1) for x in lines]
except subprocess.CalledProcessError:
    files = []

files.sort(lambda a,b: cmp(a[1].lower(), b[1].lower()))

table = []

for st,f in files:
    try:
        analysis = subprocess.check_output(
            ["pylint", "--rcfile=.pylintrc", f],
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            cwd=repoRoot)
    except subprocess.CalledProcessError as exc:
        analysis = exc.output

    scoreMatch = re.search(pylintScore, analysis)

    if scoreMatch:
        numer = scoreMatch.group(1)
        denom = scoreMatch.group(2)

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

    status_emoji = ""
    if st == "A":
        # Added
        status_emoji = ":heavy_plus_sign:"
    elif st == "D":
        # Deleted
        status_emoji = ":x:"
    elif st == "M":
        # Modified
        status_emoji = ":m:"
    # For full list of status fields:  man git-diff; search for diff-filter

    table.append((status_emoji, escaped_fname, score))


max_status = max([3, len("Status"), max([len(t[0]) for t in table])])
max_fname = max([3, len("File Name"), max([len(t[1]) for t in table])])
max_score = max([3, len("Pylint Score"), max([len(t[2]) for t in table])])

# Header
print("| {0} | {1} | {2} |".format(
    str.ljust("Status", max_status),
    str.ljust("File Name", max_fname),
    str.ljust("Pylint Score", max_score)))

# Divider
print("| {0} | {1} | {2} |".format(
    '-' * max_status,
    '-' * max_fname,
    '-' * max_score))

for t in table:
    print("| {0} | {1} | {2} |".format(
        str.ljust(t[0], max_status),
        str.ljust(t[1], max_fname),
        str.ljust(t[2], max_score)))
