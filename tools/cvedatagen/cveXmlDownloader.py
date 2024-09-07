#!/usr/bin/env python
"""
Download and store NVD's CVE data in XML.
See https://nvd.nist.gov/vuln/data-feeds#CVE_FEED for information.
"""

import os
import datetime
import common
originalDir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def process():
    DLDir = os.path.join(originalDir, "data", "CVEXML")

    try:
        os.makedirs(DLDir)
    except OSError:
        pass

    # NVD's XML Vulnerability Feeds have been deprecated. Use JSON instead..
    # https://nvd.nist.gov/feeds/json/cve/1.1/nvdcve-1.1-2002.json.zip
    urlBase = "https://nvd.nist.gov/feeds/json/cve/1.1/"

    os.chdir(DLDir)

    for year in range(2002, datetime.datetime.now().year + 1):
        fileName = "nvdcve-1.1-{0}.json.zip".format(year)
        url = urlBase + fileName

        common.download_url(url, fileName)
        common.unzip(fileName)
        os.remove(fileName)


if __name__ == '__main__':
    process()
