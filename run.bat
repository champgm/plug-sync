@echo off

pushd %~dp0
call ".\env\Scripts\activate.bat"
python ".\src\main.py"
popd
