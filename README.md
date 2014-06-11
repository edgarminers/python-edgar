Download the SEC EDGAR fillings index with python-edgar
=========

python-edgar downloads the EDGAR fillings index from the SEC FTP. The index is comprised of IDX files. An IDX file is a csv-like file that contains the following information:
  - Company name (eg. ```TWITTER, INC```)
  - Company CIK (eg.``` 0001418091```)
  - Filling date (eg. ```2013-10-03```)
  - Filling type (eg. ```S1```)
  - Filling URL on EDGAR (```edgar/data/1418091/0001193125-13-390321.txt```)


python-edgar takes care of generating the index' file list, download the files and strip the headers so all you have to do is open the files with ```csv.csvreader(idxfile, delimiter="|")``` to have the data programmatically usable.


How to use python-edgar
---
Install from pip in a virtualenv
```sh
pip install python-edgar
```

Download EDGAR index
```python
import edgar
import ftplib
ftp = ftplib.FTP(edgar.FTP_ADDR)
ftp.login()
try:
	edgar.download_all(ftp, "/tmp")
except Exception as e:
	print e
finally:
	ftp.close()
	
>>> INFO:edgar:downloading edgar/daily-index/master.20140417.idx file in /tmp/
INFO:edgar:downloaded edgar/daily-index/master.20140417.idx
INFO:edgar:downloading edgar/daily-index/master.20140418.idx file in /tmp/
INFO:edgar:downloaded edgar/daily-index/master.20140418.idx
INFO:edgar:downloading edgar/daily-index/master.20140421.idx file in /tmp/
```

List the index files downloaded
```python
import glob

>>> In [8]: for idx in glob.glob("/tmp/*.idx"):
   ...:         print idx
   ...:
/tmp/edgar.daily-index.master.20140417.idx
/tmp/edgar.daily-index.master.20140418.idx
/tmp/edgar.daily-index.master.20140421.idx
/tmp/edgar.daily-index.master.20140422.idx
...
```

License
----

MIT

[Edouard Swiac]: edouard.swiac@gmail.com
