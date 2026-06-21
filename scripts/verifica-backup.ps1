# verifica-backup.ps1
# Exibe status do último backup — roda via hook Claude Code (uma vez por dia)

$LOG   = "C:\Fenice_bRain\scripts\backup.log"
$STAMP = "C:\Fenice_bRain\scripts\.ultimo-status-check"
$HOJE  = Get-Date -Format "yyyy-MM-dd"

# Silencia se já exibiu hoje
if ((Test-Path $STAMP) -and ((Get-Content $STAMP -Raw).Trim() -eq $HOJE)) { exit 0 }
$HOJE | Set-Content $STAMP -Encoding UTF8

if (-not (Test-Path $LOG)) {
    Write-Output "BACKUP_STATUS: 🔴 Nenhum backup encontrado — execute o backup antes de continuar!"
    exit 0
}

# Agrupa o log em blocos por execução de backup
$linhas  = Get-Content $LOG -Encoding UTF8
$blocos  = [System.Collections.Generic.List[object]]::new()
$bloco   = [System.Collections.Generic.List[string]]::new()

foreach ($l in $linhas) {
    $bloco.Add($l)
    if ($l -match "BACKUP CONCLUÍDO") {
        $blocos.Add($bloco.ToArray())
        $bloco = [System.Collections.Generic.List[string]]::new()
    }
}

if ($blocos.Count -eq 0) {
    Write-Output "BACKUP_STATUS: 🔴 Backup incompleto — execute o backup manualmente!"
    exit 0
}

$ultimo = $blocos[$blocos.Count - 1]

# Data do último backup
$dataBackup = $null
foreach ($l in $ultimo) {
    if ($l -match "^(\d{4}-\d{2}-\d{2} \d{2}:\d{2})") {
        $dataBackup = $Matches[1]
        break
    }
}

$gitOK          = $ultimo | Where-Object { $_ -match "Git: (commit OK|sem alterações)" }
$pushOK         = $ultimo | Where-Object { $_ -match "Git: push OK" }
$gdriveOK       = $ultimo | Where-Object { $_ -match "GDrive: OK →" }
$gdrivePendente = $ultimo | Where-Object { $_ -match "GDrive: PENDENTE" }
# Conta quantos syncs OK (esperamos 2: Fenice_bRain + Fenice_Estudos)
$gdriveTodos    = (@($gdriveOK)).Count -ge 2

# Verifica se o backup é recente (≤ 26h para cobrir horários alternados)
$recente = $false
if ($dataBackup) {
    try {
        $dt   = [DateTime]::ParseExact($dataBackup, "yyyy-MM-dd HH:mm", $null)
        $diff = (Get-Date) - $dt
        $recente = $diff.TotalHours -le 26
    } catch {}
}

if ($recente -and $gitOK -and $pushOK) {
    if ($gdriveTodos) {
        Write-Output "BACKUP_STATUS: ✅ Seus arquivos estão bem guardados — último backup: $dataBackup (Git ✓  GDrive ✓ x2)"
    } elseif ($gdriveOK) {
        Write-Output "BACKUP_STATUS: ✅ Git OK ($dataBackup) | ⚠️  GDrive parcial — apenas $(@($gdriveOK).Count)/2 vault(s) sincronizados"
    } elseif ($gdrivePendente) {
        Write-Output "BACKUP_STATUS: ✅ Git OK ($dataBackup) | ⚠️  GDrive pendente — rode setup-gdrive.ps1"
    } else {
        Write-Output "BACKUP_STATUS: ⚠️  Git OK ($dataBackup) | GDrive com problema — verifique o log"
    }
} else {
    $motivo = @()
    if (-not $recente)  { $motivo += "último backup em $dataBackup (há mais de 26h)" }
    if (-not $gitOK)    { $motivo += "Git commit falhou" }
    if (-not $pushOK)   { $motivo += "Git push falhou" }
    Write-Output "BACKUP_STATUS: 🔴 FAÇA UM BACKUP AGORA — $($motivo -join ' | ')"
}
