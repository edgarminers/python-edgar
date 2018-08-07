[![Build Status](https://travis-ci.org/edouardswiac/python-edgar.svg?branch=master)](https://travis-ci.org/edouardswiac/python-edgar)
![PyPI](https://img.shields.io/pypi/v/python-edgar.svg)
![PyPI - License](https://img.shields.io/pypi/l/python-edgar.svg)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/python-edgar.svg)

# Build a master index of SEC filings since 1993 with `python-edgar`

The SEC filings index is split in quarterly files since 1993 (1993-QTR1, 1993-QTR2...). By using `python-edgar` and some scripting, you can easily rebuild a master index of all filings since 1993 by stitching quarterly index files together. The master index file can be then feed to a database, a pandas dataframe, stata, etc... 

An index file is a csv-like (pipe `|` separated) file that contains the following information:
  - Company name (eg. ```TWITTER, INC```)
  - Company CIK (eg.``` 0001418091```)
  - Filling date (eg. ```2013-10-03```)
  - Filling type (eg. ```S1```)
  - Filling URL on EDGAR (```edgar/data/1418091/0001193125-13-390321.txt```)

Once `python-edgar` is finished downloading index files, you can open an index file with ```csv.csvreader``` or ```pandas.read_csv```  to have the data programmatically usable. Remember that the delimiter character is `|`!

`python-edgar` can be used as a library called from another python script, or as a standalone script.

## Features 
- Fast: parallel downloads with `multiprocessing`. The more CPUs you have the faster it'll go.
- Efficient: retrieve compressed archives instead of raw index file that are 10 times bigger
- Import as a library in your python project or run as a standalone script 
- Python 2 & 3 Compatible with external 0 dependencies.

## Usage

### Using python-edgar as a library

Install from pip in a virtualenv
```sh
pip install python-edgar
```

Call the library
```python
import edgar
edgar.download_index(download_directory, since_year)
```
Output
```shell
2018-06-23 12:41:46,451 - DEBUG - downloads will be saved to /var/folders/bv/2zbdkyyj14766dcw07x6zrrr0000gn/T/tmpr2Nk3o
2018-06-23 12:41:46,451 - DEBUG - downloading files since 2017
2018-06-23 12:41:46,451 - INFO - 6 index files to retrieve
2018-06-23 12:41:46,465 - DEBUG - worker count: 4
2018-06-23 12:41:48,359 - INFO - > downloaded https://www.sec.gov/Archives/edgar/full-index/2017/QTR3/master.zip to /var/folders/bv/2zbdkyyj14766dcw07x6zrrr0000gn/T/tmpr2Nk3o/2017-QTR3.tsv
2018-06-23 12:41:48,611 - INFO - > downloaded https://www.sec.gov/Archives/edgar/full-index/2018/QTR2/master.zip to /var/folders/bv/2zbdkyyj14766dcw07x6zrrr0000gn/T/tmpr2Nk3o/2018-QTR2.tsv
2018-06-23 12:41:48,649 - INFO - > downloaded https://www.sec.gov/Archives/edgar/full-index/2017/QTR4/master.zip to /var/folders/bv/2zbdkyyj14766dcw07x6zrrr0000gn/T/tmpr2Nk3o/2017-QTR4.tsv
2018-06-23 12:41:48,935 - INFO - > downloaded https://www.sec.gov/Archives/edgar/full-index/2018/QTR1/master.zip to /var/folders/bv/2zbdkyyj14766dcw07x6zrrr0000gn/T/tmpr2Nk3o/2018-QTR1.tsv
2018-06-23 12:41:49,750 - INFO - > downloaded https://www.sec.gov/Archives/edgar/full-index/2017/QTR2/master.zip to /var/folders/bv/2zbdkyyj14766dcw07x6zrrr0000gn/T/tmpr2Nk3o/2017-QTR2.tsv
2018-06-23 12:41:50,237 - INFO - > downloaded https://www.sec.gov/Archives/edgar/full-index/2017/QTR1/master.zip to /var/folders/bv/2zbdkyyj14766dcw07x6zrrr0000gn/T/tmpr2Nk3o/2017-QTR1.tsv
2018-06-23 12:41:50,376 - INFO - complete
2018-06-23 12:41:50,377 - INFO - Files downloaded in /var/folders/bv/2zbdkyyj14766dcw07x6zrrr0000gn/T/tmpr2Nk3o
```

### Using python-edgar as a standalone script

- Download this repository as a zip ("Clone or Download" green button, > Download as zip.) 
- Open your terminal inside that directory and run `python run.py -h`. You can specify a destination directory for downloaded index files like `-d edgar-idx` (defaults to a temporary directory) and/or specify the year from which you want to build the index with `-y 2017` (defaults to current year).

```shell
 $ python run.py -y 2017
2018-06-23 12:41:46,451 - DEBUG - downloads will be saved to /var/folders/bv/2zbdkyyj14766dcw07x6zrrr0000gn/T/tmpr2Nk3o
2018-06-23 12:41:46,451 - DEBUG - downloading files since 2017
2018-06-23 12:41:46,451 - INFO - 6 index files to retrieve
2018-06-23 12:41:46,465 - DEBUG - worker count: 4
2018-06-23 12:41:48,359 - INFO - > downloaded https://www.sec.gov/Archives/edgar/full-index/2017/QTR3/master.zip to /var/folders/bv/2zbdkyyj14766dcw07x6zrrr0000gn/T/tmpr2Nk3o/2017-QTR3.tsv
2018-06-23 12:41:48,611 - INFO - > downloaded https://www.sec.gov/Archives/edgar/full-index/2018/QTR2/master.zip to /var/folders/bv/2zbdkyyj14766dcw07x6zrrr0000gn/T/tmpr2Nk3o/2018-QTR2.tsv
2018-06-23 12:41:48,649 - INFO - > downloaded https://www.sec.gov/Archives/edgar/full-index/2017/QTR4/master.zip to /var/folders/bv/2zbdkyyj14766dcw07x6zrrr0000gn/T/tmpr2Nk3o/2017-QTR4.tsv
2018-06-23 12:41:48,935 - INFO - > downloaded https://www.sec.gov/Archives/edgar/full-index/2018/QTR1/master.zip to /var/folders/bv/2zbdkyyj14766dcw07x6zrrr0000gn/T/tmpr2Nk3o/2018-QTR1.tsv
2018-06-23 12:41:49,750 - INFO - > downloaded https://www.sec.gov/Archives/edgar/full-index/2017/QTR2/master.zip to /var/folders/bv/2zbdkyyj14766dcw07x6zrrr0000gn/T/tmpr2Nk3o/2017-QTR2.tsv
2018-06-23 12:41:50,237 - INFO - > downloaded https://www.sec.gov/Archives/edgar/full-index/2017/QTR1/master.zip to /var/folders/bv/2zbdkyyj14766dcw07x6zrrr0000gn/T/tmpr2Nk3o/2017-QTR1.tsv
2018-06-23 12:41:50,376 - INFO - complete
2018-06-23 12:41:50,377 - INFO - Files downloaded in /var/folders/bv/2zbdkyyj14766dcw07x6zrrr0000gn/T/tmpr2Nk3o
```

## Stitch quarterly files to a master file

`python-edgar` does only one thing and does it well: getting and cleaning uncompressed quarterly index files to your computer. Use command line tools, in the spirit of unix philosophy, to stitch these index files together and create our master index file.

In this example, we called `python run.py` without arguments. It'll download every quarterly index file since 1993.

```shell
 python run.py -y 1993
 
2018-06-23 13:00:16,855 - DEBUG - downloads will be saved to /var/folders/bv/2zbdkyyj14766dcw07x6zrrr0000gn/T/tmpcF1rx7
2018-06-23 13:00:16,855 - DEBUG - downloading files since 1993
2018-06-23 13:00:16,856 - INFO - 102 index files to retrieve
2018-06-23 13:00:16,879 - DEBUG - worker count: 4
2018-06-23 13:00:18,814 - INFO - > downloaded https://www.sec.gov/Archives/edgar/full-index/2017/QTR4/master.zip to /var/folders/bv/2zbdkyyj14766dcw07x6zrrr0000gn/T/tmpcF1rx7/2017-QTR4.tsv
2018-06-23 13:00:19,026 - INFO - > downloaded https://www.sec.gov/Archives/edgar/full-index/2017/QTR3/master.zip to /var/folders/bv/2zbdkyyj14766dcw07x6zrrr0000gn/T/tmpcF1rx7/2017-QTR3.tsv
2018-06-23 13:00:19,157 - INFO - > downloaded https://www.sec.gov/Archives/edgar/full-index/2018/QTR2/master.zip to /var/folders/bv/2zbdkyyj14766dcw07x6zrrr0000gn/T/tmpcF1rx7/2018-QTR2.tsv
2018-06-23 13:00:19,543 - INFO - > downloaded https://www.sec.gov/Archives/edgar/full-index/2018/QTR1/master.zip to /var/folders/bv/2zbdkyyj14766dcw07x6zrrr0000gn/T/tmpcF1rx7/2018-QTR1.tsv
2018-06-23 13:00:20,521 - INFO - > downloaded https://www.sec.gov/Archives/edgar/full-index/2017/QTR2/master.zip to /var/folders/bv/2zbdkyyj14766dcw07x6zrrr0000gn/T/tmpcF1rx7/2017-QTR2.tsv
2018-06-23 13:00:20,719 - INFO - > downloaded https://www.sec.gov/Archives/edgar/full-index/2016/QTR4/master.zip to /var/folders/bv/2zbdkyyj14766dcw07x6zrrr0000gn/T/tmpcF1rx7/2016-QTR4.tsv
2018-06-23 13:00:21,016 - INFO - > downloaded https://www.sec.gov/Archives/edgar/full-index/2016/QTR3/master.zip to /var/folders/bv/2zbdkyyj14766dcw07x6zrrr0000gn/T/tmpcF1rx7/2016-QTR3.tsv
2018-06-23 13:00:21,134 - INFO - > downloaded https://www.sec.gov/Archives/edgar/full-index/2017/QTR1/master.zip to /var/folders/bv/2zbdkyyj14766dcw07x6zrrr0000gn/T/tmpcF1rx7/2017-QTR1.tsv
2018-06-23 13:00:22,099 - INFO - > downloaded https://www.sec.gov/Archives/edgar/full-index/2016/QTR2/master.zip to /var/folders/bv/2zbdkyyj14766dcw07x6zrrr0000gn/T/tmpcF1rx7/2016-QTR2.tsv
(...)
dcw07x6zrrr0000gn/T/tmpcF1rx7/1993-QTR2.tsv
2018-06-23 13:00:54,378 - INFO - > downloaded https://www.sec.gov/Archives/edgar/full-index/1993/QTR1/master.zip to /var/folders/bv/2zbdkyyj14766dcw07x6zrrr0000gn/T/tmpcF1rx7/1993-QTR1.tsv
2018-06-23 13:00:54,423 - INFO - complete
2018-06-23 13:00:54,424 - INFO - Files downloaded in /var/folders/bv/2zbdkyyj14766dcw07x6zrrr0000gn/T/tmpcF1rx7
```

Inspect the directory where our files where downloaded:
```shell
$ ls -lh /var/folders/bv/2zbdkyyj14766dcw07x6zrrr0000gn/T/tmpcF1rx7
total 4964656
drwx------  104 eswiac  staff   3.3K Jun 23 13:00 .
drwxr-xr-x  342 eswiac  staff    11K Jun 23 13:01 ..
-rw-r--r--    1 eswiac  staff   585B Jun 23 13:00 1993-QTR1.tsv
-rw-r--r--    1 eswiac  staff   580B Jun 23 13:00 1993-QTR2.tsv
-rw-r--r--    1 eswiac  staff   1.0K Jun 23 13:00 1993-QTR3.tsv
-rw-r--r--    1 eswiac  staff   2.8K Jun 23 13:00 1993-QTR4.tsv
-rw-r--r--    1 eswiac  staff   2.9M Jun 23 13:00 1994-QTR1.tsv
-rw-r--r--    1 eswiac  staff   2.3M Jun 23 13:00 1994-QTR2.tsv
(...)
-rw-r--r--    1 eswiac  staff    27M Jun 23 13:00 2017-QTR3.tsv
-rw-r--r--    1 eswiac  staff    27M Jun 23 13:00 2017-QTR4.tsv
-rw-r--r--    1 eswiac  staff    41M Jun 23 13:00 2018-QTR1.tsv
-rw-r--r--    1 eswiac  staff    31M Jun 23 13:00 2018-QTR2.tsv
```

Head to that directory so we can merge these files into a master file using `cat`
```shell
$ cd  /var/folders/bv/2zbdkyyj14766dcw07x6zrrr0000gn/T/tmpcF1rx7
$ cat *.tsv > master.tsv
$ du -h master.tsv
2.3G	master.tsv
```

Now you have this master index file. It's not sorted but that's easy to do (hint: Look into the `sort` command) 

## Grab filings from a specific company
Now that we have downloaded the index files it becomes easy, with a bit of command line scripting, to quickly filter by company and extract URLs to the filings we want with `grep` . In the following example we grep by CIK (1000045), store the output in an intermediate text file, which we re-open with cat and grep again by form 10-K. Prefix the paths with https://www.sec.gov/Archives/ and you'll get the full URL.

```shell
eswiac@mbp python-edgar (master) $ grep -h 1000045 /var/folders/bv/2zbdkyyj14766dcw07x6zrrr0000gn/T/tmpvwOzOU/* > 1000045.txt
eswiac@mbp python-edgar (master) $ cat 1000045.txt | grep -h 10-K
1000045|NICHOLAS FINANCIAL INC|10-K|2015-06-15|edgar/data/1000045/0001193125-15-223218.txt|edgar/data/1000045/0001193125-15-223218-index.html
1000045|NICHOLAS FINANCIAL INC|10-K|2016-06-14|edgar/data/1000045/0001193125-16-620952.txt|edgar/data/1000045/0001193125-16-620952-index.html
1000045|NICHOLAS FINANCIAL INC|10-K|2017-06-14|edgar/data/1000045/0001193125-17-203193.txt|edgar/data/1000045/0001193125-17-203193-index.html
1000045|NICHOLAS FINANCIAL INC|10-K|2018-06-27|edgar/data/1000045/0001193125-18-205637.txt|edgar/data/1000045/0001193125-18-205637-index.html
```

## Query the master index with `q`
https://github.com/harelba/q allows you to run SQL directly on tabular data. 

Use with caution: q does not use indexes so running queries against the master index will be very slow since it's rather large. Sorting the master index or narrowing the data to a smaller subset will make search faster. Ultimately you want to load the master index file into a proper database that's able to handle the size.

Some queries you may want to try
- `q "SELECT COUNT(1) FROM 1999-QTR4.tsv" `
- `q -d"|" "SELECT * FROM master.tsv where c1 = 1418091 and c3 = '10-Q' order by c4"`

## License

MIT

[Edouard Swiac]: edouard.swiac@gmail.com
