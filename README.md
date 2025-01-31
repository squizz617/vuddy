# Vuddy 프로젝트를 기존에 Python 2와 3을 동시에 사용해야 했던 환경에서, 이제는 Python 3만으로 동작하도록 수정하였습니다.

# VUDDY (a.k.a. `hmark`)
VUDDY is an approach for **scalable** and **accurate** vulnerable code clone
detection. This approach is specifically designed to accurately find
vulnerabilities in massive code bases (e.g., Linux kernel, 25 MLoC).
Its principles and results are discussed in our
[paper](https://ccs.korea.ac.kr/pds/SNP17.pdf), which was published in 38th
IEEE Symposium on Security and Privacy (S&P'17).

`hmark` is the implementation of VUDDY. It is the client-side preprocessing
tool for "Vulnerable Code Clone Detection" testing provided by
[IoTcube](https://iotcube.net), an automated vulnerability testing platform.
Detailed instructions are available [here](https://iotcube.net/userguide/manual/hmark).

This project is a part of the "international collaborative research", which
was conducted by [CSSA](https://cssa.korea.ac.kr) (Center for Software
Security and Assurrance).

## Getting Started with `hmark`

### Prerequisites
- **Linux or OS X** - *hmark* is designed to work on any of the operating
  systems. Tested OS distributions include Ubuntu 14.04, 16.04, and 18.04,
  Fedora 25, and OS X. Let me know if your OS is not supported.
  - Confirmed in May 2024: VUDDY works seamlessly on Ubuntu 22.04, but you need
    to install Python 2
- **Python 2**, version 2.7.10 or newer - earlier versions may work, but not
  tested.
- **python-tk** package - (only required if you want GUI) install from your
  package manager
- **Java Runtime Environment (JRE)** - We recommend openjdk-8-jre.

### Running `hmark` and checking the result on IoTcube (our web service)
1. `cd hmark`
2. `python hmark.py [-h] [-c path ON/OFF] [-n] [-V]`

You can see the help message below by passing an `-h` (or `--help`) argument.
```
usage: python hmark.py [-h] [-c path ON/OFF] [-n] [-V]

- optional arguments:
  -h, --help            show this help message and exit

  -c path ON/OFF, --cli-mode path ON/OFF
                        run hmark without GUI by specifying the path to the
                        target directory, and the abstraction mode
  -n, --no-updatecheck  bypass update checking (not recommended)
  -V, --version         print hmark version and exit
```
3. Upload the resulting `hidx` file on IoTcube's [Vulnerable Code Clone
   Detection](https://iotcube.net/process/type/wf1) testing.

### Running `hmark` and checking the result locally
Follow steps 1 and 2 above to generate the `hidx` of the target program.
Skip step 3.

4. To build your own vulnerability database, checkout `vulnDBGen`,
  which is a subrepo of this repository and follow the guidelines
  to build a vulnerability database locally.
  ```
  $ git submodule update --init
  $ cd vulnDBGen
  $ cat docs/examples.md
  ```

5. After building your own vulnerability database, you can locally run the
   vulnerable clone checker:
  ```
  $ cd ..
  $ python3 checker/check_clones.py --help
  $ python3 checker/check_clones.py --target path_to_target_hidx --database path_to_vulndb
  ```

### Binary Release
Instead of running `hmark` from source code, you can also download and execute
prebuilt binaries. Binaries for Windows, Linux, and OS X are available
[here](https://iotcube.net/downloads).

## Reporting Bugs
For reporting bugs, you can [submit an
issue](https://github.com/iotcube/hmark/issues) to the VUDDY GitHub, or send
me an <a href="mailto:seulbae@gatech.edu">email</a>. Feel free to send pull
requests if you have suggestions or bugfixes!

## About
This program is authored and maintained by **Seulbae Kim**
> GitHub [@seulbae-security](https://github.com/seulbae-security) / seulbae@postech.ac.kr

## TODOs
Please feel free to submit pull requests for the following items:
* Rewrite everything in Python3
* Use a better parser
* Replace all code that rely on stdin/stdout for IPC (e.g., git executions) with API calls

