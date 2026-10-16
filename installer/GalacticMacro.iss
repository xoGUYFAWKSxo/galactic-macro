; Inno Setup script for Galactic Macro. Build with installer\build.ps1, which publishes the app
; self-contained (no .NET runtime needed on the target PC) and passes the version in.

#define AppName "Galactic Macro"
#define AppExe "GalacticMacro.exe"
#ifndef AppVersion
  #define AppVersion "0.0.0"
#endif

[Setup]
AppId={{C9C30B49-D14E-46F9-8E0F-455CC26BED8C}
AppName={#AppName}
AppVersion={#AppVersion}
AppVerName={#AppName} {#AppVersion}
AppPublisher=xoGUYFAWKSxo
AppPublisherURL=https://github.com/xoGUYFAWKSxo/galactic-macro
AppSupportURL=https://github.com/xoGUYFAWKSxo/galactic-macro/issues
AppUpdatesURL=https://github.com/xoGUYFAWKSxo/galactic-macro/releases
VersionInfoVersion={#AppVersion}
DefaultDirName={autopf}\{#AppName}
DisableProgramGroupPage=yes
; Installs for the current user without admin rights; the user can pick "all users" instead.
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
MinVersion=10.0
DisableWelcomePage=no
OutputDir=..\dist
OutputBaseFilename=GalacticMacro-Setup-{#AppVersion}
SetupIconFile=..\assets\icon.ico
UninstallDisplayIcon={app}\{#AppExe}
UninstallDisplayName={#AppName}
WizardStyle=modern
WizardImageFile=..\assets\wizard-large-100.bmp,..\assets\wizard-large-200.bmp
WizardSmallImageFile=..\assets\wizard-small-100.bmp,..\assets\wizard-small-200.bmp
Compression=lzma2/ultra64
SolidCompression=yes
CloseApplications=yes

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"

[Files]
Source: "..\publish-installer\*"; DestDir: "{app}"; Excludes: "*.pdb"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{autoprograms}\{#AppName}"; Filename: "{app}\{#AppExe}"; IconFilename: "{app}\{#AppExe}"
Name: "{autodesktop}\{#AppName}"; Filename: "{app}\{#AppExe}"; IconFilename: "{app}\{#AppExe}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#AppExe}"; Description: "{cm:LaunchProgram,{#AppName}}"; Flags: nowait postinstall skipifsilent
