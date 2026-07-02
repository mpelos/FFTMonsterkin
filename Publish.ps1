<#
.SYNOPSIS
    Packages the Monsterkin (data-only) Reloaded-II mod for release.
.DESCRIPTION
    Monsterkin has no compiled DLL - it is a pure TableData/NXD mod. So unlike the standard
    Reloaded Publish.ps1 there is no `dotnet publish` step: we point the official
    Reloaded.Publisher tool straight at the mod folder (mod/ffttic.monsterkin) and let it
    produce a Generic package (the .zip plus ffttic.monsterkin.ReleaseMetadata.json) under
    Publish/ToUpload/Generic. That is the folder the GitHub workflow attaches to the Release.

    The Reloaded publishing tool is downloaded on demand from the official Reloaded-II
    Tools.zip if it is not already present.

.PARAMETER PackageName
    Reloaded package id / output base name. Defaults to the ModId in ModConfig.json.
.PARAMETER ModFolder
    Path to the mod folder that contains ModConfig.json.
.PARAMETER PublishOutputDir
    Root output directory. The Generic package lands in <PublishOutputDir>/Generic.
#>
param (
    $ModFolder = "mod/ffttic.monsterkin",
    $PackageName = "ffttic.monsterkin",
    $PublishOutputDir = "Publish/ToUpload",
    $ReadmePath = "README.md"
)

$ErrorActionPreference = 'Stop'

# Run relative to this script regardless of caller CWD.
Split-Path $MyInvocation.MyCommand.Path | Push-Location
[Environment]::CurrentDirectory = $PWD

try {
    $reloadedToolsPath = "./Publish/Tools/Reloaded-Tools"
    $reloadedToolPath  = "$reloadedToolsPath/Reloaded.Publisher.exe"
    $genericDir        = "$PublishOutputDir/Generic"
    $tempDir           = [System.IO.Path]::GetTempPath() + [System.IO.Path]::GetRandomFileName()

    if (-not (Test-Path (Join-Path $ModFolder 'ModConfig.json'))) {
        throw "ModConfig.json not found under '$ModFolder'"
    }

    # Fetch the Reloaded publishing tool if we don't have it yet.
    if (-not (Test-Path -Path $reloadedToolPath)) {
        Write-Host "Downloading Reloaded Tools..."
        New-Item $tempDir -ItemType Directory -Force | Out-Null
        $ProgressPreference = 'SilentlyContinue'
        Invoke-WebRequest -Uri "https://github.com/Reloaded-Project/Reloaded-II/releases/latest/download/Tools.zip" -OutFile "$tempDir/Tools.zip"
        Expand-Archive -LiteralPath "$tempDir/Tools.zip" -DestinationPath $reloadedToolsPath -Force
        Remove-Item $tempDir -Recurse -ErrorAction SilentlyContinue
    }

    # Clean previous output.
    Remove-Item $PublishOutputDir -Recurse -ErrorAction SilentlyContinue
    New-Item $genericDir -ItemType Directory -Force | Out-Null

    $readmeFullPath = $null
    if ($ReadmePath -and (Test-Path $ReadmePath)) {
        $readmeFullPath = [System.IO.Path]::GetFullPath($ReadmePath)
    }

    $arguments = "--modfolder `"$ModFolder`" --packagename `"$PackageName`" --outputfolder `"$genericDir`" --publishtarget Default"
    if ($readmeFullPath) { $arguments += " --readmepath `"$readmeFullPath`"" }

    $command = "$reloadedToolPath $arguments"
    Write-Host "$command`r`n"
    Invoke-Expression $command

    Write-Host "`nDone. Package(s) in '$genericDir':"
    Get-ChildItem $genericDir | ForEach-Object { Write-Host "  $($_.Name)" }
}
finally {
    Pop-Location
}
