# Vulnerability database generator for VUDDY

## Prerequisite
* python 2.7.x
* Git

## Crawling CVE raw data from NVD
1. `cd NVDCVEcrawler`
2. `$ python cveXmlDownloader.py` downloads XML files from NVD (https://nvd.nist.gov)
3. `$ python cveXmlParser.py` parses XML files and generates `cvedata.pkl`
4. `$ python cveXmlUpdater.py` downloades updated records from NVD and updates `cvedata.pkl`
5. Copy or move the resulting data file (`cvedata.pkl`) to the working directory.

## How to establish vulnerability database
1. Clone git repository: `$ git clone [REPO]`
2. Fetch diff patches: `$ python get_cvepatch_from_git.py [REPO] [-m: multimode]`
3. Reconstruct old functions from diff: `$ python get_source_from_cvepatch.py [REPO] [-m: multimode]`
4. Remove duplicate old functions: `$ python vul_dup_remover.py`
5. Filter out wrong functions: `$ python verify_vul.py`
6. Generate hidx of old fuenctions: `$ python hidxgen_vul.py [REPO] [ABSTRACTION LEVEL]`

## Other key modules
File Name       | Description
--------------- | -----------
parseutility.py | Library which handles parser output

