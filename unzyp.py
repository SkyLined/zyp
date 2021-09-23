import sys;

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

from fInitializeProduct import fInitializeProduct;
fInitializeProduct();

try: # mDebugOutput use is Optional
  import mDebugOutput as m0DebugOutput;
except ModuleNotFoundError as oException:
  if oException.args[0] != "No module named 'mDebugOutput'":
    raise;
  m0DebugOutput = None;

guExitCodeInternalError = 1; # Just in case mExitCodes is not loaded, as we need this later.
try:
  from mFileSystemItem import cFileSystemItem;
  from mHumanReadable import fsBytesToHumanReadableString;
  from mConsole import oConsole;
  
  from fatsArgumentLowerNameAndValue import fatsArgumentLowerNameAndValue;
  from mColorsAndChars import *;
  from mColorsAndChars import *;
  from mExitCodes import *;
  
  if __name__ == "__main__":
    # Parse arguments
    s0InputZipFilePath = None;
    s0OutputFolderPath = None;
    bExtractFiles = True;
    for (sArgument, s0LowerName, s0Value) in fatsArgumentLowerNameAndValue():
      if s0LowerName in ["l", "list"]:
        bExtractFiles = False;
      elif s0LowerName in ["debug"]:
        if m0DebugOutput is None:
          oConsole.fOutput(
            COLOR_ERROR, CHAR_ERROR,
            COLOR_NORMAL, " The mDebugOutput module is not available!",
          );
          sys.exit(2);
        m0DebugOutput.fEnableAllDebugOutput();
      elif s0LowerName:
        oConsole.fOutput(
          COLOR_ERROR, CHAR_ERROR,
          COLOR_NORMAL, " Unknown argument ",
          COLOR_INFO, sArgument,
          COLOR_NORMAL, "!",
        );
        sys.exit(2);
      elif s0InputZipFilePath is None:
        s0InputZipFilePath = sArgument;
      elif s0OutputFolderPath is None:
        s0OutputFolderPath = sArgument;
      else:
        oConsole.fOutput(
          COLOR_ERROR, CHAR_ERROR,
          COLOR_NORMAL, " Superfluous argument ",
          COLOR_INFO, sArgument,
          COLOR_ERROR, "!",
        );
        sys.exit(2);
    if s0InputZipFilePath is None:
      oConsole.fOutput(
        COLOR_ERROR, CHAR_ERROR,
        COLOR_NORMAL, " Missing input zip file argument!",
      );
      sys.exit(2);
    # Check input zip file path argument.
    oInputZipFile = cFileSystemItem(s0InputZipFilePath);
    if not oInputZipFile.fbExists(bParseZipFiles = True):
      oConsole.fOutput(
        COLOR_ERROR, CHAR_ERROR,
        COLOR_NORMAL, " Input zip ",
        COLOR_INFO, oInputZipFile.sPath,
        COLOR_ERROR, " does not exist!",
      );
      sys.exit(2);
    if not oInputZipFile.fbIsFile(bParseZipFiles = True):
      oConsole.fOutput(
        COLOR_ERROR, CHAR_ERROR,
        COLOR_NORMAL, " Input zip ",
        COLOR_INFO, oInputZipFile.sPath,
        COLOR_ERROR, " is not a file!",
      );
      sys.exit(2);
    if not oInputZipFile.fbOpenAsZipFile(bParseZipFiles = True):
      oConsole.fOutput(
        COLOR_ERROR, CHAR_ERROR,
        COLOR_NORMAL, "Input zip ",
        COLOR_INFO, oInputZipFile.sPath,
        COLOR_ERROR, " cannot be opened!",
        );
      sys.exit(3);
    
    if bExtractFiles:
      # If no output folder path argument is provided generate one base on input file name.
      if s0OutputFolderPath is None:
        if not oInputZipFile.s0Extension:
          oConsole.fOutput(
            COLOR_ERROR, CHAR_ERROR,
            COLOR_NORMAL, "You must provide an output folder argument because the input zip ",
            COLOR_INFO, oInputZipFile.sPath,
            COLOR_ERROR, " does not have an extension!",
          );
          sys.exit(3);
        s0OutputFolderPath = oInputZipFile.sPath[:-len(oInputZipFile.s0Extension) - 1];
      # Check output folder path argument (or the previously generated one).
      oOutputBaseFolder = cFileSystemItem(s0OutputFolderPath);
      if not oOutputBaseFolder.fbExists(bParseZipFiles = True):
        if not oOutputBaseFolder.fbCreateAsFolder(bParseZipFiles = True):
          oConsole.fOutput(
            COLOR_ERROR, CHAR_ERROR,
            COLOR_NORMAL, " Output folder ",
            COLOR_INFO, oOutputBaseFolder.sPath,
            COLOR_ERROR, " cannot be created!",
          );
          sys.exit(3);
      elif not oOutputBaseFolder.fbIsFolder(bParseZipFiles = True):
        oConsole.fOutput(
          COLOR_ERROR, CHAR_ERROR,
          COLOR_NORMAL, " Output folder ",
          COLOR_INFO, oOutputBaseFolder.sPath,
          COLOR_ERROR, " is not a folder!",
        );
        sys.exit(2);
    
    uTotalBytes = 0;
    # Get all descendants of the input folder, which can be iside a zip file (bParseZipFiles = True)
    # Do not get descendants of descendants if they are zip files (bParseDescendantZipFiles = False) as we will
    # simply copy them as is without parsing them.
    oConsole.fStatus("* Reading root folder...");
    aoQueuedInputFilesAndFoldersToBeEnumerated = oInputZipFile.faoGetChildren(bParseZipFiles = True);
    aoInputFolders = [];
    aoInputFiles = [];
    while len(aoQueuedInputFilesAndFoldersToBeEnumerated) > 0:
      oInputFileOrFolder = aoQueuedInputFilesAndFoldersToBeEnumerated.pop(0);
      sRelativePath = oInputZipFile.fsGetRelativePathTo(oInputFileOrFolder);
      bIsFolder = oInputFileOrFolder.fbIsFolder(bParseZipFiles = True);
      if bIsFolder:
        aoInputFolders.append(oInputFileOrFolder);
        # Queue children of the folder at the top, so we walk it like a tree, branch by branch.
        oConsole.fStatus(
          COLOR_BUSY, CHAR_BUSY,
          COLOR_NORMAL, " Found ",
          COLOR_INFO, str(len(aoInputFiles)),
          COLOR_NORMAL, " files and ",
          COLOR_INFO, str(len(aoInputFolders)),
          COLOR_NORMAL, " folders. Currently reading folder ",
          COLOR_INFO, sRelativePath,
          COLOR_NORMAL, "...",
        );
        aoQueuedInputFilesAndFoldersToBeEnumerated = oInputFileOrFolder.faoGetChildren(bParseZipFiles = True) \
            + aoQueuedInputFilesAndFoldersToBeEnumerated;
      else:
        aoInputFiles.append(oInputFileOrFolder);
    uProcessedFolders = 0;
    uProcessedFiles = 0;
    if bExtractFiles:
      for oInputFolder in aoInputFolders:
        sRelativePath = oInputZipFile.fsGetRelativePathTo(oInputFolder);
        oOutputFolder = oOutputBaseFolder.foGetDescendant(sRelativePath, bParseZipFiles = True);
        nProgress = 1.0 * (uProcessedFolders + uProcessedFiles) / (len(aoInputFolders) + len(aoInputFiles));
        oConsole.fProgressBar(nProgress, "* %s: Creating folder..." % sRelativePath, bCenterMessage = False);
        if oOutputFolder.fbExists(bParseZipFiles = True):
          if not oOutputFolder.fbIsFolder(bParseZipFiles = True):
            # File exists: error
            oConsole.fOutput(
              COLOR_ERROR, CHAR_ERROR,
              COLOR_NORMAL, "Cannot create folder ",
              COLOR_INFO, sRelativePath,
              COLOR_ERROR, " in folder ",
              COLOR_INFO, oOutputBaseFolder.sPath,
              COLOR_ERROR, ": a file with that name already exists!",
            );
            sys.exit(3);
          # Folders exists: do nothing
        else:
          # Folders does not exist: create
          if not oOutputFolder.fbCreateAsFolder(bParseZipFiles = True):
            oConsole.fOutput(
              COLOR_ERROR, CHAR_ERROR,
              COLOR_NORMAL, "Cannot create folder ",
              COLOR_INFO, sRelativePath,
              COLOR_ERROR, " in folder ",
              COLOR_INFO, oOutputBaseFolder.sPath,
              COLOR_ERROR, ": a folder with that name already exists!",
            );
            sys.exit(3);
        uProcessedFolders += 1;
      
    for oInputFile in aoInputFiles:
      sRelativePath = oInputZipFile.fsGetRelativePathTo(oInputFile);
      nProgress = 1.0 * (uProcessedFolders + uProcessedFiles) / (len(aoInputFolders) + len(aoInputFiles));
      oConsole.fProgressBar(nProgress, "* %s: reading..." % sRelativePath, bCenterMessage = False);
      sbData = oInputFileOrFolder.fsbRead(bParseZipFiles = True);
      uTotalBytes += len(sbData);
      if bExtractFiles:
        oOutputFile = oOutputBaseFolder.foGetDescendant(sRelativePath, bParseZipFiles = True);
        if oOutputFile.fbExists(bParseZipFiles = True):
          if not oOutputFile.fbIsFile(bParseZipFiles = True):
            # Folders exists: error
            oConsole.fOutput(
              COLOR_ERROR, CHAR_ERROR,
              COLOR_NORMAL, "Cannot create file ",
              COLOR_INFO, sRelativePath,
              COLOR_ERROR, " in folder ",
              COLOR_INFO, oOutputBaseFolder.sPath,
              COLOR_ERROR, ": a folder with that name already exists!",
            );
            sys.exit(3);
          # File exists: overwrite
          oConsole.fProgressBar(nProgress, "* %s: Overwriting (%d bytes)..." % (sRelativePath, len(sbData)), bCenterMessage = False);
          if not oOutputFile.fbWrite(sbData):
            oConsole.fOutput(
              COLOR_ERROR, CHAR_ERROR,
              COLOR_NORMAL, "Cannot write ",
              COLOR_INFO, str(len(sbData)),
              COLOR_ERROR, " bytes over existing file ",
              COLOR_INFO, sRelativePath,
              COLOR_ERROR, " in folder ",
              COLOR_INFO, oOutputBaseFolder.sPath,
              COLOR_ERROR, "!",
            );
            sys.exit(3);
        else:
          # File does not exists: create
          oConsole.fProgressBar(nProgress, "* %s: Creating (%d bytes)..." % (sRelativePath, len(sbData)), bCenterMessage = False);
          if not oOutputFile.fbCreateAsFile(sbData, bParseZipFiles = True):
            oConsole.fOutput(
              COLOR_ERROR, CHAR_ERROR,
              COLOR_NORMAL, " Cannot write ",
              COLOR_INFO, str(len(sbData)),
              COLOR_ERROR, " bytes to new file ",
              COLOR_INFO, sRelativePath,
              COLOR_ERROR, " in folder ",
              COLOR_INFO, oOutputBaseFolder.sPath,
              COLOR_ERROR, "!",
            );
            sys.exit(3);
      else:
        oConsole.fOutput(
          COLOR_ADD, CHAR_ADD,
          COLOR_NORMAL, " ",
          COLOR_INFO, sRelativePath,
          COLOR_NORMAL, " (",
          COLOR_INFO, str(len(sbData)),
          COLOR_NORMAL, " bytes)."
        );
      uProcessedFiles += 1;
    
    uTotalFolders = len(aoInputFolders);
    uTotalFiles = len(aoInputFiles);
    
    if not oInputZipFile.fbClose():
      oConsole.fOutput(
        COLOR_ERROR, CHAR_ERROR,
        COLOR_NORMAL, "Input zip file ",
        COLOR_INFO, oInputZipFile.sPath,
        COLOR_ERROR, " cannot be closed!",
      );
      sys.exit(5);
    
    if not bExtractFiles:
      oConsole.fOutput(
        COLOR_OK, CHAR_OK,
        COLOR_NORMAL, " Found ",
        COLOR_INFO, str(uTotalFiles),
        COLOR_NORMAL, " files (",
        COLOR_INFO, fsBytesToHumanReadableString(uTotalBytes),
        COLOR_NORMAL, ") and ",
        COLOR_INFO, str(uTotalFolders),
        COLOR_NORMAL, " folders.",
      );
      sys.exit(0);
    oConsole.fOutput(
      COLOR_OK, CHAR_OK,
        COLOR_NORMAL, " Extracted ",
      COLOR_INFO, str(uTotalFiles),
      COLOR_NORMAL, " files (",
      COLOR_INFO, fsBytesToHumanReadableString(uTotalBytes),
      COLOR_NORMAL, ") and ",
      COLOR_INFO, str(uTotalFolders),
      COLOR_NORMAL, " folders to ",
      COLOR_INFO, oOutputBaseFolder.sPath,
      COLOR_NORMAL, "."
    );
    sys.exit(0 if uTotalFiles == 0 else 1);

except Exception as oException:
  if m0DebugOutput:
    m0DebugOutput.fTerminateWithException(oException, guExitCodeInternalError);
  raise;