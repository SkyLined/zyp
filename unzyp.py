
"""
                                                                                
        .dSSSSSSSP' YSb   ,dSP' iSSSSSSb                                        
   UN-      ,dSP'    YSb,dSP'  iSP` _7SP     Python unzip decompression utility 
          ,dSP'       )dSP'   iSSSSSS*'                                         
        ,dSP'       ,dSP'    iSP`          http://github.com/SkyLined/zyp       
      .dSSSSSSP'  .dSP'     iSP`                                                
                                                                                
"""

# Running this script will return an exit code, which translates as such:
# 0 = executed successfully, nothing to uncompress.
# 1 = executed successfully, files uncompressed.
# 2 = bad arguments
# 3 = internal error
# 4 = cannot read from compressed zip file
# 5 = cannot write to decompressed file or create folder.

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
sInputZipFilePath = None;
sOutputFolderPath = None;
bExtractFiles = True;
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
  elif sArgument in ["--list", "/list"]:
    bExtractFiles = False;
  elif sInputZipFilePath is None:
    sInputZipFilePath = sArgument;
  elif sOutputFolderPath is None:
    sOutputFolderPath = sArgument;
  else:
    oConsole.fPrint(ERROR, "Superfluous argument ", ERROR_INFO, sArgument, ERROR, "!");
    sys.exit(2);
if sInputZipFilePath is None:
  oConsole.fPrint(ERROR, "Missing input zip file argument!");
  sys.exit(2);
if bExtractFiles and sOutputFolderPath is None:
  oConsole.fPrint(ERROR, "Missing output folder argument!");
  sys.exit(2);

oInputZipFile = cFileSystemItem(sInputZipFilePath);
if not oInputZipFile.fbIsFile(bParseZipFiles = True):
  oConsole.fPrint(ERROR, "Cannot find input zip file ", ERROR_INFO, oInputZipFile.sPath, ERROR, "!");
  sys.exit(2);
if not oInputZipFile.fbOpenAsZipFile(bParseZipFiles = True):
  oConsole.fPrint(ERROR, "Cannot open input zip file ", ERROR_INFO, oInputZipFile.sPath, ERROR, "!");
  sys.exit(3);

if bExtractFiles:
  oOutputBaseFolder = cFileSystemItem(sOutputFolderPath);
  if oOutputBaseFolder.fbExists(bParseZipFiles = True):
    if not oOutputBaseFolder.fbIsFolder(bParseZipFiles = True):
      oConsole.fPrint(ERROR, "Output folder ", ERROR_INFO, oOutputBaseFolder.sPath, ERROR, " exists but it is not a folder!");
      sys.exit(2);
  elif not oOutputBaseFolder.fbCreateAsFolder(bParseZipFiles = True):
    oConsole.fPrint(ERROR, "Output folder ", ERROR_INFO, oOutputBaseFolder.sPath, ERROR, " cannot be created!");
    sys.exit(3);
