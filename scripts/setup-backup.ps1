# setup-backup.ps1
# EXECUTAR UMA VEZ COMO ADMINISTRADOR
# Cria a tarefa agendada "Fenice_bRain_Backup" que roda às 22:30 todos os dias

$SCRIPT  = "C:\Fenice_bRain\scripts\backup-diario.ps1"
$USUARIO = $env:USERNAME

$action  = New-ScheduledTaskAction `
    -Execute "pwsh.exe" `
    -Argument "-NonInteractive -WindowStyle Hidden -ExecutionPolicy Bypass -File `"$SCRIPT`""

$trigger = New-ScheduledTaskTrigger -Daily -At "22:30"

$settings = New-ScheduledTaskSettingsSet `
    -ExecutionTimeLimit (New-TimeSpan -Minutes 30) `
    -StartWhenAvailable `
    -RunOnlyIfNetworkAvailable

$principal = New-ScheduledTaskPrincipal `
    -UserId "$env:COMPUTERNAME\$USUARIO" `
    -LogonType Interactive `
    -RunLevel Highest

Register-ScheduledTask `
    -TaskName    "Fenice_bRain_Backup" `
    -Description "Backup diário do vault Fenice bRain — GitHub + Google Drive (22:30)" `
    -Action      $action `
    -Trigger     $trigger `
    -Settings    $settings `
    -Principal   $principal `
    -Force

Write-Host ""
Write-Host "=== RESULTADO ===" -ForegroundColor Cyan
$task = Get-ScheduledTask -TaskName "Fenice_bRain_Backup" -ErrorAction SilentlyContinue
if ($task) {
    Write-Host "Tarefa criada com sucesso!" -ForegroundColor Green
    Write-Host "  Nome   : $($task.TaskName)"
    Write-Host "  Estado : $($task.State)"
    Write-Host "  Horário: 22:30 diariamente"
    Write-Host ""
    Write-Host "Para testar agora: Start-ScheduledTask -TaskName 'Fenice_bRain_Backup'"
    Write-Host "Log em: C:\Fenice_bRain\scripts\backup.log"
} else {
    Write-Host "FALHOU — execute como Administrador (clique direito → Executar como administrador)" -ForegroundColor Red
}
