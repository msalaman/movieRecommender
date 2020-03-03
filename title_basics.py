#!/usr/bin/env python3

import csv

N = 10

with open('title.basics.tsv', 'r') as file:
    tsv = csv.reader(file, delimiter='\t')
    headers = next(tsv)
    for title, _ in zip(tsv, range(N)):
        tconst, title_type, primary_title, original_title, is_adult, start_year, end_year, runtime_minutes, genres = title