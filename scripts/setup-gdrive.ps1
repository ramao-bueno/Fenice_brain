# setup-gdrive.ps1
# EXECUTAR UMA VEZ — configura rclone com Google Drive (abre navegador para login)
# Após configurar, o backup-diario.ps1 sincroniza automaticamente via rclone

Write-Host ""
Write-Host "=== Configuração Google Drive (rclone) ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "Vai abrir o navegador para você fazer login no Google." -ForegroundColor Yellow
Write-Host "Escolha a conta oiconsulbrasil@gmail.com" -ForegroundColor Yellow
Write-Host ""

# Passo 1: cria o remote "gdrive" com config básica (sem OAuth ainda)
Write-Host "Criando remote 'gdrive'..." -ForegroundColor Cyan
rclone config create gdrive drive scope drive use_trash false

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Falha ao criar remote — verifique se o rclone está instalado corretamente." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "✅ Google Drive configurado como remote 'gdrive'" -ForegroundColor Green
Write-Host ""
Write-Host "Testando acesso..." -ForegroundColor Cyan
rclone lsd gdrive: --max-depth 1

Write-Host ""
Write-Host "Sincronizando Fenice_bRain agora (teste inicial)..." -ForegroundColor Cyan
rclone sync "C:\Fenice_bRain" "gdrive:Fenice_bRain" `
    --exclude ".git/**" `
    --exclude ".obsidian/cache/**" `
    --progress

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ Sync concluído! Próximo backup automático: hoje às 22:30" -ForegroundColor Green
} else {
    Write-Host "❌ Sync falhou — verifique a conexão e tente novamente." -ForegroundColor Red
}
