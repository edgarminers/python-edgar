[![Build Status](https://travis-ci.org/edouardswiac/python-edgar.svg?branch=master)](https://travis-ci.org/edouardswiac/python-edgar)


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

## Using python-edgar as a library

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

## Using python-edgar as a standalone script

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


### License

MIT

[Edouard Swiac]: edouard.swiac@gmail.com
