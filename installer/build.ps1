# Builds dist\GalacticMacro-Setup-<version>.exe. Needs the .NET 8 SDK and Inno Setup 6
# (winget install JRSoftware.InnoSetup). The version comes from <Version> in GalacticMacro.csproj.
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
$version = ([xml](Get-Content "$root\GalacticMacro.csproj")).Project.PropertyGroup.Version | Where-Object { $_ } | Select-Object -First 1

$out = "$root\publish-installer"
if (Test-Path $out) { Remove-Item $out -Recurse -Force }
dotnet publish "$root\GalacticMacro.csproj" -c Release -r win-x64 --self-contained -o $out
if ($LASTEXITCODE) { throw 'dotnet publish failed' }

$iscc = @("$env:LOCALAPPDATA\Programs\Inno Setup 6\ISCC.exe", "${env:ProgramFiles(x86)}\Inno Setup 6\ISCC.exe", "$env:ProgramFiles\Inno Setup 6\ISCC.exe") |
    Where-Object { Test-Path $_ } | Select-Object -First 1
if (-not $iscc) { throw 'Inno Setup 6 not found (winget install JRSoftware.InnoSetup)' }
& $iscc /Qp "/DAppVersion=$version" "$PSScriptRoot\GalacticMacro.iss"
if ($LASTEXITCODE) { throw 'ISCC failed' }
Get-Item "$root\dist\GalacticMacro-Setup-$version.exe"
