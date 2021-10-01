"""                                                                             
        .dSSSSSSSP' YSb   ,dSP' iSSSSSSb                                        
            ,dSP'    YSb,dSP'  iSP` _7SP     Python zip compression utility     
          ,dSP'       )dSP'   iSSSSSS*'                                         
        ,dSP'       ,dSP'    iSP`          http://github.com/SkyLined/zyp       
      .dSSSSSSP'  .dSP'     iSP`                                                
                                                                            """;

import os, re, sys;

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
  
  from fasSortedAlphabetically import fasSortedAlphabetically;
  from fatsArgumentLowerNameAndValue import fatsArgumentLowerNameAndValue;
  from mColorsAndChars import *;
  from mExitCodes import *;
  
  if __name__ == "__main__":
    # Parse arguments
    asFilesAndFoldersPathsAndPatterns = [];
    sOutputZipFilePath = None;
    bVerbose = False;
    for (sArgument, s0LowerName, s0Value) in fatsArgumentLowerNameAndValue():
      if s0LowerName in ["-v", "/v", "--verbose", "/verbose"]:
        bVerbose = True;
      elif s0LowerName in ["-d", "/d", "--debug", "/debug"]:
        if m0DebugOutput is None:
          oConsole.fOutput(
            COLOR_ERROR, CHAR_ERROR,
            COLOR_NORMAL, " The mDebugOutput module is not available!",
          );
          sys.exit(2);
        m0DebugOutput.fEnableAllDebugOutput();
      elif s0LowerName:
        fExitWithError("Unknown argument \"%s\"" % sArgument);
      else:
        asFilesAndFoldersPathsAndPatterns.append(sArgument);
    if len(asFilesAndFoldersPathsAndPatterns) == 0:
      oConsole.fOutput(
        COLOR_ERROR, CHAR_ERROR,
        COLOR_NORMAL, " Missing input file or folder argument!",
      );
      sys.exit(2);
    if len(asFilesAndFoldersPathsAndPatterns) == 1:
      oConsole.fOutput(
          COLOR_ERROR, CHAR_ERROR,
          COLOR_NORMAL, " Missing output zip file argument!",
        );
      sys.exit(2);
    
    asInputFilesAndFoldersPathsAndPatterns = asFilesAndFoldersPathsAndPatterns[:-1];
    sOutputZipFilePath = asFilesAndFoldersPathsAndPatterns[-1];
    oOutputZipFile = cFileSystemItem(sOutputZipFilePath);
    
    doInputFile_by_sRelativePathInOutputZip = {};
    for sInputFilesAndFoldersPathOrPattern in asInputFilesAndFoldersPathsAndPatterns:
      # Handle wildcards:
      bContainsWildcard = "*" in sInputFilesAndFoldersPathOrPattern or "?" in sInputFilesAndFoldersPathOrPattern;
      if bContainsWildcard:
        # Create a FileSystemItem for the pattern. This which does not represent an actual file or folder.
        # It will only be used to split the base folder and the pattern.
        oInputFilesAndFoldersPatternFileSystemItem = cFileSystemItem(sInputFilesAndFoldersPathOrPattern);
        oInputFilesAndFoldersPatternBaseFolder = oInputFilesAndFoldersPatternFileSystemItem.oParent;
        sPattern = oInputFilesAndFoldersPatternFileSystemItem.sName;
        rPattern = re.compile("^%s$" % re.escape(sPattern).replace("\\*", ".*").replace("\\?", "."));
        aoInputFilesAndFolders = [
          oChildFileOrFolder
          for oChildFileOrFolder in oInputFilesAndFoldersPatternBaseFolder.faoGetChildren(bParseZipFiles = True)
          if rPattern.match(oChildFileOrFolder.sName)
        ];
        if len(aoInputFilesAndFolders) == 0:
          oConsole.fOutput(
            COLOR_ERROR, CHAR_ERROR,
            COLOR_NORMAL, " Input file or folder pattern ",
            COLOR_INFO, oInputFileOrFolder.sPath,
            COLOR_ERROR, " does not match anything!",
          );
          sys.exit(4);
        if bVerbose:
          oConsole.fOutput(
            COLOR_OK, CHAR_OK,
            COLOR_NORMAL, " Pattern ",
            COLOR_INFO, str(sPattern),
            COLOR_NORMAL, " matches ",
            COLOR_INFO, str(len(aoInputFilesAndFolders)),
            COLOR_NORMAL, " files/folders:",
          );
      else:
        oInputFileOrFolder = cFileSystemItem(sInputFilesAndFoldersPathOrPattern);
        aoInputFilesAndFolders = [oInputFileOrFolder];
      # Add the given or matched files and all descendant files of the given or matched folders to the list of files to add.
      for oInputFileOrFolder in aoInputFilesAndFolders:
        if oInputFileOrFolder.fbIsFile(bParseZipFiles = True):
          bAddedAllFilesInAFolder = False;
          oBaseFolder = oInputFileOrFolder.oParent;
          aoInputFiles = [oInputFileOrFolder];
        elif oInputFileOrFolder.fbIsFolder(bParseZipFiles = True):
          bAddedAllFilesInAFolder = True;
          oBaseFolder = oInputFileOrFolder;
          aoInputFiles = [
            oInputFileOrFolder
            for oInputFileOrFolder in oBaseFolder.faoGetDescendants()
            if (
              oInputFileOrFolder.sPath != oOutputZipFile.sPath
              and oInputFileOrFolder.fbIsFile(bParseZipFiles = True)
            )
          ];
        else:
          oConsole.fOutput(
            COLOR_ERROR, CHAR_ERROR,
            COLOR_NORMAL, " Input file or folder ",
            COLOR_INFO, oInputFileOrFolder.sPath,
            COLOR_ERROR, " not found!",
          );
          sys.exit(4);
        if bVerbose and bAddedAllFilesInAFolder:
          if len(aoInputFiles) == 0:
            oConsole.fOutput("  " if bContainsWildcard else "", "- Folder ", COLOR_INFO, oInputFileOrFolder.sName, COLOR_NORMAL, "/ contains no files.");
          else:
            oConsole.fOutput("  " if bContainsWildcard else "", "+ Folder ", COLOR_INFO, oInputFileOrFolder.sName, COLOR_NORMAL, "/ containing ",
              COLOR_INFO, str(len(aoInputFiles)), COLOR_NORMAL, " files:");
        for oInputFile in aoInputFiles:
          sRelativePath = oBaseFolder.fsGetRelativePathTo(oInputFile);
          if sRelativePath in doInputFile_by_sRelativePathInOutputZip:
            oPreviousInputFile = doInputFile_by_sRelativePathInOutputZip[sRelativePath];
            if oPreviousInputFile.sWindowsPath == oInputFile.sWindowsPath:
              # Requesting to add the same file multiple times will result in it being added once:
              if bVerbose:
                oConsole.fOutput(
                  "  " if bContainsWildcard else "", "  " if bAddedAllFilesInAFolder else "",
                  "- File ", COLOR_INFO, oBaseFolder.fsGetRelativePathTo(oInputFile), COLOR_NORMAL, " already added."
                );
              continue;
            oConsole.fOutput(
              COLOR_ERROR, CHAR_ERROR,
              COLOR_NORMAL, " Input files ",
              COLOR_INFO, oPreviousInputFile.sPath,
              COLOR_ERROR, " and ",
              COLOR_INFO, oInputFile.sPath,
              COLOR_ERROR, " cannot both be stored as ",
              COLOR_INFO, sRelativePath,
              COLOR_ERROR, "!",
            );
            sys.exit(2);
          if bVerbose:
            oConsole.fOutput(
              "  " if bContainsWildcard else "", "  " if bAddedAllFilesInAFolder else "",
              "+ File ", COLOR_INFO, oBaseFolder.fsGetRelativePathTo(oInputFile), COLOR_NORMAL, " (", COLOR_INFO, fsBytesToHumanReadableString(oInputFile.fuGetSize()), COLOR_NORMAL, ")."
            );
          doInputFile_by_sRelativePathInOutputZip[sRelativePath] = oInputFile;
    if oOutputZipFile.fbExists(bParseZipFiles = True):
      try:
        oOutputZipFile.fbDelete(bParseZipFiles = True, bThrowErrors = True);
      except Exception as oException:
        oConsole.fOutput(
          COLOR_ERROR, CHAR_ERROR,
          COLOR_NORMAL, " Existing output zip file ",
          COLOR_INFO, oOutputZipFile.sPath,
          COLOR_ERROR, " cannot be deleted: ",
          COLOR_INFO, repr(oException),
          COLOR_ERROR, "!",
        );
        sys.exit(5);
      if bVerbose:
        oConsole.fOutput(
          COLOR_OK, CHAR_OK,
          COLOR_NORMAL, " Deleted existing zip file ",
          COLOR_INFO, oOutputZipFile.sPath,
          COLOR_NORMAL, ".",
        );
    try:
      oOutputZipFile.fbCreateAsZipFile(bParseZipFiles = True, bKeepOpen = True, bThrowErrors = True);
    except Exception as oException:
      oConsole.fOutput(
        COLOR_ERROR, CHAR_ERROR,
        COLOR_NORMAL, " Output zip file ",
        COLOR_INFO, oOutputZipFile.sPath,
        COLOR_ERROR, " cannot be created: ",
        COLOR_INFO, repr(oException),
        COLOR_ERROR, "!",
      );
      sys.exit(5);
    uTotalFiles = len(doInputFile_by_sRelativePathInOutputZip);
    if bVerbose:
      oConsole.fOutput(
        "* Adding ",
        COLOR_INFO, str(uTotalFiles),
        COLOR_NORMAL, " files to ",
        COLOR_INFO, oOutputZipFile.sPath,
        COLOR_NORMAL, ":",
      );
    uProcessedBytes = 0;
    uProcessedFiles = 0;
    for sRelativePath in fasSortedAlphabetically(doInputFile_by_sRelativePathInOutputZip.keys()):
      oInputFile = doInputFile_by_sRelativePathInOutputZip[sRelativePath];
      oOutputFile = oOutputZipFile.foGetDescendant(sRelativePath, bParseZipFiles = True);
      nProgress = 1.0 * uProcessedFiles / uTotalFiles;
      oConsole.fProgressBar(nProgress, "* %s: Reading..." % sRelativePath);
      sbData = oInputFile.fsbRead();
      if oOutputFile.fbIsFile(bParseZipFiles = True):
        oConsole.fProgressBar(nProgress, "* %s: Overwriting (%s)..." % (sRelativePath, fsBytesToHumanReadableString(len(sbData))));
        try:
          oOutputFile.fbWrite(sbData, bThrowErrors = True);
        except Exception as oException:
          oConsole.fOutput(
            COLOR_ERROR, CHAR_ERROR,
            COLOR_NORMAL, " Cannot write ",
            COLOR_INFO, fsBytesToHumanReadableString(len(sbData)),
            COLOR_ERROR, " over existing file ",
            COLOR_INFO, sRelativePath,
            COLOR_ERROR, " in zip file ",
            COLOR_INFO, oOutputZipFile.sPath,
            COLOR_ERROR, ":",
            COLOR_INFO, repr(oException),
            COLOR_ERROR, "!",
          );
          sys.exit(5);
      else:
        oConsole.fProgressBar(nProgress, "* %s: Creating (%s)..." % (sRelativePath, fsBytesToHumanReadableString(len(sbData))));
        try:
          oOutputFile.fbCreateAsFile(sbData, bParseZipFiles = True, bThrowErrors = True);
        except Exception as oException:
          oConsole.fOutput(
            COLOR_ERROR, CHAR_ERROR,
            COLOR_NORMAL, " Cannot write ",
            COLOR_INFO, fsBytesToHumanReadableString(len(sbData)),
            COLOR_ERROR, " to new file ",
            COLOR_INFO, sRelativePath,
            COLOR_ERROR, " in zip file ",
            COLOR_INFO, oOutputZipFile.sPath,
            COLOR_ERROR, ":",
            COLOR_INFO, repr(oException),
            COLOR_ERROR, "!",
          );
          sys.exit(5);
      uProcessedBytes += len(sbData);
      uProcessedFiles += 1;
    
    try:
      oOutputZipFile.fbClose(bThrowErrors = True);
    except Exception as oException:
      oConsole.fOutput(
        COLOR_ERROR, CHAR_ERROR,
        COLOR_NORMAL, " Output zip file ",
        COLOR_INFO, oOutputZipFile.sPath,
        COLOR_ERROR, " cannot be closed:",
        COLOR_INFO, str(oException),
        COLOR_ERROR, "!",
      );
      sys.exit(5);
    
    uFileSizeInBytes = oOutputZipFile.fuGetSize();
    oConsole.fOutput(
      COLOR_OK, CHAR_OK,
      COLOR_NORMAL, " Added ",
      COLOR_INFO, fsBytesToHumanReadableString(uProcessedBytes),
      COLOR_NORMAL, ", resulting in a ",
      COLOR_INFO, fsBytesToHumanReadableString(uFileSizeInBytes),
      COLOR_NORMAL, " zip file (",
      COLOR_INFO, str(uFileSizeInBytes * 100 / uProcessedBytes),
      COLOR_NORMAL, "% of original size).",
    );
    sys.exit(0 if uProcessedFiles == 0 else 1);
   
except Exception as oException:
  if m0DebugOutput:
    m0DebugOutput.fTerminateWithException(oException, guExitCodeInternalError);
  raise;