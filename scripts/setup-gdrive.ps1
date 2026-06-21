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
Write-Host "Sincronizando vaults para a raiz do Google Drive..." -ForegroundColor Cyan

$syncPairs = @(
    @{ Local = "C:\Fenice_bRain";    Remote = "gdrive:Fenice_bRain"   },
    @{ Local = "C:\Fenice_Estudos";  Remote = "gdrive:Fenice_Estudos" }
)

$erros = 0
foreach ($pair in $syncPairs) {
    if (-not (Test-Path $pair.Local)) {
        Write-Host "⚠️  Pasta não encontrada: $($pair.Local) — pulando" -ForegroundColor Yellow
        continue
    }
    Write-Host ""
    Write-Host "  $($pair.Local) → $($pair.Remote)" -ForegroundColor White
    rclone sync $pair.Local $pair.Remote `
        --exclude ".git/**" `
        --exclude ".obsidian/cache/**" `
        --exclude "*.tmp" `
        --progress
    if ($LASTEXITCODE -ne 0) { $erros++ }
}

Write-Host ""
if ($erros -eq 0) {
    Write-Host "✅ Sync concluído! Próximo backup automático: hoje às 22:30" -ForegroundColor Green
} else {
    Write-Host "❌ $erros sync(s) falharam — verifique a conexão e tente novamente." -ForegroundColor Red
}
