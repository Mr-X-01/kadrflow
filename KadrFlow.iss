#ifndef AppVersion
  #define AppVersion "0.1.0"
#endif

[Setup]
AppId={{A3C28D27-2765-4C35-892E-44EF915B1A21}
AppName=KadrFlow
AppVersion={#AppVersion}
AppPublisher=Mr-X-01
AppPublisherURL=https://github.com/Mr-X-01/kadrflow
AppSupportURL=https://github.com/Mr-X-01/kadrflow/issues
AppUpdatesURL=https://github.com/Mr-X-01/kadrflow/releases
SetupArchitecture=x64
ArchitecturesAllowed=x64compatible
PrivilegesRequired=lowest
DefaultDirName={localappdata}\Programs\KadrFlow
DefaultGroupName=KadrFlow
DisableProgramGroupPage=yes
UninstallDisplayIcon={app}\KadrFlow.exe
OutputDir=release
OutputBaseFilename=KadrFlow-{#AppVersion}-Setup-windows-x64
SetupIconFile=assets\KadrFlow.ico
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
CloseApplications=yes

[Files]
Source: "dist\KadrFlow\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: ".venv\tools\MicrosoftEdgeWebview2Setup.exe"; DestDir: "{tmp}"; Flags: deleteafterinstall

[Icons]
Name: "{autoprograms}\KadrFlow"; Filename: "{app}\KadrFlow.exe"; WorkingDir: "{app}"
Name: "{autodesktop}\KadrFlow"; Filename: "{app}\KadrFlow.exe"; WorkingDir: "{app}"

[Run]
Filename: "{tmp}\MicrosoftEdgeWebview2Setup.exe"; Parameters: "/silent /install"; StatusMsg: "Установка Microsoft WebView2..."; Flags: waituntilterminated; Check: WebView2Missing
Filename: "{app}\KadrFlow.exe"; Description: "Запустить KadrFlow"; Flags: nowait postinstall skipifsilent

[Code]
function WebView2Missing: Boolean;
var
  Version: String;
begin
  Result := True;
  if RegQueryStringValue(HKLM, 'SOFTWARE\WOW6432Node\Microsoft\EdgeUpdate\Clients\{F3017226-FE2A-4295-8BDF-00C3A9A7E4C5}', 'pv', Version) and
     (Version <> '') and (Version <> '0.0.0.0') then
    Result := False;
  if RegQueryStringValue(HKLM, 'SOFTWARE\Microsoft\EdgeUpdate\Clients\{F3017226-FE2A-4295-8BDF-00C3A9A7E4C5}', 'pv', Version) and
     (Version <> '') and (Version <> '0.0.0.0') then
    Result := False;
  if RegQueryStringValue(HKCU, 'Software\Microsoft\EdgeUpdate\Clients\{F3017226-FE2A-4295-8BDF-00C3A9A7E4C5}', 'pv', Version) and
     (Version <> '') and (Version <> '0.0.0.0') then
    Result := False;
end;
