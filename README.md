# VUDDY (a.k.a. hmark)
VUDDY: A Scalable Approach for Vulnerable Code Clone Discovery.
This project is part of the international collaborative research which is being by CSSA (Center for Software Security and Assurrance).
The implementation targeted IEEE S&P (submission due: Nov. 11, 2016)

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
<!-- 

1. Library
  + parseutility.py
2. Vulnerability Retrievers
  + get_cvepatch_from_git.py
  + get_source_from_cvepatch.py
3. Hash-index Generators
  + hidxgen_src.py
  + hidxgen_vul.py

You don't have to worry about the rest of the files.

I just don't wanna be bothered by cleanups. -->

## Documentation
### parseutility.py

#### loadSource()
Load every C/C++/C# files.
* Input: (string) Path to the root directory
* Output: (list) List of every source files

#### loadVul()
Load every .vul files.
* Input: (string) Path to the root directory
* Output: (list) List of every .vul files

#### parseFile()
Parse functions from the specified file.
* Input: (string) Name and path to the file
* Output: (list) of function class instances

#### removeComment()
Removes C/C++ style comments from a given string.
* Input: (string) source code
* Output: (string) source code w/o comments

#### normalize()
Normalizes the input string: LF, TABs, curly braces, spaces are removed.
Then, all characters are lowercased.
* Input: (string) original string
* Output: (string) normalized string

#### abstract()
Apply abstraction on the function instance, and then return a tuple of the original body and abstracted body.
* Input: (class instance) instance, (int) abstraction level
* Output: tuple ( (string) originalFunctionBody, (string) abstractBody )


