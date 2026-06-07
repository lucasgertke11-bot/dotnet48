; .NET Framework 4.8 Portable Installer for Wine/Proton prefixes
; Extracts to $WINDIR (C:\windows)
; Compile: wine makensis.exe install.nsi

Unicode true
SetCompressor /SOLID lzma
Name ".NET Framework 4.8 Portable"
OutFile "install-dotnet48.exe"
RequestExecutionLevel admin
ShowInstDetails show

!include LogicLib.nsh

Section "-PreInstall"
  DetailPrint "Removing blocking registry keys (GE-Proton workaround)..."
  ExecWait '"$WINDIR\regedit.exe" /S /D "HKLM\Software\Wow6432Node\Microsoft\NET Framework Setup\NDP\v4"' $0
  ExecWait '"$WINDIR\regedit.exe" /S /D "HKLM\Software\Wow6432Node\Microsoft\.NETFramework"' $0
  ExecWait '"$WINDIR\regedit.exe" /S /D "HKLM\Software\Microsoft\NET Framework Setup\NDP\v4"' $0

  ; Remove existing mscoree.dll symlinks (Proton)
  DetailPrint "Removing existing mscoree.dll..."
  Delete "$WINDIR\system32\mscoree.dll"
  Delete "$WINDIR\syswow64\mscoree.dll"
SectionEnd

Section "Extract .NET Framework 4.8"
  SetOutPath "$TEMP\dotnet48-installer"
  
  DetailPrint "Extracting tools..."
  File "7za.exe"
  File "dotnet48-package.7z"
  File "dotnet48-full.reg"
  
  ; Extract directly to Windows directory
  DetailPrint "Extracting to: $WINDIR"
  
  ExecWait '"$TEMP\dotnet48-installer\7za.exe" x "$TEMP\dotnet48-installer\dotnet48-package.7z" -o"$WINDIR" -y' $0
  
  ${If} $0 != 0
    DetailPrint "ERROR: Extraction failed with code $0"
    MessageBox MB_ICONSTOP "Failed to extract. Error code: $0"
    Abort
  ${EndIf}
  
  DetailPrint "Extraction complete!"
SectionEnd

Section "Import Registry"
  DetailPrint "Importing registry..."
  ExecWait '"$WINDIR\regedit.exe" /S "$TEMP\dotnet48-installer\dotnet48-full.reg"' $0
  
  ${If} $0 != 0
    DetailPrint "WARNING: regedit returned code $0"
  ${Else}
    DetailPrint "Registry imported!"
  ${EndIf}
SectionEnd

Section "-PostInstall"
  DetailPrint ""
  DetailPrint "========================================"
  DetailPrint ".NET Framework 4.8 installation complete!"
  DetailPrint "========================================"
  DetailPrint "Target: $WINDIR"
  DetailPrint ""
  DetailPrint "Se mscoree.dll nao foi copiado (Proton read-only):"
  DetailPrint "  cp -RLv mscoree.dll \$WINEPREFIX/drive_c/windows/system32/"
  DetailPrint "  cp -RLv mscoree.dll \$WINEPREFIX/drive_c/windows/syswow64/"
  DetailPrint ""
  MessageBox MB_OK ".NET Framework 4.8 installed!"
SectionEnd
