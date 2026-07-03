@echo off
setlocal ENABLEDELAYEDEXPANSION

if "%~1"=="" (
  echo Usage: publish-framework.bat ^<SourcePath^> [DestinationPath] [--force]
  exit /b 64
)

set "SOURCE=%~1"
set "DEST=%~2"
set "FORCE=%~3"
if "%DEST%"=="" set "DEST=c:\mayank\Software\VSCode_Isolated\data\user-data\User\prompts\saarthi-framework"
if /I "%~2"=="--force" (
  set "FORCE=--force"
  set "DEST=c:\mayank\Software\VSCode_Isolated\data\user-data\User\prompts\saarthi-framework"
)

if not exist "%SOURCE%" (
  echo Source path not found: %SOURCE%
  exit /b 1
)

for %%I in ("%SOURCE%") do set "SRCFULL=%%~fI"
for %%I in ("%DEST%") do set "DESTFULL=%%~fI"
if /I "%SRCFULL%"=="%DESTFULL%" (
  echo Source and destination are the same path.
  exit /b 1
)

set /a SIG=0
set /a FOUND=0
for %%R in ("framework.config.yaml" "manifest.json" "AGENTS.md" "_framework" "templates" "tools") do (
  set /a SIG+=1
  if exist "%SOURCE%\%%~R" set /a FOUND+=1
)

set /a PCT=(FOUND*100)/SIG
if %PCT% LSS 50 if /I not "%FORCE%"=="--force" (
  echo Guardrail: source path looks very different from expected framework structure.
  echo Source: %SOURCE%
  echo Similarity score: %PCT%%% (threshold: 50%%)
  set /p CONFIRM=Proceed anyway? Type YES to continue: 
  if /I not "!CONFIRM!"=="YES" (
    echo Publish cancelled by guardrail.
    exit /b 1
  )
)

if not exist "%DEST%" mkdir "%DEST%"
for /f "delims=" %%D in ('dir /b /a "%DEST%"') do rmdir /s /q "%DEST%\%%D" 2>nul & del /f /q "%DEST%\%%D" 2>nul
xcopy "%SOURCE%\*" "%DEST%\" /E /I /Y >nul

set "MISSING="
if not exist "%DEST%\framework.config.yaml" set "MISSING=1"
if not exist "%DEST%\_framework\INDEX.md" set "MISSING=1"
if not exist "%DEST%\tools\validate-work-item.js" set "MISSING=1"

if defined MISSING (
  echo Publish completed, but required files are missing.
  exit /b 2
)

echo Publish successful.
echo Source:      %SOURCE%
echo Destination: %DEST%
echo Validator:   node "%DEST%\tools\validate-work-item.js" ^<WORK_ITEM_ID^> --root "%DEST%"
if /I "%FORCE%"=="--force" echo Guardrail override was used (--force).

echo Running post-publish smoke test...
if exist "%DEST%\tools\smoke-test-framework.js" (
  node "%DEST%\tools\smoke-test-framework.js" --root "%DEST%"
  if errorlevel 1 (
    echo Publish completed but smoke test failed.
    exit /b 3
  )
) else (
  echo Smoke-test helper not found after publish; running fallback smoke check.
  node "%DEST%\tools\validate-work-item.js" --help >nul
  if errorlevel 1 (
    echo Publish completed but fallback smoke test failed.
    exit /b 3
  )
)

echo Post-publish smoke test passed.
exit /b 0
