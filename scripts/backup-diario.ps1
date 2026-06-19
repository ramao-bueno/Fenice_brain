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
    robocopy $VAULT $gdDest /MIR /XD ".git" ".obsidian\cache" /XF "*.tmp" "*.log" /NFL /NDL /NJH /NJS /NC /NS 2>&1 | Out-Null
    if ($LASTEXITCODE -le 7) {   # robocopy: 0-7 = sucesso
        Log "GDrive: sync OK → $gdDest"
    } else {
        Log "GDrive: robocopy FALHOU (código $LASTEXITCODE)"
    }
} elseif (Get-Command rclone -ErrorAction SilentlyContinue) {
    # Opção B: rclone configurado (rclone config → remote "gdrive")
    rclone sync $VAULT "gdrive:Fenice_bRain" --exclude ".git/**" --exclude ".obsidian/cache/**" 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) { Log "GDrive: rclone sync OK" }
    else { Log "GDrive: rclone FALHOU" }
} else {
    Log "GDrive: PENDENTE — instalar Google Drive for Desktop OU rclone"
    Log "GDrive:   → https://www.google.com/drive/download/"
    Log "GDrive:   → https://rclone.org/downloads/"
}

Log "BACKUP CONCLUÍDO"
Log "========================================="
