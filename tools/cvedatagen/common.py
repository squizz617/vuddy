import urllib2
import sys
from zipfile import ZipFile
from xml.etree.ElementTree import parse
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
    update_count = 0
    new_count = 0
    subDict = {}
    tree = parse(xmlFile)
    root = tree.getroot()

    cveid = ""
    cvss = ""
    cweid = ""
    reference = []
    summary = ""

    for element in root.iter():
        tag = element.tag
        text = element.text
        attrib = element.attrib

        if "cve-id" in tag:
            cveid = text
        elif "score" in tag:
            cvss = text
        elif "cwe" in tag:
            cweid = attrib["id"]
        elif "reference" == tag[-9:]:
            reference.append(attrib["href"])
        elif "summary" in tag:
            summary = text.encode('utf-8')

            if cveid in subDict:
                update_count += 1
            else:
                new_count += 1

            subDict[cveid] = [cvss, cweid, reference, summary]

    print "[Updated %s records, added %s new records]" % (update_count, new_count)
    return subDict