uTotalFolders = 0;
uTotalFiles = 0;
uTotalBytes = 0;
# Get all descendants of the input folder, which can be iside a zip file (bParseZipFiles = True)
# Do not get descendants of descendants if they are zip files (bParseDescendantZipFiles = False) as we will
# simply copy them as is without parsing them.
aoQueuedInputFilesAndFolders = oInputZipFile.faoGetChildren(bParseZipFiles = True);
while len(aoQueuedInputFilesAndFolders) > 0:
  oInputFileOrFolder = aoQueuedInputFilesAndFolders.pop(0);
  sRelativePath = oInputZipFile.fsGetRelativePathTo(oInputFileOrFolder);
  bIsFolder = oInputFileOrFolder.fbIsFolder(bParseZipFiles = True);
  if bIsFolder:
    uTotalFolders += 1;
    # Queue children of the folder at the top, so we walk it like a tree, branch by branch.
    oConsole.fStatus("* Reading folder ", INFO, sRelativePath, NORMAL, "...");
    aoQueuedInputFilesAndFolders = oInputFileOrFolder.faoGetChildren(bParseZipFiles = True) + aoQueuedInputFilesAndFolders;
  else:
    oConsole.fStatus("* Reading file ", INFO, sRelativePath, NORMAL, "...");
    sData = oInputFileOrFolder.fsRead(bParseZipFiles = True);
    uTotalFiles += 1;
    uTotalBytes += len(sData);
  if bExtractFiles:
    oOutputFileOrFolder = oOutputBaseFolder.foGetDescendant(sRelativePath, bParseZipFiles = True);
    if oInputFileOrFolder.fbIsFolder(bParseZipFiles = True):
      # Handle folders:
      if oOutputFileOrFolder.fbExists(bParseZipFiles = True):
        if not oOutputFileOrFolder.fbIsFolder(bParseZipFiles = True):
          # File exists: error
          oConsole.fPrint(ERROR, "Cannot create folder ", ERROR_INFO, sRelativePath, ERROR, " in folder ", ERROR_INFO,
              oOutputBaseFolder.sPath, ERROR, ": a file with that name already exists!");
          sys.exit(3);
        # Folders exists: do nothing
      else:
        # Folders does not exist: create
        oConsole.fStatus("* Creating folder ", INFO, sRelativePath, NORMAL, "...");
        if not oOutputFileOrFolder.fbCreateAsFolder(bParseZipFiles = True):
          oConsole.fPrint(ERROR, "Cannot create folder ", ERROR_INFO, sRelativePath, ERROR, " in folder ", ERROR_INFO,
              oOutputBaseFolder.sPath, ERROR, ": a folder with that name already exists!");
          sys.exit(3);
    else:
      # Handle files:
      if oOutputFileOrFolder.fbExists(bParseZipFiles = True):
        if not oOutputFileOrFolder.fbIsFile(bParseZipFiles = True):
          # Folders exists: error
          oConsole.fPrint(ERROR, "Cannot create file ", ERROR_INFO, sRelativePath, ERROR, " in folder ", ERROR_INFO,
              oOutputBaseFolder.sPath, ERROR, ": a folder with that name already exists!");
          sys.exit(3);
        # File exists: overwrite
        oConsole.fStatus("* Overwriting file ", INFO, sRelativePath, NORMAL, " (", INFO, str(len(sData)), NORMAL, " bytes)...");
        if not oOutputFileOrFolder.fbWrite(sData):
          oConsole.fPrint(ERROR, "Cannot write ", ERROR_INFO, str(len(sData)), ERROR, " bytes over existing file ", ERROR_INFO,
              sRelativePath, ERROR, " in folder ", ERROR_INFO, oOutputBaseFolder.sPath, ERROR, "!");
          sys.exit(3);
      else:
        # File does not exists: create
        oConsole.fStatus("* Creating file ", INFO, sRelativePath, NORMAL, " (", INFO, str(len(sData)), NORMAL, " bytes)...");
        if not oOutputFileOrFolder.fbCreateAsFile(sData, bParseZipFiles = True):
          oConsole.fPrint(ERROR, "Cannot write ", ERROR_INFO, str(len(sData)), ERROR, " bytes to new file ", ERROR_INFO,
              sRelativePath, ERROR, " in folder ", ERROR_INFO, oOutputBaseFolder.sPath, ERROR, "!");
          sys.exit(3);
  elif not bIsFolder:
    # We're not extracting, simply listing the files:
    oConsole.fOutput("+ File ", INFO, sRelativePath, NORMAL, " (", INFO, str(len(sData)), NORMAL, " bytes)...");

if not oInputZipFile.fbClose():
  oConsole.fPrint(ERROR, "Input zip file ", ERROR_INFO, oInputZipFile.sPath, ERROR, " cannot be closed!");
  sys.exit(5);

if not bExtractFiles:
  oConsole.fPrint("Found ", INFO, str(uTotalFiles), NORMAL, " files (", INFO, str(uTotalBytes), NORMAL,
      " bytes) and ", INFO, str(uTotalFolders), NORMAL, " folders.");
  sys.exit(0);
oConsole.fPrint("Extracted ", INFO, str(uTotalFiles), NORMAL, " files (", INFO, str(uTotalBytes), NORMAL,
    " bytes) and ", INFO, str(uTotalFolders), NORMAL, " folders to ", INFO, oOutputBaseFolder.sPath, NORMAL, ".");
sys.exit(0 if uTotalFiles == 0 else 1);
