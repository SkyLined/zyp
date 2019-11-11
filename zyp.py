
"""
                                                                                
        .dSSSSSSSP' YSb   ,dSP' iSSSSSSb                                        
            ,dSP'    YSb,dSP'  iSP` _7SP     Python zip compression utility     
          ,dSP'       )dSP'   iSSSSSS*'                                         
        ,dSP'       ,dSP'    iSP`          http://github.com/SkyLined/zyp       
      .dSSSSSSP'  .dSP'     iSP`                                                
                                                                                
"""

# Running this script will return an exit code, which translates as such:
# 0 = executed successfully, nothing to compress.
# 1 = executed successfully, files compressed.
# 2 = bad arguments
# 3 = internal error
# 4 = cannot read from uncompressed file or folder.
# 5 = cannot write to compressed zip file.

from fCheckDependencies import fCheckDependencies;
fCheckDependencies();

import sys;

from cFileSystemItem import cFileSystemItem;
from fPrintLogo import fPrintLogo;
from fPrintUsageInformation import fPrintUsageInformation;
from fPrintVersionInformation import fPrintVersionInformation;
from mColors import *;
from oConsole import oConsole;

# Parse arguments
sInputFileOrFolderPath = None;
sOutputZipFilePath = None;
for sArgument in sys.argv[1:]:
  if sArgument in ["-?", "-h", "--help", "/?", "/h", "/help"]:
    fPrintLogo();
    fPrintUsageInformation();
    sys._exit(0);
  elif sArgument in ["--version", "/version"]:
    fPrintVersionInformation(
      bCheckForUpdates = True,
      bCheckAndShowLicenses = True,
      bShowInstallationFolders = True,
    );
    sys._exit(0);
  elif sInputFileOrFolderPath is None:
    sInputFileOrFolderPath = sArgument;
  elif sOutputZipFilePath is None:
    sOutputZipFilePath = sArgument;
  else:
    oConsole.fPrint(ERROR, "Superfluous argument ", ERROR_INFO, sArgument, ERROR, "!");
    sys.exit(2);
if sInputFileOrFolderPath is None:
  oConsole.fPrint(ERROR, "Missing input file or folder argument!");
  sys.exit(2);
if sOutputZipFilePath is None:
  oConsole.fPrint(ERROR, "Missing output zip file argument!");
  sys.exit(2);

oInputFileOrFolder = cFileSystemItem(sInputFileOrFolderPath);
if oInputFileOrFolder.fbIsFile(bParseZipFiles = True):
  oBaseFolder = oInputFileOrFolder.oParent;
  aoInputFilesAndFolders = [oInputFileOrFolder];
elif oInputFileOrFolder.fbIsFolder(bParseZipFiles = True):
  oBaseFolder = oInputFileOrFolder;
  aoInputFilesAndFolders = oInputFileOrFolder.faoGetDescendants();
else:
  oConsole.fPrint(ERROR, "Input file or folder ", ERROR_INFO, oInputFileOrFolder.sPath, ERROR, " not found!");
  sys.exit(4);

oOutputZipFile = cFileSystemItem(sOutputZipFilePath);
if oOutputZipFile.fbExists(bParseZipFiles = True) \
    and not oOutputZipFile.fbDelete(bParseZipFiles = True):
  oConsole.fPrint(ERROR, "Existing output zip file ", ERROR_INFO, oOutputZipFile.sPath, ERROR, " cannot be deleted!");
  sys.exit(5);
if not oOutputZipFile.fbCreateAsZipFile(bParseZipFiles = True, bKeepOpen = True):
  oConsole.fPrint(ERROR, "Output zip file ", ERROR_INFO, oOutputZipFile.sPath, ERROR, " cannot be created!");
  sys.exit(5);
uTotalBytes = 0;
uTotalFiles = 0;
for oInputFileOrFolder in aoInputFilesAndFolders:
  if oInputFileOrFolder.sPath != oOutputZipFile.sPath \
      and oInputFileOrFolder.fbIsFile(bParseZipFiles = True):
    sRelativePath = oBaseFolder.fsGetRelativePathTo(oInputFileOrFolder);
    oOutputFile = oOutputZipFile.foGetDescendant(sRelativePath, bParseZipFiles = True);
    oConsole.fStatus("* Reading ", INFO, sRelativePath, NORMAL, "...");
    sData = oInputFileOrFolder.fsRead();
    if oOutputFile.fbIsFile(bParseZipFiles = True):
      oConsole.fStatus("* Overwriting file ", INFO, sRelativePath, NORMAL,
          " (", INFO, str(len(sData)), NORMAL, " bytes)...");
      if not oOutputFile.fbWrite(sData):
        oConsole.fPrint(ERROR, "Cannot write ", ERROR_INFO, str(len(sData)), ERROR,
            " bytes over existing file ", ERROR_INFO, sRelativePath, ERROR,
            " in zip file ", ERROR_INFO, oOutputZipFile.sPath, ERROR, "!");
        sys.exit(5);
    else:
      oConsole.fStatus("* Creating file ", INFO, sRelativePath, NORMAL,
          " (", INFO, str(len(sData)), NORMAL, " bytes)...");
      if not oOutputFile.fbCreateAsFile(sData, bParseZipFiles = True):
        oConsole.fPrint(ERROR, "Cannot write ", ERROR_INFO, str(len(sData)), ERROR,
            " bytes to new file ", ERROR_INFO, sRelativePath, ERROR,
            " in zip file ", ERROR_INFO, oOutputZipFile.sPath, ERROR, "!");
        sys.exit(5);
    uTotalBytes += len(sData);
    uTotalFiles += 1;

if not oOutputZipFile.fbClose():
  oConsole.fPrint(ERROR, "Output zip file ", ERROR_INFO, oOutputZipFile.sPath, ERROR, " cannot be closed!");
  sys.exit(5);

oConsole.fPrint("Added ", INFO, str(uTotalFiles), NORMAL, " files (", INFO, str(uTotalBytes), NORMAL,
    " bytes) to ", INFO, oOutputZipFile.sPath, NORMAL, ".");
sys.exit(0 if uTotalFiles == 0 else 1);