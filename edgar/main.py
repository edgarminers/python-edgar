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
import io

EDGAR_PREFIX = "https://www.sec.gov/Archives/"
SEP = "|"
IS_PY3 = sys.version_info[0] >= 3


def _worker_count():
    cpu_count = 1
    try:
        cpu_count = len(os.sched_getaffinity(0))
    except AttributeError:
        cpu_count = multiprocessing.cpu_count()
    return cpu_count


def _get_current_quarter():
    return "QTR%s" % ((datetime.date.today().month-1)//3 + 1)


def _quarterly_idx_list(since_year=1993):
    """
    Generate the list of quarterly zip files archived in EDGAR
    since 1993 until this previous quarter
    """
    logging.debug("downloading files since %s" % since_year)
    years = range(since_year, datetime.date.today().year+1)
    quarters = ["QTR1", "QTR2", "QTR3", "QTR4"]
    history = list((y, q) for y in years for q in quarters)
    history.reverse()

    quarter = _get_current_quarter()

    while history:
        _, q = history[0]
        if (q == quarter):
            break
        else:
            history.pop(0)

    return [
        (EDGAR_PREFIX+"edgar/full-index/%s/%s/master.zip" % (x[0], x[1]),
         "%s-%s.tsv" % (x[0], x[1])) for x in history]


def _append_html_version(line):
    chunks = line.split(SEP)
    return line + SEP + chunks[-1].replace(".txt", "-index.html")


def _skip_header(f):
    for x in range(0, 11):
        f.readline()


def _url_get(url):
    content = None
    if IS_PY3:
        # python 3
        import urllib.request
        content = urllib.request.urlopen(url).read()
    else:
        # python 2
        import urllib2
        content = urllib2.urlopen(url).read()
    return content


def _download(file, dest):
    """
    Download an idx archive from EDGAR
    This will read idx files and unzip
    archives + read the master.idx file inside
    """
    if not dest.endswith("/"):
        dest = "%s/" % dest

    url = file[0]
    dest_name = file[1]
    if url.endswith("zip"):
        with tempfile.TemporaryFile(mode='w+b') as tmp:
            tmp.write(_url_get(url))
            with zipfile.ZipFile(tmp).open("master.idx") as z:
                with io.open(dest+dest_name, 'w+', encoding='utf-8') as idxfile:
                    _skip_header(z)
                    lines = z.read()
                    if IS_PY3:
                        lines = lines.decode("latin-1")
                    lines = map(lambda line: _append_html_version(line),
                                lines.splitlines())
                    idxfile.write('\n'.join(lines))
                    logging.info("> downloaded %s to %s%s" % (url,
                                                              dest, dest_name))
    else:
        raise logging.error("python-edgar only supports zipped index files")


def download_index(dest, since_year):
    """
    Convenient method to download all files at once
    """
    if not os.path.exists(dest):
        os.makedirs(dest)

    tasks = _quarterly_idx_list(since_year)
    logging.info("%d index files to retrieve", len(tasks))

    worker_count = _worker_count()
    logging.debug("worker count: %d", worker_count)
    pool = multiprocessing.Pool(worker_count)

    for file in tasks:
        pool.apply_async(_download, (file, dest))

    pool.close()
    pool.join()
    logging.info("complete")
