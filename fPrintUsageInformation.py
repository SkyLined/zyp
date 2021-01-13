from oConsole import oConsole;

from mColors import *;

def fPrintUsageInformation():
  oConsole.fLock();
  try:
    oConsole.fPrint(HILITE,"Usage:");
    oConsole.fPrint(INFO, "  zyp.py [options] <source file or folder> <destination .zip file>");
    oConsole.fPrint(INFO, "  unzyp.py [options] <source .zip file> [<destination folder>]");
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
    oConsole.fPrint();
    oConsole.fPrint(INFO, "Options:");
    oConsole.fPrint(INFO, "  -h", NORMAL, ", ", INFO, "--help", NORMAL);
    oConsole.fPrint("    Output this cruft without zipping/unzipping anything.");
    oConsole.fPrint(INFO, "  --version", NORMAL);
    oConsole.fPrint("    Output version information without zipping/unzipping anything.");
    oConsole.fPrint(INFO, "  -d", NORMAL, ", ", INFO, "--debug", NORMAL);
    oConsole.fPrint("    Output debug information while zipping/unzipping files.");
    oConsole.fPrint(INFO, "  -l", NORMAL, ", ", INFO, "--list", NORMAL);
    oConsole.fPrint("    (unzyp only) List all files in a zip file without extracting them.");
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