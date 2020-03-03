#!/usr/bin/env python3

import csv, re

N = 10

MOVIE_TITLE_RE = re.compile(r'^(.*?)\s*\(([\d]+)\)$')

with open('MovieTweetings/latest/movies.dat', 'r') as movies, open('MovieTweetings/latest/ratings.dat', 'r') as ratings:
    movies = csv.reader((line.replace('::', ':') for line in movies), delimiter=':')
    ratings = csv.reader((line.replace('::', ':') for line in ratings), delimiter=':')

    for movie, _ in zip(movies, range(N)):
        movie_id, movie_title_year, genres = movie
        movie_title, movie_year = re.fullmatch(MOVIE_TITLE_RE, movie_title_year).groups()

    for rating, _ in zip(ratings, range(N)):
        user_id, movie_id, rating, rating_timestamp = rating
        print(rating)