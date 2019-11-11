from oConsole import oConsole;
from mColors import *;

def fPrintUsageInformation():
  oConsole.fLock();
  try:
    oConsole.fPrint(HILITE,"Usage:");
    oConsole.fPrint();
    oConsole.fPrint(INFO,"  zyp.py <source file or folder> <destination zip file>");
    oConsole.fPrint(INFO,"  unzyp.py <source zip file> <destination folder>");
    oConsole.fPrint();
    oConsole.fPrint(HILITE, "Exit codes:");
    oConsole.fPrint("  ", INFO, "0", NORMAL," = zyp/unzyp did not compress/decompress any files.");
    oConsole.fPrint("  ", INFO, "1", NORMAL," = zyp/unzyp compressed/decompressed files successfully.");
    oConsole.fPrint("  ", ERROR_INFO, "2", NORMAL, " = zyp/unzyp was unable to parse the command-line arguments provided.");
    oConsole.fPrint("  ", ERROR_INFO, "3", NORMAL, " = zyp/unzyp ran into an internal error: please report the details!");
    oConsole.fPrint("  ", ERROR_INFO, "4", NORMAL, " = zyp/unzyp cannot read from the given source.");
    oConsole.fPrint("  ", ERROR_INFO, "5", NORMAL, " = zyp/unzyp cannot write to the given destination.");
  finally:             
    oConsole.fUnlock();