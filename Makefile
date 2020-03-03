.PHONY:	title_basics.py	clean movie_tweetings.py all

all:	movie_tweetings.py title_basics.py

movie_tweetings.py:	MovieTweetings/

MovieTweetings/:	MovieTweetings.zip
	unzip MovieTweetings.zip
	mv MovieTweetings-master MovieTweetings

MovieTweetings.zip:
	wget -O MovieTweetings.zip https://github.com/sidooms/MovieTweetings/archive/master.zip

title_basics.py:	title.basics.tsv

title.basics.tsv:	title.basics.tsv.gz
	gunzip -k title.basics.tsv.gz

title.basics.tsv.gz:
	wget https://datasets.imdbws.com/title.basics.tsv.gz

clean:
	@-rm -fr title.basics.tsv title.basics.tsv.gz MovieTweetings.zip MovieTweetings/ 2> /dev/null