# VUDDY (a.k.a. hmark)

VUDDY is an approach for **scalable** and **accurate** vulnerable code clone
detection. This approach is specifically designed to accurately find
vulnerabilities in massive code bases (e.g., Linux kernel, 25 MLoC).
Principles and results are discussed in our
[paper](https://ccs.korea.ac.kr/pds/SNP17.pdf), which was published in 38th
IEEE Symposium on Security and Privacy (S&P'17).

*hmark* is the implementation of VUDDY, which is also the client-side
preprocessing tool for "Vulnerable Code Clone Detection" testing provided by
[IoTcube](https://iotcube.net), an automated vulnerability testing platform.
Details are available [here](https://iotcube.net/userguide/manual/hmark).

This project is a part of the "international collaborative research", which
was conducted by [CSSA](https://cssa.korea.ac.kr) (Center for Software
Security and Assurrance).

## Getting Started with hmark

### Prerequisites
- **Linux or OS X** - *hmark* is designed to work on any of the operating
  systems. Tested OS distributions include Ubuntu 14.04, 16.04, and 18.04,
  Fedora 25, and OS X. Let me know if your OS is not supported.
- **Python 2**, version 2.7.10 or newer - earlier versions may work, but not
  tested.
- **python-tk** package - install from your package manager.
- **Java Runtime Environment (JRE)** - We recommend openjdk-8-jre.

### Running hmark
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

### Binary Release
Instead of running *hmark* from source code, you can also download and execute
prebuilt binaries. Binaries for Windows, Linux, and OS X are available
[here](https://iotcube.net/downloads).

## Reporting Bugs
For reporting bugs, you can [submit an
issue](https://github.com/iotcube/hmark/issues) to the VUDDY GitHub, or send
me an <a href="mailto:seulbae@gatech.edu">email</a>. Feel free to send pull
requests if you have suggestions or bugfixes!

## About
This program is authored and maintained by **Seulbae Kim**
> GitHub [@squizz617](https://github.com/squizz617)

