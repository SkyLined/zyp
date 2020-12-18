@ECHO OFF
SETLOCAL
SET _NT_SYMBOL_PATH=

IF "%~1" == "--all" (
  REM If you can add the x86 and x64 binaries of python to the path, or add links to the local folder, tests will be run
  REM in both
  WHERE PYTHON_X86 >nul 2>&1
  IF NOT ERRORLEVEL 0 (
    ECHO - PYTHON_X86 was not found; not testing both x86 and x64 ISAs.
  ) ELSE (
    WHERE PYTHON_X64 >nul 2>&1
    IF NOT ERRORLEVEL 0 (
      ECHO - PYTHON_X64 was not found; not testing both x86 and x64 ISAs.
    ) ELSE (
      GOTO :TEST_BOTH_ISAS
    )
  )
)

WHERE PYTHON 2>&1 >nul
IF ERRORLEVEL 1 (
  ECHO - PYTHON was not found!
  ENDLOCAL
  EXIT /B 1
)

CALL PYTHON "%~dpn0\%~n0.py" %*
IF ERRORLEVEL 1 GOTO :ERROR
ENDLOCAL
GOTO :ADDITIONAL_TESTS

:TEST_BOTH_ISAS
  ECHO * Running tests in x86 build of Python...
  CALL PYTHON_X86 "%~dpn0\%~n0.py" %*
  IF ERRORLEVEL 1 GOTO :ERROR
  ECHO * Running tests in x64 build of Python...
  CALL PYTHON_X64 "%~dpn0\%~n0.py" %*
  IF ERRORLEVEL 1 GOTO :ERROR
  ENDLOCAL
  EXIT /B 0

:ADDITIONAL_TESTS
SET REDIRECT_STDOUT_FILE_PATH=%TEMP%\zyp Test stdout %RANDOM%.txt
SET TEST_FILE_PATH=%TEMP%\zyp Test file %RANDOM%.txt
SET TEST_ZIP_FILE_PATH=%TEMP%\zyp Test file %RANDOM%.zip

ECHO   * Test version check...
CALL "%~dp0zyp.cmd" --version
IF ERRORLEVEL 1 GOTO :ERROR
CALL "%~dp0unzyp.cmd" --version
IF ERRORLEVEL 1 GOTO :ERROR

ECHO   * Test help...
CALL "%~dp0zyp.cmd" --help
IF ERRORLEVEL 1 GOTO :ERROR
CALL "%~dp0unzyp.cmd" --help
IF ERRORLEVEL 1 GOTO :ERROR

ECHO   * Zipping test file...
ECHO Hello, world! >"%TEST_FILE_PATH%"
IF ERRORLEVEL 1 GOTO :ERROR
CALL "%~dp0zyp.cmd" "%TEST_FILE_PATH%" "%TEST_ZIP_FILE_PATH%"
IF NOT %ERRORLEVEL% == 1 GOTO :ERROR
DEL "%TEST_FILE_PATH%" /Q

ECHO   * Listing zipped test file...
CALL "%~dp0unzyp.cmd" --list "%TEST_ZIP_FILE_PATH%"
IF ERRORLEVEL 1 GOTO :ERROR

ECHO   * Unzipping test file...
CALL "%~dp0unzyp.cmd" "%TEST_ZIP_FILE_PATH%" "%TEMP%"
IF NOT %ERRORLEVEL% == 1 GOTO :ERROR
IF NOT EXIST "%TEST_FILE_PATH%" (
  ECHO Unzipping did not re-create test file!
  DEL %TEST_ZIP_FILE_PATH% /Q
  ENDLOCAL
  EXIT /B 1
)
DEL "%TEST_FILE_PATH%" /Q
DEL "%TEST_ZIP_FILE_PATH%" /Q

ECHO + Done.
ENDLOCAL
EXIT /B 0

:ERROR
  ECHO     - Failed with error level %ERRORLEVEL%
  IF EXIST "%TEST_FILE_PATH%" DEL "%TEST_FILE_PATH%" /Q
  IF EXIST "%TEST_ZIP_FILE_PATH%" DEL "%TEST_ZIP_FILE_PATH%" /Q
  ENDLOCAL
  EXIT /B 1
