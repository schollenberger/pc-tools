@echo off
rem
rem start PhotoViewer for each file in parameter list
rem
rem Note: Path is hard coded !!
rem

for  %%i in (%*) do rundll32.exe "%ProgramFiles%\Windows Photo Viewer\PhotoViewer.dll", &"r:\iCloud Photos\Photos\%%i"

echo "That's all folks..."
