# NVD CVE crawler

## Modules
File Name           | Description
--------------------|------------
cveXmlDownloader.py	| Downloads XML files from NVD
cveXmlParser.py		| Parses and generates cvedata.pkl
cveXmlUpdater.py	| Downloads updated records from NVD and update cvedata.pkl

## How to use
1. Running for the first time
Run cveXmlDownloader.py, cveXmlParser.py, and cveXmlUpdater.py in a row.

2. Later use
If you already have a cvedata.pkl, run cveXmlUpdater.py for updates.

