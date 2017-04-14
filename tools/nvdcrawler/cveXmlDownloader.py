"""
Download and store NVD's CVE data in XML.
See https://nvd.nist.gov/vuln/data-feeds#CVE_FEED for information.
"""

import os
import datetime
import common

DLDir = "CVEXML"

try:
    os.mkdir("CVEXML")
except OSError:
    pass

urlBase = "https://static.nvd.nist.gov/feeds/xml/cve/"

pwd = os.getcwd()
os.chdir(DLDir)

for year in range(2002, datetime.datetime.now().year + 1):
    fileName = "nvdcve-2.0-" + str(year) + ".xml.zip"
    url = urlBase + fileName

    common.download_url(url, fileName)
    common.unzip(fileName)
    os.remove(fileName)
