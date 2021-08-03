from __future__ import print_function
import os
import datetime
import tempfile
import sys
from argparse import ArgumentParser
import logging

import edgar

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)


if __name__ == "__main__":
    
    if sys.version_info[0] < 3:
        raise Exception("Must be using Python 3")
    
    parser = ArgumentParser()
    parser.add_argument(
        "-y",
        "--from-year",
        type=int,
        dest="year",
        help="The year from which to start downloading "
        + "the filing index. Default to current year",
        default=datetime.date.today().year,
    )

    parser.add_argument(
        "-d",
        "--directory",
        dest="directory",
        help="A directory where the filing index files will"
        + "be downloaded to. Default to a temporary directory",
        default=tempfile.mkdtemp(),
    )

    parser.add_argument(
        '-ua',
        "-user-agent",
        dest="ua",
        help="The User Agent to set. This must be set properly "
        + "else the SEC may temporarily ban you. See https://www.sec.gov/os/accessing-edgar-data"
    )
    
    args = parser.parse_args()

    if args.ua is None:
        logger.error("A user agent is required. See https://www.sec.gov/os/accessing-edgar-data")
        sys.exit(1)
        
    logger.debug("downloads will be saved to %s" % args.directory)

    edgar.download_index(args.directory, args.year, args.ua)
    logger.info("Files downloaded in %s" % args.directory)
