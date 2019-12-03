from oConsole import oConsole;
from mColors import *;

def fPrintUsageInformation():
  oConsole.fLock();
  try:
    oConsole.fPrint(HILITE,"Usage:");
    oConsole.fPrint(INFO, "  zyp.py <source file or folder> <destination .zip file>");
    oConsole.fPrint(INFO, "  unzyp.py [--list] <source .zip file> <destination folder>");
    oConsole.fPrint(INFO, "  unzyp.py --list <source .zip file>");
    oConsole.fPrint();
    oConsole.fPrint(INFO, "  zyp.py", NORMAL, " will add the source files or all files in the source folder to the");
    oConsole.fPrint("  destination .zip file. The destination .zip file is created if it does not");
    oConsole.fPrint("  exist but files are added to any existing destination .zip file. If a file");
    oConsole.fPrint("  already exists in the destination .zip file, it is overwritten.");
    oConsole.fPrint();
    oConsole.fPrint(INFO, "  unzyp.py", NORMAL, " will extract all files in the source .zip file to the destination");
    oConsole.fPrint("  folder. The destination folder is created if it does not exist and files");
    oConsole.fPrint("  are added to any existing destination folder. If a file already exists in");
    oConsole.fPrint("  the destination folder, it is overwritten.");
    oConsole.fPrint("  If you specify the ", INFO, "--list", NORMAL, " argument, no files will be extracted but");
    oConsole.fPrint("  all the files found in the source .zip file are output.");
    oConsole.fPrint();
    oConsole.fPrint(HILITE, "Exit codes:");
    oConsole.fPrint("  ", 0x0F0A, "0", NORMAL," = zyp/unzyp did not compress/decompress any files.");
    oConsole.fPrint("  ", 0x0F0A, "1", NORMAL," = zyp/unzyp compressed/decompressed files successfully.");
    oConsole.fPrint("  ", 0x0F0C, "2", NORMAL, " = zyp/unzyp was unable to parse the command-line arguments provided.");
    oConsole.fPrint("  ", 0x0F0C, "3", NORMAL, " = zyp/unzyp ran into an internal error: please report the details!");
    oConsole.fPrint("  ", 0x0F0C, "4", NORMAL, " = zyp/unzyp cannot read from the given source.");
    oConsole.fPrint("  ", 0x0F0C, "5", NORMAL, " = zyp/unzyp cannot write to the given destination.");
  finally:             
    oConsole.fUnlock();