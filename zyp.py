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
          sys.exit(guExitCodeBadArgument);
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
      sys.exit(guExitCodeBadArgument);
    if len(asFilesAndFoldersPathsAndPatterns) == 1:
      oConsole.fOutput(
          COLOR_ERROR, CHAR_ERROR,
          COLOR_NORMAL, " Missing output zip file argument!",
        );
      sys.exit(guExitCodeBadArgument);
    
    asInputFilesAndFoldersPathsAndPatterns = asFilesAndFoldersPathsAndPatterns[:-1];
    sOutputZipFilePath = asFilesAndFoldersPathsAndPatterns[-1];
    oOutputZipFile = cFileSystemItem(sOutputZipFilePath);
    
    doInputFile_by_sRelativePathInOutputZip = {};
    for sInputFilesAndFoldersPathOrPattern in asInputFilesAndFoldersPathsAndPatterns:
      # Handle wildcards:
      bContainsWildcard = "*" in sInputFilesAndFoldersPathOrPattern or "?" in sInputFilesAndFoldersPathOrPattern;
      if bContainsWildcard:
        # Create a FileSystemItem for the pattern. This does not represent an actual file or folder.
        # It will only be used to split the base folder and the pattern.
        oInputFilesAndFoldersPatternFileSystemItem = cFileSystemItem(sInputFilesAndFoldersPathOrPattern);
        o0InputFilesAndFoldersPatternBaseFolder = oInputFilesAndFoldersPatternFileSystemItem.o0Parent;
        if o0InputFilesAndFoldersPatternBaseFolder is None:
          oConsole.fOutput(
            COLOR_ERROR, CHAR_ERROR,
            COLOR_NORMAL, " Input file or folder pattern ",
            COLOR_INFO, sInputFilesAndFoldersPathOrPattern,
            COLOR_NORMAL, " is invalid!",
          );
          sys.exit(guExitCodeCannotReadFromFileSystem);
        sPattern = oInputFilesAndFoldersPatternFileSystemItem.sName;
        rPattern = re.compile("^%s$" % re.escape(sPattern).replace("\\*", ".*").replace("\\?", "."));
        a0oChildren = o0InputFilesAndFoldersPatternBaseFolder.fa0oGetChildren(bParseZipFiles = True);
        if a0oChildren is None:
          oConsole.fOutput(
            COLOR_ERROR, CHAR_ERROR,
            COLOR_NORMAL, " Input file or folder pattern base folder ",
            COLOR_INFO, oInputFilesAndFoldersPatternBaseFolder.sPath,
            COLOR_NORMAL, " cannot be read!",
          );
          sys.exit(guExitCodeCannotReadFromFileSystem);
        aoInputFilesAndFolders = [
          oChildFileOrFolder
          for oChildFileOrFolder in a0oChildren
          if rPattern.match(oChildFileOrFolder.sName)
        ];
        if len(aoInputFilesAndFolders) == 0:
          oConsole.fOutput(
            COLOR_ERROR, CHAR_ERROR,
            COLOR_NORMAL, " Input file or folder pattern ",
            COLOR_INFO, sInputFilesAndFoldersPathOrPattern,
            COLOR_NORMAL, " does not match anything!",
          );
          sys.exit(guExitCodeBadArgument);
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
          oBaseFolder = oInputFileOrFolder.o0Parent; # Could return None, so assert to make sure it doesn't.
          assert oBaseFolder, \
              "Input file %s does not have a parent folder!?" % oInputFileOrFolder;
          aoInputFiles = [oInputFileOrFolder];
        elif oInputFileOrFolder.fbIsFolder(bParseZipFiles = True):
          bAddedAllFilesInAFolder = True;
          oBaseFolder = oInputFileOrFolder;
          a0oDescendants = oBaseFolder.fa0oGetDescendants(bParseZipFiles = True);
          if a0oDescendants is None:
            oConsole.fOutput(
              COLOR_ERROR, CHAR_ERROR,
              COLOR_NORMAL, " Input folder ",
              COLOR_INFO, oInputFileOrFolder.sPath,
              COLOR_NORMAL, " cannot be read!",
            );
            sys.exit(guExitCodeCannotReadFromFileSystem);
          aoInputFiles = [
            oInputFileOrFolder
            for oInputFileOrFolder in a0oDescendants
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
            COLOR_NORMAL, " not found!",
          );
          sys.exit(guExitCodeBadArgument);
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
              COLOR_NORMAL, " and ",
              COLOR_INFO, oInputFile.sPath,
              COLOR_NORMAL, " cannot both be stored as ",
              COLOR_INFO, sRelativePath,
              COLOR_NORMAL, "!",
            );
            sys.exit(guExitCodeBadArgument);
          if bVerbose:
            u0Size = oInputFile.fu0GetSize(bThrowErrors = False);
            if u0Size is None:
              oConsole.fOutput(
                COLOR_ERROR, CHAR_ERROR,
                COLOR_NORMAL, " Cannot get size of input files ",
                COLOR_INFO, oInputFile.sPath,
                COLOR_NORMAL, "!",
              );
              sys.exit(guExitCodeCannotReadFromFileSystem);
            oConsole.fOutput(
              "  " if bContainsWildcard else "",
              "  " if bAddedAllFilesInAFolder else "",
              "+ File ",
              COLOR_INFO, oBaseFolder.fsGetRelativePathTo(oInputFile),
              COLOR_NORMAL, " (",
              COLOR_INFO, fsBytesToHumanReadableString(u0Size),
              COLOR_NORMAL, ")."
            );
          doInputFile_by_sRelativePathInOutputZip[sRelativePath] = oInputFile;
    if oOutputZipFile.fbExists(bParseZipFiles = True):
      if not oOutputZipFile.fbDelete(bParseZipFiles = True):
        oConsole.fOutput(
          COLOR_ERROR, CHAR_ERROR,
          COLOR_NORMAL, " Existing output zip file ",
          COLOR_INFO, oOutputZipFile.sPath,
          COLOR_NORMAL, " cannot be deleted!",
        );
        sys.exit(guExitCodeCannotWriteToFileSystem);
      if bVerbose:
        oConsole.fOutput(
          COLOR_OK, CHAR_OK,
          COLOR_NORMAL, " Deleted existing zip file ",
          COLOR_INFO, oOutputZipFile.sPath,
          COLOR_NORMAL, ".",
        );
    if not oOutputZipFile.fbCreateAsZipFile(bParseZipFiles = True, bKeepOpen = True):
      oConsole.fOutput(
        COLOR_ERROR, CHAR_ERROR,
        COLOR_NORMAL, " Output zip file ",
        COLOR_INFO, oOutputZipFile.sPath,
        COLOR_NORMAL, " cannot be created!",
      );
      sys.exit(guExitCodeCannotWriteToFileSystem);
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
      oOutputFile = oOutputZipFile.fo0GetDescendant(sRelativePath, bParseZipFiles = True);
      nProgress = 1.0 * uProcessedFiles / uTotalFiles;
      oConsole.fProgressBar(nProgress, "* %s: Reading..." % sRelativePath);
      sb0Data = oInputFile.fsb0Read(bThrowErrors = False);
      if sb0Data is None:
        oConsole.fOutput(
          COLOR_ERROR, CHAR_ERROR,
          COLOR_NORMAL, " Cannot read input file ",
          COLOR_INFO, oInputFile.sPath,
          COLOR_NORMAL, "!",
        );
        sys.exit(guExitCodeCannotReadFRomFileSystem);
      if oOutputFile.fbIsFile(bParseZipFiles = True):
        oConsole.fProgressBar(nProgress, "* %s: Overwriting (%s)..." % (sRelativePath, fsBytesToHumanReadableString(len(sb0Data))));
        if not oOutputFile.fbWrite(sb0Data):
          oConsole.fOutput(
            COLOR_ERROR, CHAR_ERROR,
            COLOR_NORMAL, " Cannot write ",
            COLOR_INFO, fsBytesToHumanReadableString(len(sb0Data)),
            COLOR_NORMAL, " over existing file ",
            COLOR_INFO, sRelativePath,
            COLOR_NORMAL, " in zip file ",
            COLOR_INFO, oOutputZipFile.sPath,
            COLOR_NORMAL, "!",
          );
          sys.exit(guExitCodeCannotWriteToFileSystem);
      else:
        oConsole.fProgressBar(nProgress, "* %s: Creating (%s)..." % (sRelativePath, fsBytesToHumanReadableString(len(sb0Data))));
        if not oOutputFile.fbCreateAsFile(sb0Data, bParseZipFiles = True):
          oConsole.fOutput(
            COLOR_ERROR, CHAR_ERROR,
            COLOR_NORMAL, " Cannot write ",
            COLOR_INFO, fsBytesToHumanReadableString(len(sb0Data)),
            COLOR_NORMAL, " to new file ",
            COLOR_INFO, sRelativePath,
            COLOR_NORMAL, " in zip file ",
            COLOR_INFO, oOutputZipFile.sPath,
            COLOR_NORMAL, "!",
          );
          sys.exit(guExitCodeCannotWriteToFileSystem);
      if bVerbose:
        u0CompressedSize = oOutputFile.fu0GetCompressedSize(bThrowErrors = False);
        if u0CompressedSize is None:
          oConsole.fOutput(
            COLOR_ERROR, CHAR_ERROR,
            COLOR_NORMAL, " Cannot read compressed file size of ",
            COLOR_INFO, sRelativePath,
            COLOR_NORMAL, " in zip file ",
            COLOR_INFO, oOutputZipFile.sPath,
            COLOR_NORMAL, "!",
          );
          sys.exit(guExitCodeCannotReadFromFileSystem);
        oConsole.fOutput(
          COLOR_ADD, CHAR_ADD,
          COLOR_NORMAL, " Added ",
          COLOR_INFO, sRelativePath,
          COLOR_NORMAL, " (",
          COLOR_INFO, fsBytesToHumanReadableString(len(sb0Data)),
          COLOR_NORMAL, " => ",
          COLOR_INFO, fsBytesToHumanReadableString(),
          COLOR_NORMAL, ")",
        );
      uProcessedBytes += len(sb0Data);
      uProcessedFiles += 1;
    
    if not oOutputZipFile.fbClose(bThrowErrors = False):
      oConsole.fOutput(
        COLOR_ERROR, CHAR_ERROR,
        COLOR_NORMAL, " Output zip file ",
        COLOR_INFO, oOutputZipFile.sPath,
        COLOR_NORMAL, " cannot be closed!",
      );
      sys.exit(guExitCodeCannotWriteToFileSystem);
    
    u0FileSizeInBytes = oOutputZipFile.fu0GetSize(bThrowErrors = False);
    if u0FileSizeInBytes is None:
      oConsole.fOutput(
        COLOR_ERROR, CHAR_ERROR,
        COLOR_NORMAL, " Cannot get file size of output zip file ",
        COLOR_INFO, oOutputZipFile.sPath,
        COLOR_NORMAL, "!",
      );
      sys.exit(guExitCodeCannotReadFromFileSystem);
    oConsole.fOutput(
      COLOR_OK, CHAR_OK,
      COLOR_NORMAL, " Added ",
      COLOR_INFO, fsBytesToHumanReadableString(uProcessedBytes),
      COLOR_NORMAL, ", resulting in a ",
      COLOR_INFO, fsBytesToHumanReadableString(u0FileSizeInBytes),
      COLOR_NORMAL, " zip file (",
      COLOR_INFO, str(u0FileSizeInBytes * 100 / uProcessedBytes),
      COLOR_NORMAL, "% of original size).",
    );
    sys.exit(guExitCodeNothingToDo if uProcessedFiles == 0 else guExitCodeSuccess);
   
except Exception as oException:
  if m0DebugOutput:
    m0DebugOutput.fTerminateWithException(oException, guExitCodeInternalError);
  raise;