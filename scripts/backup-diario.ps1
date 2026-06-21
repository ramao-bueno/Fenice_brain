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
# Sincroniza dois vaults direto na raiz do Drive via rclone
$syncPairs = @(
    @{ Local = "C:\Fenice_bRain";    Remote = "gdrive:Fenice_bRain"   },
    @{ Local = "C:\Fenice_Estudos";  Remote = "gdrive:Fenice_Estudos" }
)

if (Get-Command rclone -ErrorAction SilentlyContinue) {
    foreach ($pair in $syncPairs) {
        if (-not (Test-Path $pair.Local)) {
            Log "GDrive: SKIP $($pair.Local) — pasta não encontrada"
            continue
        }
        $rcloneOut = rclone sync $pair.Local $pair.Remote `
            --exclude ".git/**" `
            --exclude ".obsidian/cache/**" `
            --exclude "*.tmp" `
            --stats-one-line --stats 0 2>&1
        if ($LASTEXITCODE -eq 0) {
            Log "GDrive: OK → $($pair.Remote)"
        } else {
            Log "GDrive: FALHOU → $($pair.Remote)"
            $rcloneOut | ForEach-Object { $s = "$_".Trim(); if ($s) { Log "GDrive:   $s" } }
        }
    }
} else {
    Log "GDrive: PENDENTE — rclone não encontrado"
    Log "GDrive:   → https://rclone.org/downloads/"
}

Log "BACKUP CONCLUÍDO"
Log "========================================="
