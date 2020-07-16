#!/usr/bin/env python
# Quick and dirty script to do an in-place replace on "DOCDIR" string so that I don't have to modify the code to work with Meson yet.
# Usage: docdir_findreplace.py "search text" "replace_text" input_file

import fileinput, sys

search_text = sys.argv[1]
replace_text = sys.argv[2]
input_file = sys.argv[3]

with fileinput.FileInput(input_file, inplace=True, backup='.bak') as file:
    for line in file:
        print(line.replace(search_text, replace_text), end='')
