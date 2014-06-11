# -*- coding: utf-8 -*-
from __future__ import print_function

try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO

import datetime
import csv
import zipfile
import tempfile
import logging
import edgar

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("edgar")

FTP_ADDR = "ftp.sec.gov"
EDGAR_PREFIX = "ftp://%s/" % FTP_ADDR

def quarterly_file_list(since_year):
    """
    Generate the list of quarterly zip files archived in EDGAR
    since 1993 until this previous quarter
    """
    logger.debug("generating files since %s" % since_year)
    years = xrange(since_year, datetime.date.today().year+1)
    quarters = ["QTR1", "QTR2", "QTR3", "QTR4"]
    current_quarter =  ((datetime.date.today().month-1)//3 + 1)
    history =  list((y, q) for y in years for q in quarters)
    history.reverse()

    quarter = "QTR%s" % current_quarter
    while history:
        _, q = history[0]
        if (q == quarter):
            history.pop(0)
            break
        else:
            history.pop(0)

    return ["edgar/full-index/%s/%s/master.zip" % (x[0], x[1]) for x in history]


def daily_file_list(ftp):
    """ Generate the list of daily index files archived in EDGAR for the current quarter """
    files = []
    ftp.retrlines("NLST edgar/daily-index", files.append)
    return [f for f in files if f.startswith("edgar/daily-index/master")]


def file_list(ftp, since=1993):
    """ Complete file list (idx+zip) from 1993 to current quarter """
    return daily_file_list(ftp) + quarterly_file_list(since)


def ftp_retr(ftp, filename, buffer):
    """ Write remote filename's bytes from ftp to local buffer """
    ftp.retrbinary('RETR %s' % filename, buffer.write)
    logger.debug("FTP RETR %s" % filename)
    return buffer


def download_all(ftp, dest=""):
    """
    Convenient method to download all files at once
    """
    if not dest:
         dest = tempfile.mkdtemp()

    for file in file_list(ftp):
        download(ftp, file, dest)

def download(ftp, file, dest):
    """
    Download an idx file or archive from EDGAR
    This will read idx files and unzip archives + read the master.idx file inside
    """
    if not dest.endswith("/"):
        dest = "%s/" % dest

    logger.info("downloading %s file in %s" % (file, dest))

    if file.startswith(EDGAR_PREFIX):
        file = file[len(EGAR_PREFIX):]

    if file.endswith("idx"):
        dest_name = file.replace("/", ".")

        with tempfile.TemporaryFile() as tmp:
            ftp_retr(ftp, file, tmp)
            tmp.seek(0) 
            for x in xrange(0,7): # remove csv headers
                tmp.readline()
            tmp.seek(0, 1) #reset

            with open(dest+dest_name, 'w') as idxfile:
                idxfile.write(tmp.read())
        logger.debug("wrote %s" % dest+dest_name)

    elif file.endswith("zip"):
        dest_name = file.replace("/", ".").replace("zip", "idx")
        buffer = StringIO()
        ftp_retr(ftp, file, buffer)
        with zipfile.ZipFile(buffer).open("master.idx") as z:
            for x in xrange(0,10):
                z.readline()
            with open(dest+dest_name, 'w') as idxfile:
                idxfile.write(z.read())
        logger.debug("wrote %s" % dest+dest_name)
    else:
        raise NotImplementedError("python-edgar only supports .idx and .zip files")
