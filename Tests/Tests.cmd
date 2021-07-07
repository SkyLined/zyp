@ECHO OFF
SETLOCAL
SET REDIRECT_STDOUT_FILE_PATH=%TEMP%\zyp Test stdout %RANDOM%.txt
SET TEST_FILE_PATH=%TEMP%\zyp Test file %RANDOM%.txt
SET TEST_ZIP_FILE_PATH=%TEMP%\zyp Test file %RANDOM%.zip

ECHO   * Test usage help...
CALL "%~dp0\..\zyp.cmd" --help >"%REDIRECT_STDOUT_FILE_PATH%"
IF ERRORLEVEL 1 GOTO :ERROR
CALL "%~dp0\..\unzyp.cmd" --help >"%REDIRECT_STDOUT_FILE_PATH%"
IF ERRORLEVEL 1 GOTO :ERROR
ECHO   * Test version info...
CALL "%~dp0\..\zyp.cmd" --version >"%REDIRECT_STDOUT_FILE_PATH%"
IF ERRORLEVEL 1 GOTO :ERROR
CALL "%~dp0\..\unzyp.cmd" --version >"%REDIRECT_STDOUT_FILE_PATH%"
IF ERRORLEVEL 1 GOTO :ERROR
ECHO   * Test version check...
CALL "%~dp0\..\zyp.cmd" --version-check >"%REDIRECT_STDOUT_FILE_PATH%"
IF ERRORLEVEL 1 GOTO :ERROR
CALL "%~dp0\..\unzyp.cmd" --version-check >"%REDIRECT_STDOUT_FILE_PATH%"
IF ERRORLEVEL 1 GOTO :ERROR
ECHO   * Test license info...
CALL "%~dp0\..\zyp.cmd" --license >"%REDIRECT_STDOUT_FILE_PATH%"
IF ERRORLEVEL 1 GOTO :ERROR
CALL "%~dp0\..\unzyp.cmd" --license >"%REDIRECT_STDOUT_FILE_PATH%"
IF ERRORLEVEL 1 GOTO :ERROR
ECHO   * Test license update...
CALL "%~dp0\..\zyp.cmd" --license-update >"%REDIRECT_STDOUT_FILE_PATH%"
IF ERRORLEVEL 1 GOTO :ERROR
CALL "%~dp0\..\unzyp.cmd" --license-update >"%REDIRECT_STDOUT_FILE_PATH%"
IF ERRORLEVEL 1 GOTO :ERROR

DEL "%REDIRECT_STDOUT_FILE_PATH%" /Q

ECHO   * Zipping test file...
ECHO Hello, world! >"%TEST_FILE_PATH%"
IF ERRORLEVEL 1 GOTO :ERROR
CALL "%~dp0\..\zyp.cmd" "%TEST_FILE_PATH%" "%TEST_ZIP_FILE_PATH%"
IF NOT %ERRORLEVEL% == 1 GOTO :ERROR
DEL "%TEST_FILE_PATH%" /Q

ECHO   * Listing zipped test file...
CALL "%~dp0\..\unzyp.cmd" --list "%TEST_ZIP_FILE_PATH%"
IF ERRORLEVEL 1 GOTO :ERROR

ECHO   * Unzipping test file...
CALL "%~dp0\..\unzyp.cmd" "%TEST_ZIP_FILE_PATH%" "%TEMP%"
IF NOT %ERRORLEVEL% == 1 GOTO :ERROR
IF NOT EXIST "%TEST_FILE_PATH%" (
  ECHO Unzipping did not re-create test file!
  DEL %TEST_ZIP_FILE_PATH% /Q
  ENDLOCAL
  EXIT /B 1
)
DEL "%TEST_FILE_PATH%" /Q
DEL "%TEST_ZIP_FILE_PATH%" /Q

ECHO + Test.cmd completed.
ENDLOCAL
EXIT /B 0

:ERROR
  ECHO     - Failed with error level %ERRORLEVEL%
  CALL :CLEANUP
  ENDLOCAL
  EXIT /B 3

:CLEANUP
  IF EXIST "%TEST_FILE_PATH%" (
    DEL "%TEST_FILE_PATH%" /Q
  )
  IF EXIST "%TEST_ZIP_FILE_PATH%" (
    DEL "%TEST_ZIP_FILE_PATH%" /Q
  )
  IF EXIST "%REDIRECT_STDOUT_FILE_PATH%" (
    TYPE "%REDIRECT_STDOUT_FILE_PATH%"
    DEL "%REDIRECT_STDOUT_FILE_PATH%" /Q
  )
