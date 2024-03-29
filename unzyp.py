"""                                                                             
        .dSSSSSSSP' YSb   ,dSP' iSSSSSSb                                        
   UN-      ,dSP'    YSb,dSP'  iSP` _7SP     Python unzip decompression utility 
          ,dSP'       )dSP'   iSSSSSS*'                                         
        ,dSP'       ,dSP'    iSP`          http://github.com/SkyLined/zyp       
      .dSSSSSSP'  .dSP'     iSP`                                                
                                                                            """;

import os, sys;

sModulePath = os.path.dirname(__file__);
sys.path = [sModulePath] + [sPath for sPath in sys.path if sPath.lower() != sModulePath.lower()];
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
    bVerbose = False;
    bExtractFiles = True;
    for (sArgument, s0LowerName, s0Value) in fatsArgumentLowerNameAndValue():
      if s0LowerName in ["-v", "/v", "--verbose", "/verbose"]:
        bVerbose = True;
      elif s0LowerName in ["-d", "/d", "--debug", "/debug"]:
        if m0DebugOutput is None:
          oConsole.fOutput(
            COLOR_ERROR, CHAR_ERROR,
            COLOR_NORMAL, " The mDebugOutput module is not available!",
          );
          sys.exit(guExitCodeBadArgument);
        m0DebugOutput.fEnableAllDebugOutput();
      elif s0LowerName in ["l", "list"]:
        bExtractFiles = False;
      elif s0LowerName:
        oConsole.fOutput(
          COLOR_ERROR, CHAR_ERROR,
          COLOR_NORMAL, " Unknown argument ",
          COLOR_INFO, sArgument,
          COLOR_NORMAL, "!",
        );
        sys.exit(guExitCodeBadArgument);
      elif s0InputZipFilePath is None:
        s0InputZipFilePath = sArgument;
      elif s0OutputFolderPath is None:
        s0OutputFolderPath = sArgument;
      else:
        oConsole.fOutput(
          COLOR_ERROR, CHAR_ERROR,
          COLOR_NORMAL, " Superfluous argument ",
          COLOR_INFO, sArgument,
          COLOR_NORMAL, "!",
        );
        sys.exit(guExitCodeBadArgument);
    if s0InputZipFilePath is None:
      oConsole.fOutput(
        COLOR_ERROR, CHAR_ERROR,
        COLOR_NORMAL, " Missing input zip file argument!",
      );
      sys.exit(guExitCodeBadArgument);
    # Check input zip file path argument.
    oInputZipFile = cFileSystemItem(s0InputZipFilePath);
    if not oInputZipFile.fbExists(bParseZipFiles = True):
      oConsole.fOutput(
        COLOR_ERROR, CHAR_ERROR,
        COLOR_NORMAL, " Input zip ",
        COLOR_INFO, oInputZipFile.sPath,
        COLOR_NORMAL, " does not exist!",
      );
      sys.exit(guExitCodeBadArgument);
    if not oInputZipFile.fbIsFile(bParseZipFiles = True):
      oConsole.fOutput(
        COLOR_ERROR, CHAR_ERROR,
        COLOR_NORMAL, " Input zip ",
        COLOR_INFO, oInputZipFile.sPath,
        COLOR_NORMAL, " is not a file!",
      );
      sys.exit(guExitCodeBadArgument);
    if not oInputZipFile.fbIsValidZipFile(bThrowErrors = False):
      oConsole.fOutput(
        COLOR_ERROR, CHAR_ERROR,
        COLOR_NORMAL, " Input zip ",
        COLOR_INFO, oInputZipFile.sPath,
        COLOR_NORMAL, " is not a valid zip file!",
      );
      sys.exit(guExitCodeBadArgument);
    if not oInputZipFile.fbOpenAsZipFile(bParseZipFiles = True):
      oConsole.fOutput(
        COLOR_ERROR, CHAR_ERROR,
        COLOR_NORMAL, "Input zip ",
        COLOR_INFO, oInputZipFile.sPath,
        COLOR_NORMAL, " cannot be opened!",
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
            COLOR_NORMAL, " does not have an extension!",
          );
          sys.exit(guExitCodeBadArgument);
        s0OutputFolderPath = oInputZipFile.sPath[:-len(oInputZipFile.s0Extension) - 1];
      # Check output folder path argument (or the previously generated one).
      oOutputBaseFolder = cFileSystemItem(s0OutputFolderPath);
      if not oOutputBaseFolder.fbExists(bParseZipFiles = True):
        if not oOutputBaseFolder.fbCreateAsFolder(bParseZipFiles = True):
          oConsole.fOutput(
            COLOR_ERROR, CHAR_ERROR,
            COLOR_NORMAL, " Output folder ",
            COLOR_INFO, oOutputBaseFolder.sPath,
            COLOR_NORMAL, " cannot be created!",
          );
          sys.exit(guExitCodeCannotWriteToFileSystem);
      elif not oOutputBaseFolder.fbIsFolder(bParseZipFiles = True):
        oConsole.fOutput(
          COLOR_ERROR, CHAR_ERROR,
          COLOR_NORMAL, " Output folder ",
          COLOR_INFO, oOutputBaseFolder.sPath,
          COLOR_NORMAL, " is not a folder!",
        );
        sys.exit(guExitCodeBadArgument);
    
    uTotalBytes = 0;
    # Get all descendants of the input folder, which can be iside a zip file (bParseZipFiles = True)
    # Do not get descendants of descendants if they are zip files (bParseDescendantZipFiles = False) as we will
    # simply copy them as is without parsing them.
    oConsole.fStatus("* Reading root folder...");
    a0oQueuedInputFilesAndFoldersToBeEnumerated = oInputZipFile.fa0oGetChildren(bParseZipFiles = True);
    if not a0oQueuedInputFilesAndFoldersToBeEnumerated:
      oConsole.fOutput(
        COLOR_ERROR, CHAR_ERROR,
        COLOR_NORMAL, " Input zip file ",
        COLOR_INFO, oInputZipFile.sPath,
        COLOR_NORMAL, " cannot be read!",
      );
      sys.exit(guExitCodeCannotReadFromFileSystem);
    aoInputFolders = [];
    aoInputFiles = [];
    while len(a0oQueuedInputFilesAndFoldersToBeEnumerated) > 0:
      oInputFileOrFolder = a0oQueuedInputFilesAndFoldersToBeEnumerated.pop(0);
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
        a0oChildren = oInputFileOrFolder.fa0oGetChildren(bParseZipFiles = True);
        if a0oChildren is None:
          oConsole.fOutput(
            COLOR_ERROR, CHAR_ERROR,
            COLOR_NORMAL, " Input zip file ",
            COLOR_INFO, oOutputBaseFolder.sPath,
            COLOR_NORMAL, " cannot be read!",
          );
          sys.exit(guExitCodeCannotReadFromFileSystem);
        a0oQueuedInputFilesAndFoldersToBeEnumerated = a0oChildren + a0oQueuedInputFilesAndFoldersToBeEnumerated;
      else:
        aoInputFiles.append(oInputFileOrFolder);
    uProcessedFolders = 0;
    uProcessedFiles = 0;
    if bExtractFiles:
      for oInputFolder in aoInputFolders:
        sRelativePath = oInputZipFile.fsGetRelativePathTo(oInputFolder);
        o0OutputFolder = oOutputBaseFolder.fo0GetDescendant(sRelativePath, bParseZipFiles = True);
        if not o0OutputFolder:
          oConsole.fOutput(
            COLOR_ERROR, CHAR_ERROR,
            COLOR_NORMAL, " Output folder ",
            COLOR_INFO, oOutputBaseFolder.sPath,
            COLOR_NORMAL, " cannot be found!",
          );
          sys.exit(guExitCodeBadArgument);
        nProgress = 1.0 * (uProcessedFolders + uProcessedFiles) / (len(aoInputFolders) + len(aoInputFiles));
        oConsole.fProgressBar(nProgress, "* %s: Creating folder..." % sRelativePath, bCenterMessage = False);
        if oOutputFolder.fbExists(bParseZipFiles = True):
          if not oOutputFolder.fbIsFolder(bParseZipFiles = True):
            # File exists: error
            oConsole.fOutput(
              COLOR_ERROR, CHAR_ERROR,
              COLOR_NORMAL, "Cannot create folder ",
              COLOR_INFO, sRelativePath,
              COLOR_NORMAL, " in folder ",
              COLOR_INFO, oOutputBaseFolder.sPath,
              COLOR_NORMAL, ": a file with that name already exists!",
            );
            sys.exit(guExitCodeCannotWriteToFileSystem);
          # Folders exists: do nothing
        else:
          # Folders does not exist: create
          if not oOutputFolder.fbCreateAsFolder(bParseZipFiles = True):
            oConsole.fOutput(
              COLOR_ERROR, CHAR_ERROR,
              COLOR_NORMAL, "Cannot create folder ",
              COLOR_INFO, sRelativePath,
              COLOR_NORMAL, " in folder ",
              COLOR_INFO, oOutputBaseFolder.sPath,
              COLOR_NORMAL, "!",
            );
            sys.exit(guExitCodeCannotWriteToFileSystem);
        uProcessedFolders += 1;
      
    for oInputFile in aoInputFiles:
      sRelativePath = oInputZipFile.fsGetRelativePathTo(oInputFile);
      nProgress = 1.0 * (uProcessedFolders + uProcessedFiles) / (len(aoInputFolders) + len(aoInputFiles));
      oConsole.fProgressBar(nProgress, "* %s: reading..." % sRelativePath, bCenterMessage = False);
      sb0Data = oInputFileOrFolder.fsb0Read(bParseZipFiles = True);
      if sb0Data is None:
        oConsole.fOutput(
          COLOR_ERROR, CHAR_ERROR,
          COLOR_NORMAL, "Cannot read input file ",
          COLOR_INFO, sRelativePath,
          COLOR_NORMAL, " in zip file ",
          COLOR_INFO, oInputZipFile.sPath,
          COLOR_NORMAL, "!",
        );
        sys.exit(guExitCodeCannotReadFromFileSystem);
      uTotalBytes += len(sb0Data);
      if bExtractFiles:
        o0OutputFile = oOutputBaseFolder.fo0GetDescendant(sRelativePath, bParseZipFiles = True);
        if o0OutputFile is None:
          oConsole.fOutput(
            COLOR_ERROR, CHAR_ERROR,
            COLOR_NORMAL, "Cannot find output file ",
            COLOR_INFO, sRelativePath,
            COLOR_NORMAL, " in folder ",
            COLOR_INFO, oOutputBaseFolder.sPath,
            COLOR_NORMAL, "!",
          );
          sys.exit(guExitCodeCannotReadFromFileSystem);
        elif o0OutputFile.fbExists(bParseZipFiles = True):
          if not o0OutputFile.fbIsFile(bParseZipFiles = True):
            # Folders exists: error
            oConsole.fOutput(
              COLOR_ERROR, CHAR_ERROR,
              COLOR_NORMAL, "Cannot create file ",
              COLOR_INFO, sRelativePath,
              COLOR_NORMAL, " in folder ",
              COLOR_INFO, oOutputBaseFolder.sPath,
              COLOR_NORMAL, ": a folder with that name already exists!",
            );
            sys.exit(guExitCodeCannotWriteToFileSystem);
          # File exists: overwrite
          oConsole.fProgressBar(nProgress, "* %s: Overwriting (%s)..." % (sRelativePath, fsBytesToHumanReadableString(len(sb0Data))), bCenterMessage = False);
          if not o0OutputFile.fbWrite(sb0Data):
            oConsole.fOutput(
              COLOR_ERROR, CHAR_ERROR,
              COLOR_NORMAL, "Cannot write ",
              COLOR_INFO, fsBytesToHumanReadableString(len(sb0Data)),
              COLOR_NORMAL, " over existing file ",
              COLOR_INFO, sRelativePath,
              COLOR_NORMAL, " in folder ",
              COLOR_INFO, oOutputBaseFolder.sPath,
              COLOR_NORMAL, "!",
            );
            sys.exit(guExitCodeCannotWriteToFileSystem);
        else:
          # File does not exists: create
          oConsole.fProgressBar(nProgress, "* %s: Creating (%s)..." % (sRelativePath, fsBytesToHumanReadableString(len(sb0Data))), bCenterMessage = False);
          if not o0OutputFile.fbCreateAsFile(sb0Data, bParseZipFiles = True):
            oConsole.fOutput(
              COLOR_ERROR, CHAR_ERROR,
              COLOR_NORMAL, " Cannot write ",
              COLOR_INFO, fsBytesToHumanReadableString(len(sb0Data)),
              COLOR_NORMAL, " to new file ",
              COLOR_INFO, sRelativePath,
              COLOR_NORMAL, " in folder ",
              COLOR_INFO, oOutputBaseFolder.sPath,
              COLOR_NORMAL, "!",
            );
            sys.exit(3);
        if bVerbose:
          try:
            uCompressedSize = oInputFileOrFolder.fuGetCompressedSize();
          except Exception as oException:
            oConsole.fOutput(
              COLOR_ERROR, CHAR_ERROR,
              COLOR_NORMAL, " Cannot read compressed file size of ",
              COLOR_INFO, sRelativePath,
              COLOR_NORMAL, " in zip file ",
              COLOR_INFO, oInputZipFile.sPath,
              COLOR_NORMAL, "!",
            );
            raise;
          oConsole.fOutput(
            COLOR_ADD, CHAR_ADD,
            COLOR_NORMAL, " Extracted ",
            COLOR_INFO, sRelativePath,
            COLOR_NORMAL, " (",
            COLOR_INFO, fsBytesToHumanReadableString(uCompressedSize),
            COLOR_NORMAL, " => ",
            COLOR_INFO, fsBytesToHumanReadableString(len(sb0Data)),
            COLOR_NORMAL, ")",
          );
          
      else:
        try:
          uCompressedSize = oInputFileOrFolder.fuGetCompressedSize();
        except Exception as oException:
          oConsole.fOutput(
            COLOR_ERROR, CHAR_ERROR,
            COLOR_NORMAL, " Cannot read compressed file size of ",
            COLOR_INFO, sRelativePath,
            COLOR_NORMAL, " in zip file ",
            COLOR_INFO, oInputZipFile.sPath,
            COLOR_NORMAL, "!",
          );
          raise;
        oConsole.fOutput(
          COLOR_ADD, CHAR_ADD,
          COLOR_NORMAL, " ",
          COLOR_INFO, sRelativePath,
          COLOR_NORMAL, " (",
            COLOR_INFO, fsBytesToHumanReadableString(uCompressedSize),
            COLOR_NORMAL, " => ",
            COLOR_INFO, fsBytesToHumanReadableString(len(sb0Data)),
          COLOR_NORMAL, ")"
        );
      uProcessedFiles += 1;
    
    uTotalFolders = len(aoInputFolders);
    uTotalFiles = len(aoInputFiles);
    
    if not oInputZipFile.fbClose(bThrowErrors = False):
      oConsole.fOutput(
        COLOR_ERROR, CHAR_ERROR,
        COLOR_NORMAL, "Input zip file ",
        COLOR_INFO, oInputZipFile.sPath,
        COLOR_ERROR, " cannot be closed!",
      );
      sys.exit(guExitCodeInternalError);
    
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
      sys.exit(guExitCodeSuccess);
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
    sys.exit(guExitCodeNothingToDo if uTotalFiles == 0 else guExitCodeSuccess);

except Exception as oException:
  if m0DebugOutput:
    m0DebugOutput.fTerminateWithException(oException, guExitCodeInternalError);
  raise;