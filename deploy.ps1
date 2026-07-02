# Deploy do mod "Beast Tamer" para o Reloaded-II.
# Copia D:\Projects\FFTIVC-BeastTamer\mod\fftivc.beasttamer -> C:\Reloaded-II\Mods\fftivc.beasttamer

$ErrorActionPreference = 'Stop'

$modId = 'fftivc.monsterkin'
$src   = Join-Path $PSScriptRoot "mod\$modId"
$dst   = "C:\Reloaded-II\Mods\$modId"

Write-Host ""
Write-Host "==== Deploy Monsterkin ====" -ForegroundColor Cyan
Write-Host "  origem : $src"
Write-Host "  destino: $dst"

if (-not (Test-Path $src)) { Write-Host "ERRO: pasta de origem nao encontrada: $src" -ForegroundColor Red; exit 1 }

$cfgPath = Join-Path $src 'ModConfig.json'
if (Test-Path $cfgPath) {
    $cfg = Get-Content $cfgPath -Raw | ConvertFrom-Json
    Write-Host ("  mod    : {0}  v{1}" -f $cfg.ModName, $cfg.ModVersion) -ForegroundColor Gray
}

New-Item -ItemType Directory -Force -Path $dst | Out-Null

$files = Get-ChildItem -Recurse -File -LiteralPath $src | Where-Object { $_.Name -ne '.gitkeep' }
$copied = 0
foreach ($f in $files) {
    $rel    = $f.FullName.Substring($src.Length).TrimStart('\')
    $target = Join-Path $dst $rel
    New-Item -ItemType Directory -Force -Path (Split-Path $target) | Out-Null
    Copy-Item -LiteralPath $f.FullName -Destination $target -Force
    $copied++
}
Write-Host ("  copiados: {0} arquivo(s)" -f $copied) -ForegroundColor Gray

$ok = $true
foreach ($f in $files) {
    $rel    = $f.FullName.Substring($src.Length).TrimStart('\')
    $target = Join-Path $dst $rel
    $h1 = (Get-FileHash -LiteralPath $f.FullName).Hash
    $h2 = (Get-FileHash -LiteralPath $target).Hash
    if ($h1 -ne $h2) { $ok = $false; Write-Host "  HASH DIFERENTE: $rel" -ForegroundColor Red }
}
if ($ok) { Write-Host "  verificacao por hash: OK" -ForegroundColor Green } else { exit 1 }
Write-Host ""
Write-Host "Pronto. Habilite 'Monsterkin' no Reloaded-II e lance o jogo pela GUI." -ForegroundColor Yellow
