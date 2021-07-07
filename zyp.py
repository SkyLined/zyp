import re, sys;

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

from fInitializeProduct import fInitializeProduct;
fInitializeProduct();

try: # mDebugOutput use is Optional
  import mDebugOutput as m0DebugOutput;
except ModuleNotFoundError as oException:
  if oException.args[0] != "No module named 'mDebugOutput'":
    raise;
  m0DebugOutput = None;

try:
  from mFileSystemItem import cFileSystemItem;
  from mHumanReadable import fsBytesToHumanReadableString;
  from mConsole import oConsole;
  
  from fasSortedAlphabetically import fasSortedAlphabetically;
  from fatsArgumentLowerNameAndValue import fatsArgumentLowerNameAndValue;
  from mColors import *;
  
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
          oConsole.fOutput(ERROR, "The mDebugOutput module is not available!");
          sys.exit(2);
        m0DebugOutput.fEnableAllDebugOutput();
      elif s0LowerName:
        fExitWithError("Unknown argument \"%s\"" % sArgument);
      else:
        asFilesAndFoldersPathsAndPatterns.append(sArgument);
    if len(asFilesAndFoldersPathsAndPatterns) == 0:
      oConsole.fOutput(ERROR, "Missing input file or folder argument!");
      sys.exit(2);
    if len(asFilesAndFoldersPathsAndPatterns) == 1:
      oConsole.fOutput(ERROR, "Missing output zip file argument!");
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
          oConsole.fOutput(ERROR, "Input file or folder pattern ", ERROR_INFO, oInputFileOrFolder.sPath, ERROR, " does not match anything!");
          sys.exit(4);
        if bVerbose:
          oConsole.fOutput("+ Pattern ", INFO, str(sPattern), NORMAL, " matches ", INFO, str(len(aoInputFilesAndFolders)), NORMAL,
              " files/folders:");
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
          oConsole.fOutput(ERROR, "Input file or folder ", ERROR_INFO, oInputFileOrFolder.sPath, ERROR, " not found!");
          sys.exit(4);
        if bVerbose and bAddedAllFilesInAFolder:
          if len(aoInputFiles) == 0:
            oConsole.fOutput("  " if bContainsWildcard else "", "- Folder ", INFO, oInputFileOrFolder.sName, NORMAL, "/ contains no files.");
          else:
            oConsole.fOutput("  " if bContainsWildcard else "", "+ Folder ", INFO, oInputFileOrFolder.sName, NORMAL, "/ containing ",
              INFO, str(len(aoInputFiles)), NORMAL, " files:");
        for oInputFile in aoInputFiles:
          sRelativePath = oBaseFolder.fsGetRelativePathTo(oInputFile);
          if sRelativePath in doInputFile_by_sRelativePathInOutputZip:
            oPreviousInputFile = doInputFile_by_sRelativePathInOutputZip[sRelativePath];
            if oPreviousInputFile.sWindowsPath == oInputFile.sWindowsPath:
              # Requesting to add the same file multiple times will result in it being added once:
              if bVerbose:
                oConsole.fOutput(
                  "  " if bContainsWildcard else "", "  " if bAddedAllFilesInAFolder else "",
                  "- File ", INFO, oBaseFolder.fsGetRelativePathTo(oInputFile), NORMAL, " already added."
                );
              continue;
            oConsole.fOutput(
              ERROR, "Input files ", ERROR_INFO, oPreviousInputFile.sPath, ERROR, " and ",
              ERROR_INFO, oInputFile.sPath, ERROR, " cannot both be stored as ", ERROR_INFO, sRelativePath, ERROR, "!"
            );
            sys.exit(2);
          if bVerbose:
            oConsole.fOutput(
              "  " if bContainsWildcard else "", "  " if bAddedAllFilesInAFolder else "",
              "+ File ", INFO, oBaseFolder.fsGetRelativePathTo(oInputFile), NORMAL, " (", INFO, fsBytesToHumanReadableString(oInputFile.fuGetSize()), NORMAL, ")."
            );
          doInputFile_by_sRelativePathInOutputZip[sRelativePath] = oInputFile;
    if oOutputZipFile.fbExists(bParseZipFiles = True):
      try:
        oOutputZipFile.fbDelete(bParseZipFiles = True, bThrowErrors = True);
      except Exception as oException:
        oConsole.fOutput(ERROR, "Existing output zip file ", ERROR_INFO, oOutputZipFile.sPath, ERROR, " cannot be deleted: ", ERROR_INFO, repr(oException), ERROR, "!");
        sys.exit(5);
      if bVerbose:
        oConsole.fOutput("+ Deleted existing zip file ", INFO, oOutputZipFile.sPath, NORMAL, ".");
    try:
      oOutputZipFile.fbCreateAsZipFile(bParseZipFiles = True, bKeepOpen = True, bThrowErrors = True);
    except Exception as oException:
      oConsole.fOutput(ERROR, "Output zip file ", ERROR_INFO, oOutputZipFile.sPath, ERROR, " cannot be created: ", ERROR_INFO, repr(oException), ERROR, "!");
      sys.exit(5);
    uTotalFiles = len(doInputFile_by_sRelativePathInOutputZip);
    if bVerbose:
      oConsole.fOutput("* Adding ", INFO, str(uTotalFiles), NORMAL, " files to ", INFO, oOutputZipFile.sPath, NORMAL, ":");
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
            ERROR, "Cannot write ", ERROR_INFO, fsBytesToHumanReadableString(len(sbData)), ERROR,
            " over existing file ", ERROR_INFO, sRelativePath, ERROR,
            " in zip file ", ERROR_INFO, oOutputZipFile.sPath, ERROR, ":", ERROR_INFO, repr(oException), ERROR, "!"
          );
          sys.exit(5);
      else:
        oConsole.fProgressBar(nProgress, "* %s: Creating (%s)..." % (sRelativePath, fsBytesToHumanReadableString(len(sbData))));
        try:
          oOutputFile.fbCreateAsFile(sbData, bParseZipFiles = True, bThrowErrors = True);
        except Exception as oException:
          oConsole.fOutput(
            ERROR, "Cannot write ", ERROR_INFO, fsBytesToHumanReadableString(len(sbData)), ERROR,
            " to new file ", ERROR_INFO, sRelativePath, ERROR,
            " in zip file ", ERROR_INFO, oOutputZipFile.sPath, ERROR, ":", ERROR_INFO, repr(oException), ERROR, "!"
          );
          sys.exit(5);
      uProcessedBytes += len(sbData);
      uProcessedFiles += 1;
    
    try:
      oOutputZipFile.fbClose(bThrowErrors = True);
    except Exception as oException:
      oConsole.fOutput(ERROR, "Output zip file ", ERROR_INFO, oOutputZipFile.sPath, ERROR, " cannot be closed:", ERROR_INFO, repr(oException), ERROR, "!");
      sys.exit(5);
    
    uFileSizeInBytes = oOutputZipFile.fuGetSize();
    oConsole.fOutput(
      "Added ", INFO, fsBytesToHumanReadableString(uProcessedBytes), NORMAL, ", resulting in a ",
      INFO, fsBytesToHumanReadableString(uFileSizeInBytes), NORMAL, " zip file (",
      INFO, str(uFileSizeInBytes * 100 / uProcessedBytes), NORMAL, "% of original size)."
    );
    sys.exit(0 if uProcessedFiles == 0 else 1);

except Exception as oException:
  if m0DebugOutput:
    m0DebugOutput.fTerminateWithException(oException);
  raise;