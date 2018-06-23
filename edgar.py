# -*- coding: utf-8 -*-
from __future__ import print_function
import multiprocessing
import os
import datetime
import zipfile
import tempfile
import logging
import os.path
import sys
from argparse import ArgumentParser

EDGAR_PREFIX = "https://www.sec.gov/Archives/"
SEP = "|"

PY3 = sys.version_info[0] >= 3

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


def _worker_count():
    cpu_count = 1
    try:
        cpu_count = len(os.sched_getaffinity(0))
    except AttributeError:
        cpu_count = multiprocessing.cpu_count()
    return cpu_count


def get_current_quarter():
    return "QTR%s" % ((datetime.date.today().month-1)//3 + 1)


def get_current_year_quarter():
    return "%s-%s" % (datetime.date.today().year, get_current_quarter())


def quarterly_file_list(since_year=1993):
    """
    Generate the list of quarterly zip files archived in EDGAR
    since 1993 until this previous quarter
    """
    logger.debug("generating files since %s" % since_year)
    years = range(since_year, datetime.date.today().year+1)
    quarters = ["QTR1", "QTR2", "QTR3", "QTR4"]
    history = list((y, q) for y in years for q in quarters)
    history.reverse()

    quarter = get_current_quarter()

    while history:
        _, q = history[0]
        if (q == quarter):
            break
        else:
            history.pop(0)

    return [(EDGAR_PREFIX+"edgar/full-index/%s/%s/master.zip" % (x[0], x[1]), "%s-%s.tsv" % (x[0], x[1])) for x in history]


def download_all(dest, since_year):
    """
    Convenient method to download all files at once
    """
    worker_count = _worker_count()
    logger.debug("worker count: %d", worker_count)
    pool = multiprocessing.Pool(worker_count)

    tasks = quarterly_file_list(since_year)
    logger.info("%d files to retrieve", len(tasks))
    for file in tasks:
        pool.apply_async(download, (file, dest))

    pool.close()
    pool.join()
    logger.info("complete")


def append_html_version(line):
    chunks = line.split(SEP)
    return line + SEP + chunks[-1].replace(".txt", "-index.html")


def skip_header(f):
    for x in range(0, 11):
        f.readline()


def url_get(url):
    content = ''
    if PY3:
        # python 3
        import urllib.request
        content = urllib.request.urlopen(url).read()
    else:
        # python 2
        import urllib2
        content = urllib2.urlopen(url).read()
    return content


def download(file, dest):
    """
    Download an idx file or archive from EDGAR
    This will read idx files and unzip archives + read the master.idx file inside
    """
    if not dest.endswith("/"):
        dest = "%s/" % dest

    url = file[0]
    dest_name = file[1]
    if url.endswith("zip"):
        with tempfile.TemporaryFile(mode='w+b') as tmp:
            tmp.write(url_get(url))
            with zipfile.ZipFile(tmp).open("master.idx") as z:
                with open(dest+dest_name, 'w+') as idxfile:
                    skip_header(z)
                    lines = z.read()
                    if PY3:
                        lines = str(lines, "utf-8")
                    lines = map(lambda line: append_html_version(line), lines.splitlines())
                    idxfile.write('\n'.join(lines))
                    logger.info("> downloaded %s to %s%s" % (url, dest, dest_name))
    else:
        raise NotImplementedError("python-edgar only supports zipped index files")

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "-y",
        "--from-year",
        type=int,
        dest="year")

    args = parser.parse_args()
    if not args.year:
        parser.print_help()
        exit()

    dest = tempfile.mkdtemp()
    logger.debug("downloads will be saved to %s" % dest)

    download_all(dest, args.year)
    logger.info("Files downloaded in %s" % dest)
