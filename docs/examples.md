Vulnerability Database Generator (vulnDBGen) - Use Examples
====

## 1. Configuration Settings
Set `gitStoragePath`, `gitBinary`, `diffBinary`, and `javaBinary` in `config.py`.
```
~$ cd ~/vulnDBGen
~/vulnDBGen$ cat config.py
```
Result
```
import platform

gitStoragePath = r"/home/squizz/gitrepos"
version = "3.0.3" # for use in IoTcube.
pf = platform.platform()
if "Windows" in pf:  # Windows
    gitBinary = r"C:\Program Files\Git\bin\git.exe"
    diffBinary = r"C:\Program Files\Git\usr\bin\diff.exe"
else:  # POSIX
    gitBinary = "git"
    diffBinary = "diff"
    javaBinary = "java"

```

## 2. Cloning repositories and collecting vulnerabilities

### A. ChakraCore (Microsoft)
```
~$ cd ~/gitrepos
~/gitrepos$ git clone https://github.com/Microsoft/ChakraCore.git

~$ cd ~/vulnDBGen
~/vulnDBGen$ python initialize.py
~/vulnDBGen$ python src/get_cvepatch_from_git.py ChakraCore
~/vulnDBGen$ python src/get_source_from_cvepatch.py ChakraCore
```

### B. FreeBSD (FreeBSD Foundation)
```
~$ cd ~/gitrepos
~/gitrepos$ git clone https://github.com/freebsd/freebsd.git

~$ cd ~/vulnDBGen
~/vulnDBGen$ python initialize.py
~/vulnDBGen$ python src/get_cvepatch_from_git.py freebsd
~/vulnDBGen$ python src/get_source_from_cvepatch.py freebsd
```

### C. Gecko (Mozilla)
```
~$ cd ~/gitrepos
~/gitrepos$ git clone https://github.com/mozilla/gecko-dev.git

~$ cd ~/vulnDBGen
~/vulnDBGen$ python initialize.py
~/vulnDBGen$ python src/get_cvepatch_from_git.py gecko-dev
~/vulnDBGen$ python src/get_source_from_cvepatch.py gecko-dev
```

### D. glibc (GNU)
```
~$ cd ~/gitrepos
~/gitrepos$ git clone git://sourceware.org/git/glibc.git

~$ cd ~/vulnDBGen
~/vulnDBGen$ python initialize.py
~/vulnDBGen$ python src/get_cvepatch_from_git.py glibc
~/vulnDBGen$ python src/get_source_from_cvepatch.py glibc
```

### E. httpd (APACHE)
```
~$ cd ~/gitrepos
~/gitrepos$ git clone https://github.com/apache/httpd.git

~$ cd ~/vulnDBGen
~/vulnDBGen$ python initialize.py
~/vulnDBGen$ python src/get_cvepatch_from_git.py httpd
~/vulnDBGen$ python src/get_source_from_cvepatch.py httpd
```

### F. Kerberos Version 5 (MIT)
```
~$ cd ~/gitrepos
~/gitrepos$ git clone https://github.com/krb5/krb5.git

~$ cd ~/vulnDBGen
~/vulnDBGen$ python initialize.py
~/vulnDBGen$ python src/get_cvepatch_from_git.py krb5
~/vulnDBGen$ python src/get_source_from_cvepatch.py krb5
```

### G. Linux kernel (Linux Foundation)
```
~$ cd ~/gitrepos
~/gitrepos$ git clone git://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git

~$ cd ~/vulnDBGen
~/vulnDBGen$ python initialize.py
~/vulnDBGen$ python src/get_cvepatch_from_git.py linux
~/vulnDBGen$ python src/get_source_from_cvepatch.py linux
```

### H. OpenSSL (OpenSSL Software Foundation)
```
~$ cd ~/gitrepos
~/gitrepos$ git clone https://github.com/openssl/openssl.git

~$ cd ~/vulnDBGen
~/vulnDBGen$ python initialize.py
~/vulnDBGen$ python src/get_cvepatch_from_git.py openssl
~/vulnDBGen$ python src/get_source_from_cvepatch.py openssl
```

### I. PostgreSQL DBMS (The PostgreSQL Global Development Group)
```
~$ cd ~/gitrepos
~/gitrepos$ git clone https://github.com/postgres/postgres.git

~$ cd ~/vulnDBGen
~/vulnDBGen$ python initialize.py
~/vulnDBGen$ python src/get_cvepatch_from_git.py postgres
~/vulnDBGen$ python src/get_source_from_cvepatch.py postgres
```

### J. Ubuntu Trusty (Canonical Ltd.)
```
~$ cd ~/gitrepos
~/gitrepos$ git clone git://kernel.ubuntu.com/ubuntu/ubuntu-trusty.git

~$ cd ~/vulnDBGen
~/vulnDBGen$ python initialize.py
~/vulnDBGen$ python src/get_cvepatch_from_git.py ubuntu-trusty
~/vulnDBGen$ python src/get_source_from_cvepatch.py ubuntu-trusty
```

## 3. Filtering vulnerabilities and generating hash index

### From all repositories
```
~$ cd ~/vulnDBGen
~/vulnDBGen$ python src/vul_dup_remover.py
~/vulnDBGen$ python src/vul_verifier.py

~/vulnDBGen$ python src/vul_hidx_generator.py -a 0 ChakraCore
~/vulnDBGen$ python src/vul_hidx_generator.py -a 4 ChakraCore

~/vulnDBGen$ python src/vul_hidx_generator.py -a 0 freebsd
~/vulnDBGen$ python src/vul_hidx_generator.py -a 4 freebsd

~/vulnDBGen$ python src/vul_hidx_generator.py -a 0 gecko-dev
~/vulnDBGen$ python src/vul_hidx_generator.py -a 4 gecko-dev

~/vulnDBGen$ python src/vul_hidx_generator.py -a 0 glibc
~/vulnDBGen$ python src/vul_hidx_generator.py -a 4 glibc

~/vulnDBGen$ python src/vul_hidx_generator.py -a 0 httpd
~/vulnDBGen$ python src/vul_hidx_generator.py -a 4 httpd

~/vulnDBGen$ python src/vul_hidx_generator.py -a 0 krb5
~/vulnDBGen$ python src/vul_hidx_generator.py -a 4 krb5

~/vulnDBGen$ python src/vul_hidx_generator.py -a 0 linux
~/vulnDBGen$ python src/vul_hidx_generator.py -a 4 linux

~/vulnDBGen$ python src/vul_hidx_generator.py -a 0 openssl
~/vulnDBGen$ python src/vul_hidx_generator.py -a 4 openssl

~/vulnDBGen$ python src/vul_hidx_generator.py -a 0 postgres
~/vulnDBGen$ python src/vul_hidx_generator.py -a 4 postgres

~/vulnDBGen$ python src/vul_hidx_generator.py -a 0 ubuntu-trusty
~/vulnDBGen$ python src/vul_hidx_generator.py -a 4 ubuntu-trusty
```
