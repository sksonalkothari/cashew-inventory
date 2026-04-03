[Setup]
AppId=dd63fbbb-d349-4ad0-8870-5201c651fea2
AppName=Cashew Inventory Management
AppVersion=1.0.0
VersionInfoVersion=1.0.0.0
DefaultDirName={autopf}\CashewInventory
DefaultGroupName=Cashew Inventory
OutputDir=.\Output
OutputBaseFilename=CashewInventoryFull
Compression=lzma2
SolidCompression=yes
ArchitecturesInstallIn64BitMode=x64
PrivilegesRequired=admin

[Files]
Source: "..\backend\*"; DestDir: "{app}\backend"; Excludes: "venv,__pycache__,.git,dist,build,*.log,node_modules"; Flags: ignoreversion recursesubdirs
Source: "..\frontend\dist\*"; DestDir: "{app}\frontend\dist"; Flags: ignoreversion recursesubdirs
Source: "runtimes\python-3.11.5-embed-amd64\*"; DestDir: "{app}\python"; Flags: ignoreversion recursesubdirs
Source: "launcher\*"; DestDir: "{app}\bin"; Flags: ignoreversion recursesubdirs

[Dirs]
Name: "{commonappdata}\CashewInventory\logs"

[Code]

function GetInstalledVersion(): String;
begin
  if RegQueryStringValue(HKLM, 'Software\Microsoft\Windows\CurrentVersion\Uninstall\{#SetupSetting("AppId")}_is1', 'DisplayVersion', Result) then
  begin
  end
  else
    Result := '';
end;

function IsUpgradeAllowed(): Boolean;
var
  InstalledVersion: String;
begin
  InstalledVersion := GetInstalledVersion();

  if InstalledVersion <> '' then
  begin
    if CompareStr(InstalledVersion, '{#SetupSetting("AppVersion")}') > 0 then
    begin
      MsgBox('A newer version (' + InstalledVersion + ') is already installed.', mbError, MB_OK);
      Result := False;
      exit;
    end;
  end;

  Result := True;
end;

function InitializeSetup(): Boolean;
begin
  Result := IsUpgradeAllowed();
end;

procedure CurStepChanged(CurStep: TSetupStep);
var
  ExecResult: Integer;
begin
  if CurStep = ssPostInstall then
  begin
    ShellExec('', 
      ExpandConstant('{app}\bin\setup_environment.bat'), 
      ExpandConstant('{app} "{commonappdata}\CashewInventory\logs"'), 
      '', 
      SW_HIDE, 
      ewWaitUntilTerminated, 
      ExecResult);
  end;
end;