from mConsole import oConsole;

from mColors import *;
from fPrintLogo import fPrintLogo;

def fPrintUsageInformation():
  oConsole.fLock();
  try:
    fPrintLogo();
    oConsole.fOutput(HILITE,"Usage:");
    oConsole.fOutput(INFO, "  zyp.py [options] <source file or folder> <destination .zip file>");
    oConsole.fOutput(INFO, "  unzyp.py [options] <source .zip file> [<destination folder>]");
    oConsole.fOutput();
    oConsole.fOutput(INFO, "  zyp.py", NORMAL, " will add the source files or all files in the source folder to the");
    oConsole.fOutput("  destination .zip file. The destination .zip file is created if it does not");
    oConsole.fOutput("  exist but files are added to any existing destination .zip file. If a file");
    oConsole.fOutput("  already exists in the destination .zip file, it is overwritten.");
    oConsole.fOutput();
    oConsole.fOutput(INFO, "  unzyp.py", NORMAL, " will extract all files in the source .zip file to the destination");
    oConsole.fOutput("  folder. The destination folder is created if it does not exist and files");
    oConsole.fOutput("  are added to any existing destination folder. If a file already exists in");
    oConsole.fOutput("  the destination folder, it is overwritten.");
    oConsole.fOutput();
    oConsole.fOutput(INFO, "Options:");
    oConsole.fOutput("  ", INFO, "-h", NORMAL, ", ", INFO, "--help");
    oConsole.fOutput("    This cruft.");
    oConsole.fOutput("  ", INFO, "--version");
    oConsole.fOutput("    Show version information.");
    oConsole.fOutput("  ", INFO, "--version-check");
    oConsole.fOutput("    Check for updates and show version information.");
    oConsole.fOutput("  ", INFO, "--license");
    oConsole.fOutput("    Show license information.");
    oConsole.fOutput("  ", INFO, "--license-update");
    oConsole.fOutput("    Download license updates and show license information.");
    oConsole.fOutput("  ", INFO, "--arguments", NORMAL, "=<", INFO, "file path", NORMAL, ">");
    oConsole.fOutput("    Load additional arguments from the provided value and insert them in place");
    oConsole.fOutput("    of this argument.");
    
    oConsole.fOutput(INFO, "  -d", NORMAL, ", ", INFO, "--debug", NORMAL);
    oConsole.fOutput("    Output debug information while zipping/unzipping files.");
    oConsole.fOutput(INFO, "  -l", NORMAL, ", ", INFO, "--list", NORMAL);
    oConsole.fOutput("    (unzyp only) List all files in a zip file without extracting them.");
    oConsole.fOutput();
    oConsole.fOutput(HILITE, "Exit codes:");
    oConsole.fOutput("  ", 0x0F0A, "0", NORMAL," = zyp/unzyp did not compress/decompress any files.");
    oConsole.fOutput("  ", 0x0F0A, "1", NORMAL," = zyp/unzyp compressed/decompressed files successfully.");
    oConsole.fOutput("  ", 0x0F0C, "2", NORMAL, " = zyp/unzyp was unable to parse the command-line arguments provided.");
    oConsole.fOutput("  ", 0x0F0C, "3", NORMAL, " = zyp/unzyp ran into an internal error: please report the details!");
    oConsole.fOutput("  ", 0x0F0C, "4", NORMAL, " = zyp/unzyp cannot read from the given source.");
    oConsole.fOutput("  ", 0x0F0C, "5", NORMAL, " = zyp/unzyp cannot write to the given destination.");
  finally:             
    oConsole.fUnlock();