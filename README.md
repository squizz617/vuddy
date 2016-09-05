# Advanced version of DiscoVULer
This version targets IEEE S&P (submission due: Nov. 11)

## Key Modules
1. Library
  + parseutility.py
2. Vulnerability Retrievers
  + get_cvepatch_from_git.py
  + get_source_from_cvepatch.py
3. Hash-index Generators
  + hidxgen_src.py
  + hidxgen_vul.py

You don't have to worry about the rest of the files.

I just don't wanna be bothered by cleanups.

## Documentation
### parseutility.py

#### loadSource()
Load every C/C++/C# files.
Input: (string) Path to the root directory
Output: (list) List of every source files

#### loadVul()
Load every .vul files.
Input: (string) Path to the root directory
Output: (list) List of every .vul files

#### removeComment()
Removes C/C++ style comments from a given string.
Input: (string) source code
Output: (string) source code w/o comments

#### normalize()
Normalizes the input string: LF, TABs, curly braces, spaces are removed.
Then, all characters are lowercased.
Input: (string) original string
Output: (string) normalized string

