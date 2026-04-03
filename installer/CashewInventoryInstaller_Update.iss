[Setup]
AppId=dd63fbbb-d349-4ad0-8870-5201c651fea2
AppName=Cashew Inventory Management (Update)
AppVersion=1.0.1
VersionInfoVersion=1.0.1.0
DefaultDirName={autopf}\CashewInventory
OutputDir=.\Output
OutputBaseFilename=CashewInventoryUpdate
Compression=lzma2
SolidCompression=yes
ArchitecturesInstallIn64BitMode=x64
PrivilegesRequired=admin

[Files]
Source: "..\backend\*"; DestDir: "{app}\backend"; Excludes: "venv,__pycache__,.git,dist,build,*.log,node_modules"; Flags: ignoreversion recursesubdirs
Source: "..\frontend\dist\*"; DestDir: "{app}\frontend\dist"; Flags: ignoreversion recursesubdirs
Source: "launcher\backup.bat"; DestDir: "{app}\bin"; Flags: ignoreversion
Source: "launcher\restore.bat"; DestDir: "{app}\bin"; Flags: ignoreversion
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

function InitializeSetup(): Boolean;
var
  InstalledVersion: String;
begin
  InstalledVersion := GetInstalledVersion();

  if InstalledVersion = '' then
  begin
    MsgBox('No existing installation found. Please use the full installer first.', mbError, MB_OK);
    Result := False;
    exit;
  end;

  if CompareStr(InstalledVersion, '{#SetupSetting("AppVersion")}') >= 0 then
  begin
    MsgBox('Same or newer version already installed (' + InstalledVersion + ').', mbInformation, MB_OK);
    Result := False;
    exit;
  end;

  Result := True;
end;

procedure CurStepChanged(CurStep: TSetupStep);
var
  ExecResult: Integer;
  BackupDir: String;
begin
  BackupDir := ExpandConstant('{commonappdata}\CashewInventory\backup');

  if CurStep = ssInstall then
  begin
    Exec(
      ExpandConstant('{app}\bin\backup.bat'),
      ExpandConstant('{app} "' + BackupDir + '"'),
      '',
      SW_HIDE,
      ewWaitUntilTerminated,
      ExecResult
    );
  end;

  if CurStep = ssPostInstall then
  begin
    Exec(
      ExpandConstant('{app}\bin\setup_environment.bat'),
      ExpandConstant('{app} "{commonappdata}\CashewInventory\logs"'),
      '',
      SW_HIDE,
      ewWaitUntilTerminated,
      ExecResult
    );

    if ExecResult <> 0 then
    begin
      MsgBox('Update failed. Restoring previous version...', mbError, MB_OK);

      Exec(
        ExpandConstant('{app}\bin\restore.bat'),
        ExpandConstant('{app} "' + BackupDir + '"'),
        '',
        SW_HIDE,
        ewWaitUntilTerminated,
        ExecResult
      );

      MsgBox('Rollback completed. Previous version restored.', mbInformation, MB_OK);
    end
    else
    begin
      MsgBox('Update completed successfully!', mbInformation, MB_OK);
    end;
  end;
end;