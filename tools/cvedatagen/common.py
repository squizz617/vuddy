import urllib2
import sys
from zipfile import ZipFile
from xml.etree.ElementTree import parse
import json
import os


def download_url(url, fileName):
    u = urllib2.urlopen(url)
    f = open(fileName, "wb")
    meta = u.info()
    fileSize = int(meta.getheaders("Content-Length")[0])
    print "Downloading: %s (%s bytes)" % (fileName, fileSize)

    downloadedSize = 0
    blockSize = 8192
    barSize = 30
    while True:
        buffer = u.read(blockSize)
        if not buffer:
            break

        downloadedSize += len(buffer)
        f.write(buffer)
        status = "\r"
        status += "#" * (downloadedSize * barSize / fileSize)
        status += " " * (barSize - downloadedSize * barSize / fileSize)
        status += "%10d  [%3.2f%%]" % (downloadedSize, downloadedSize * 100. / fileSize)
        # status += chr(8)*(len(status)+1)
        sys.stdout.write(status)
        sys.stdout.flush()

    sys.stdout.write("\n")
    f.close()


def unzip(fileName):
    print "Extracting: " + fileName,
    zip = ZipFile(fileName)
    zip.extractall()
    zip.close()
    print " [DONE]"


def parse_xml(xmlFile):
    print "Processing: " + xmlFile,
    if not xmlFile.endswith(".json"):
        return {}

    update_count = 0
    new_count = 0
    subDict = {}
    cveid = ""
    cvss = ""
    cweid = ""
    reference = []
    summary = ""

    with open(xmlFile) as f:
        json_obj = json.load(f)

    cve_dict = json_obj["CVE_Items"]
    for cve in cve_dict:
        cveid = cve["cve"]["CVE_data_meta"]["ID"]
        try:
            cweid = cve["cve"]["problemtype"]["problemtype_data"][0]["description"][0]["value"]
        except:
            cweid = "CWE-000"

        try:
            cvss = cve["impact"]["baseMetricV2"]["cvssV2"]["baseScore"]
        except:
            cvss = "0.0"

        if cveid in subDict:
            update_count += 1
        else:
            new_count += 1

        subDict[cveid] = [cvss, cweid, reference, summary]

    print "[Updated %s records, added %s new records]" % (update_count, new_count)
    return subDict
