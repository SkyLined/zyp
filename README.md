```

        .dSSSSSSSP' YSb   ,dSP' iSSSSSSb,
            ,dSP'    YSb,dSP'  iSP` _7SP`   Python zip (de-)compression utility
          ,dSP'       )dSP'   iSSSSSS*'
        ,dSP'       ,dSP'    iSP`          http://github.com/SkyLined/zyp
      .dSSSSSSP'  .dSP'     iSP`
```
Usage:
======
+ **zyp.py <source file or folder> <destination .zip file>**
+ **unzyp.py [--list] <source .zip file> <destination folder>**
+ **unzyp.py --list <source .zip file>**

zyp.py
------
**zyp.py** will add the source files or all files in the source folder to the
destination .zip file. The destination .zip file is created if it does not
exist but files are added to any existing destination .zip file. If a file
already exists in the destination .zip file, it is overwritten.

unzyp.py
--------
**unzyp.py** will extract all files in the source .zip file to the destination
folder. The destination folder is created if it does not exist and files
are added to any existing destination folder. If a file already exists in
the destination folder, it is overwritten.
If you specify the --list argument, no files will be extracted but
all the files found in the source .zip file are output.

Exit codes:
===========
+ **0** = zyp/unzyp did not compress/decompress any files.
+ **1** = zyp/unzyp compressed/decompressed files successfully.
+ **2** = zyp/unzyp was unable to parse the command-line arguments provided.
+ **3** = zyp/unzyp ran into an internal error: please report the details!
+ **4** = zyp/unzyp cannot read from the given source.
+ **5** = zyp/unzyp cannot write to the given destination.
