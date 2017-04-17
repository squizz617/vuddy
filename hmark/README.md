# hmark - Hash index generator for IoTcube's vulnerable code clone detection.
*hmark* is the preprocessor for the "vulnerable code clone detection" 
in IoTcube (https://iotcube.korea.ac.kr). 

## How to run
This documentation addresses how to run hmark on various platforms,
on the basis of *hmark* version 3.0.3. 
*hmark* has no application-specific requirements.

### Running on Linux
Ubuntu 14.04 and 16.04 (32 and 64-bits) are officially supported by *hmark*.
1. Change access permissions if necesary.
    - 32-bit system: $ sudo chmod a+x hmark_3.0.3_linux_x86
    - 64-bit system: $ sudo chmod a+x hmark_3.0.3_linux_x64
2. Run with or without optional arguments.
    - In terminal:
        - 32-bit system: $ ./hmark_3.0.3_linux_x86 [-h] [-c path ON/OFF] [-n] [-V]
        - 64-bit system: $ ./hmark_3.0.3_linux_x64 [-h] [-c path ON/OFF] [-n] [-V]
    - Graphic user interface:
        - You can launch app in GUI (e.g., in Nautilus), 
          but you cannot pass command line arguments.

### Running on Mac OS X (macOS)
*hmark* for MAC supports 64-bit architecture.
1. Change access permissions if necessary.
    - $ sudo chmod a+x hmark_3.0.3_osx
2. Run with or without optional arguments.
    - In terminal:
        - $ ./hmark_3.0.3_osx [-h] [-c path ON/OFF] [-n] [-V]

### Running on Windows
*hmark* works on both 32-bit and 64-bit windows.
The execution is tested on Windows 7, 8, and 10.
1. Execute the application.
    - In terminal:
        - hmark_3.0.3_win.exe [-h] [-c path ON/OFF] [-n] [-V]
    - Graphic user interface:
        - You can launch app in GUI (e.g., in Explorer),
          but you cannot pass command line arguments.

## Optional arguments
You can see the help message below by passing an `-h` (or `--help`) argument.
```
usage: ./hmark_3.0.3_linux_x64 [-h] [-c path ON/OFF] [-n] [-V]

- optional arguments:
    -h, --help            show this help message and exit
    
  -c path ON/OFF, --cli-mode path ON/OFF
                        run hmark without GUI by specifying the path to the
                        target directory, and the abstraction mode
  -n, --no-updatecheck  bypass update checking (not recommended)
  -V, --version         print hmark version and exit
```

## Troubleshooting
1. Cannot execute *hmark* in GUI mode.
    - Some systems might require you to install several packages.
        - Oftentimes, `sudo apt-get install python-tk` will do.
        - If not, please contact us (cssa@korea.ac.kr) with the error message.
    - You can still use the same functionality as GUI in cli-mode (option `-c`).
2. App does not run.
    - Check the path to *hmark*
        - The path should not have any non-ascii, unicode characters.