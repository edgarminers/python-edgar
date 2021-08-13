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
import time

EDGAR_PREFIX = "https://www.sec.gov/Archives/"
SEP = "|"
IS_PY3 = sys.version_info[0] >= 3
REQUEST_BUDGET_MS = 200

def _get_current_quarter():
    return "QTR%s" % ((datetime.date.today().month - 1) // 3 + 1)


def _quarterly_idx_list(since_year=1993):
    """
    Generate the list of quarterly zip files archived in EDGAR
    since 1993 until this previous quarter
    """
    logging.debug("downloading files since %s" % since_year)
    years = range(since_year, datetime.date.today().year + 1)
    quarters = ["QTR1", "QTR2", "QTR3", "QTR4"]
    history = list((y, q) for y in years for q in quarters)
    history.reverse()

    quarter = _get_current_quarter()

    while history:
        _, q = history[0]
        if q == quarter:
            break
        else:
            history.pop(0)

    return [
        (
            EDGAR_PREFIX + "edgar/full-index/%s/%s/master.zip" % (x[0], x[1]),
            "%s-%s.tsv" % (x[0], x[1]),
        )
        for x in history
    ]


def _append_html_version(line):
    chunks = line.split(SEP)
    return line + SEP + chunks[-1].replace(".txt", "-index.html")


def _skip_header(f):
    for x in range(0, 11):
        f.readline()


def _url_get(url, user_agent):
    content = None
    if IS_PY3:
        # python 3
        import urllib.request
        hdr = { 'User-Agent' : user_agent }
        req = urllib.request.Request(url, headers=hdr)
        content =urllib.request.urlopen(req).read()
    else:
        # python 2
        import urllib2

        content = urllib2.urlopen(url).read()
    return content


def _download(file, dest, skip_file, user_agent):
    """
    Download an idx archive from EDGAR
    This will read idx files and unzip
    archives + read the master.idx file inside

    when skip_file is True, it will skip the file if it's already present.
    """
    if not dest.endswith("/"):
        dest = "%s/" % dest

    url = file[0]
    dest_name = file[1]
    if skip_file and os.path.exists(dest+dest_name):
        logging.info("> Skipping %s" % (dest_name))
        return

    if url.endswith("zip"):
        with tempfile.TemporaryFile(mode="w+b") as tmp:
            tmp.write(_url_get(url, user_agent))
            with zipfile.ZipFile(tmp).open("master.idx") as z:
                with io.open(dest + dest_name, "w+", encoding="utf-8") as idxfile:
                    _skip_header(z)
                    lines = z.read()
                    if IS_PY3:
                        lines = lines.decode("latin-1")
                    lines = map(
                        lambda line: _append_html_version(line), lines.splitlines()
                    )
                    idxfile.write("\n".join(lines)+"\n")
                    logging.info("> downloaded %s to %s%s" % (url, dest, dest_name))
    else:
        raise logging.error("python-edgar only supports zipped index files")


def _get_millis():
    return round(time.time() * 1000)

def download_index(dest, since_year, user_agent, skip_all_present_except_last=False):
    """
    Convenient method to download all files at once
    """
    if not os.path.exists(dest):
        os.makedirs(dest)

    tasks = _quarterly_idx_list(since_year)
    logging.info("%d index files to retrieve", len(tasks))
    last_download_at = _get_millis()
    for i, file in enumerate(tasks):
        skip_file = skip_all_present_except_last
        if i == 0:
            # First one should always be re-downloaded
            skip_file = False
        # naive: 200ms or 5QPS serialized
        start = _get_millis()
        _download(file, dest, skip_file, user_agent)
        elapsed = _get_millis() - start
        if elapsed < REQUEST_BUDGET_MS:
            sleep_for = REQUEST_BUDGET_MS-elapsed
            logging.info("sleeping for %dms because we are going too fast (previous request took %dms", sleep_for, elapsed)
            time.sleep(sleep_for/1000)
        last_download_at = _get_millis()


    logging.info("complete")
