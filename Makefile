.PHONY:	title_basics.py	clean

title_basics.py:	title.basics.tsv

title.basics.tsv:	title.basics.tsv.gz
	gunzip title.basics.tsv.gz

title.basics.tsv.gz:
	wget https://datasets.imdbws.com/title.basics.tsv.gz

clean:
	-rm title.basics.tsv title.basics.tsv.gz