# backup-diario.ps1
# Backup diário às 22:30 — git push + Google Drive sync
# Tarefa agendada: "Fenice_bRain_Backup" (criada por setup-backup.ps1)

$VAULT  = "C:\Fenice_bRain"
$LOG    = "$VAULT\scripts\backup.log"
$DATA   = Get-Date -Format "yyyy-MM-dd HH:mm"
$BRANCH = "main"
$REMOTE = "github"

function Log($msg) {
    $linha = "$DATA | $msg"
    $linha | Add-Content -Path $LOG -Encoding UTF8
    Write-Output $linha
}

Set-Location $VAULT
Log "========================================="
Log "BACKUP INICIADO"

# ── GIT ───────────────────────────────────────────────────────
$alteracoes = git status --porcelain 2>&1
if ($alteracoes) {
    git add -u 2>&1 | Out-Null
    $commitMsg = "backup: $DATA"
    git commit -m $commitMsg 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) { Log "Git: commit OK — $commitMsg" }
    else { Log "Git: commit FALHOU" }
} else {
    Log "Git: sem alterações para commitar"
}

$push = git push $REMOTE $BRANCH 2>&1
if ($LASTEXITCODE -eq 0) {
    Log "Git: push OK → $REMOTE/$BRANCH (github.com/ramao-bueno/Fenice_brain)"
} else {
    Log "Git: push FALHOU — $push"
}

# ── GOOGLE DRIVE ──────────────────────────────────────────────
# Opção A: Google Drive for Desktop (pasta "My Drive" local)
$gdLocalPaths = @(
    "$env:USERPROFILE\My Drive",
    "$env:USERPROFILE\Google Drive\My Drive",
    "G:\My Drive"
)
$gdDest = $null
foreach ($p in $gdLocalPaths) {
    if (Test-Path $p) { $gdDest = "$p\Fenice_bRain"; break }
}

if ($gdDest) {
    # /NFL /NDL = sem lista de arquivos/dirs individuais; sem /NJH /NJS para manter resumo
    $roboOut = robocopy $VAULT $gdDest /MIR /XD ".git" ".obsidian\cache" /XF "*.tmp" "*.log" /NFL /NDL /NC 2>&1
    if ($LASTEXITCODE -le 7) {
        Log "GDrive: sync OK → $gdDest"
        $roboOut | ForEach-Object { $s = "$_".Trim(); if ($s) { Log "GDrive:   $s" } }
    } else {
        Log "GDrive: robocopy FALHOU (código $LASTEXITCODE)"
        $roboOut | ForEach-Object { $s = "$_".Trim(); if ($s) { Log "GDrive:   $s" } }
    }
} elseif (Get-Command rclone -ErrorAction SilentlyContinue) {
    # Opção B: rclone configurado (rclone config → remote "gdrive")
    $rcloneOut = rclone sync $VAULT "gdrive:Fenice_bRain" --exclude ".git/**" --exclude ".obsidian/cache/**" --stats-one-line --stats 0 2>&1
    if ($LASTEXITCODE -eq 0) {
        Log "GDrive: rclone sync OK"
        $rcloneOut | ForEach-Object { $s = "$_".Trim(); if ($s) { Log "GDrive:   $s" } }
    } else {
        Log "GDrive: rclone FALHOU"
        $rcloneOut | ForEach-Object { $s = "$_".Trim(); if ($s) { Log "GDrive:   $s" } }
    }
} else {
    Log "GDrive: PENDENTE — instalar Google Drive for Desktop OU rclone"
    Log "GDrive:   → https://www.google.com/drive/download/"
    Log "GDrive:   → https://rclone.org/downloads/"
}

Log "BACKUP CONCLUÍDO"
Log "========================================="
