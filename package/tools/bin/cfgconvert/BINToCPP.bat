:::::::::::::::::::::::::::::::::::::::::
::	file: BINToCPP.bat
::	======
::	Author: Bohemia Interactive
::	Description: Convert a Bin file to CPP (plain text)
::	Note: 
::	Wiki:
::		Go to http://community.bistudio.com/wiki/CfgConvert for more information
:::::::::::::::::::::::::::::::::::::::::
@pushd P:\
@"%~dp0CfgConvert.exe" -txt -dst "%~dpn1.cpp" %1
@if Errorlevel 1 pause
@popd