from .downloader import FTP_ADDR, file_list, download, download_all

"""
find . -name "*.pyc" -exec rm -rf {} \;

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

import glob
for idx in glob.glob("/tmp/*.idx"):
	print idx
"""