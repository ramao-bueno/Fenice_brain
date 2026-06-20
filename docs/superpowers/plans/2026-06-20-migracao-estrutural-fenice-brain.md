# Migração Estrutural Fenice_bRain — Plano A

> **Para agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) ou superpowers:executing-plans para implementar este plano tarefa a tarefa. Steps usam sintaxe checkbox (`- [ ]`) para rastreamento.

**Goal:** Reorganizar os 23.826 arquivos de `C:\Fenice_bRain` da estrutura atual com 3 cópias redundantes para a estrutura canônica kelseniana em 10 módulos numerados, eliminando ~18k arquivos duplicados e preparando o vault para o Plugin v22.

**Architecture:** Fonte canônica é `Fenice bRain/` (subfolder, 13.645 arquivos). Pastas `⚖️` da raiz e `02 - Áreas/` são subconjuntos — exclusivos são mesclados, resto eliminado. Cada fase é atômica: falhou → git restore → repetir.

**Tech Stack:** PowerShell 7+, Git, Obsidian 1.x (fechado durante toda a migração)

## Global Constraints

- **Obsidian deve estar fechado** durante todas as Tarefas 1–7. Abrir só na Tarefa 8.
- **Nunca usar `rm -rf` direto** — sempre verificar contagem antes de deletar.
- **Commit ao fim de cada tarefa** — cada tarefa é um ponto de restauração.
- **Base:** `$base = "C:\Fenice_bRain"` em todos os scripts.
- **Git:** usar `git add -u && git add .` após moves (não `git mv` — impraticável com 23k arquivos).
- **Wikilinks:** Obsidian resolve por nome de arquivo, não path — nomes únicos sobrevivem à migração.
- **Plano B** (Plugin v22 — DomainModal + JurisconsultoModal + FilosofoModal) depende deste plano e será executado em sessão separada após Task 8 passar.

---

### Task 1: Criar Estrutura de Pastas Nova

**Files:**
- Create: `C:\Fenice_bRain\00_APEX\`
- Create: `C:\Fenice_bRain\01_PRIVADO\{Codigos\CC,Codigos\CPC,Codigos\CDC,Jurisprudencia,Doutrina,Revisao}\`
- Create: `C:\Fenice_bRain\02_PENAL\{Codigos\CP\DEL2848,Codigos\CP\Crimes,Codigos\CPP,Codigos\Especial,Jurisprudencia,Doutrina,Revisao}\`
- Create: `C:\Fenice_bRain\03_PUBLICO\{Codigos\Admin,Codigos\Tributario,Codigos\Previdenciario,Codigos\Ambiental,Jurisprudencia,Doutrina,Revisao}\`
- Create: `C:\Fenice_bRain\04_TRABALHO\{Codigos\CLT,Codigos\ProcessualTrabalhista,Jurisprudencia,Doutrina,Revisao}\`
- Create: `C:\Fenice_bRain\05_ESPECIAL\{Codigos\ECA,Codigos\LGPD,Codigos\MariadaPenha,Codigos\StatutoIdoso,Jurisprudencia,Revisao}\`
- Create: `C:\Fenice_bRain\06_JURISCONSULTOS\{PRIVADO,PENAL,PUBLICO,TRABALHO,METODOLOGIA}\`
- Create: `C:\Fenice_bRain\07_FILOSOFIA\{Antigos,Iluministas,Modernos,Contemporaneos,Penalistas}\`
- Create: `C:\Fenice_bRain\08_ENSINO\Univille\`
- Create: `C:\Fenice_bRain\09_FENICE_BRAIN\{Metodologia,Templates,Sistema}\`
- Create: `C:\Fenice_bRain\_SISTEMA\{Templates,OAB,Projetos,Arquivo,LeisComplementares}\`

**Interfaces:**
- Produces: estrutura de pastas vazia pronta para receber arquivos nas Tasks 2–5

- [ ] **Step 1: Executar script de criação**

```powershell
$base = "C:\Fenice_bRain"
$dirs = @(
  "00_APEX",
  "01_PRIVADO\Codigos\CC", "01_PRIVADO\Codigos\CPC", "01_PRIVADO\Codigos\CDC",
  "01_PRIVADO\Jurisprudencia", "01_PRIVADO\Doutrina", "01_PRIVADO\Revisao",
  "02_PENAL\Codigos\CP\DEL2848", "02_PENAL\Codigos\CP\Crimes",
  "02_PENAL\Codigos\CPP", "02_PENAL\Codigos\Especial",
  "02_PENAL\Jurisprudencia", "02_PENAL\Doutrina", "02_PENAL\Revisao",
  "03_PUBLICO\Codigos\Admin", "03_PUBLICO\Codigos\Tributario",
  "03_PUBLICO\Codigos\Previdenciario", "03_PUBLICO\Codigos\Ambiental",
  "03_PUBLICO\Jurisprudencia", "03_PUBLICO\Doutrina", "03_PUBLICO\Revisao",
  "04_TRABALHO\Codigos\CLT", "04_TRABALHO\Codigos\ProcessualTrabalhista",
  "04_TRABALHO\Jurisprudencia", "04_TRABALHO\Doutrina", "04_TRABALHO\Revisao",
  "05_ESPECIAL\Codigos\ECA", "05_ESPECIAL\Codigos\LGPD",
  "05_ESPECIAL\Codigos\MariadaPenha", "05_ESPECIAL\Codigos\StatutoIdoso",
  "05_ESPECIAL\Jurisprudencia", "05_ESPECIAL\Revisao",
  "06_JURISCONSULTOS\PRIVADO", "06_JURISCONSULTOS\PENAL",
  "06_JURISCONSULTOS\PUBLICO", "06_JURISCONSULTOS\TRABALHO",
  "06_JURISCONSULTOS\METODOLOGIA",
  "07_FILOSOFIA\Antigos", "07_FILOSOFIA\Iluministas",
  "07_FILOSOFIA\Modernos", "07_FILOSOFIA\Contemporaneos", "07_FILOSOFIA\Penalistas",
  "08_ENSINO\Univille",
  "09_FENICE_BRAIN\Metodologia", "09_FENICE_BRAIN\Templates", "09_FENICE_BRAIN\Sistema",
  "_SISTEMA\Templates", "_SISTEMA\OAB", "_SISTEMA\Projetos",
  "_SISTEMA\Arquivo", "_SISTEMA\LeisComplementares"
)
foreach ($d in $dirs) {
  New-Item -ItemType Directory -Force -Path "$base\$d" | Out-Null
}
Write-Host "Estrutura criada: $($dirs.Count) pastas"
```

- [ ] **Step 2: Verificar criação**

```powershell
$base = "C:\Fenice_bRain"
$esperadas = @("00_APEX","01_PRIVADO","02_PENAL","03_PUBLICO","04_TRABALHO",
               "05_ESPECIAL","06_JURISCONSULTOS","07_FILOSOFIA","08_ENSINO",
               "09_FENICE_BRAIN","_SISTEMA")
$ok = $true
foreach ($d in $esperadas) {
  if (-not (Test-Path "$base\$d")) { Write-Host "FALTANDO: $d"; $ok = $false }
}
if ($ok) { Write-Host "✅ Todas as 11 pastas raiz criadas" }
```

Esperado: `✅ Todas as 11 pastas raiz criadas`

- [ ] **Step 3: Commit da estrutura vazia**

```powershell
cd "C:\Fenice_bRain"
git add .
git commit -m "refactor: cria estrutura kelseniana vazia (Plano A Task 1)"
```

---

### Task 2: Migrar Fenice bRain/ → Domínios (fonte canônica)

**Files:**
- Modify: mover subpastas de `"Fenice bRain\"` para os domínios correspondentes
- Source: `C:\Fenice_bRain\Fenice bRain\` (13.645 arquivos — fonte canônica)

**Interfaces:**
- Consumes: estrutura de pastas da Task 1
- Produces: conteúdo canônico em `00_APEX/`, `01_PRIVADO/`, `02_PENAL/`, etc.

- [ ] **Step 1: Registrar contagem ANTES da migração**

```powershell
$src = "C:\Fenice_bRain\Fenice bRain"
$total = (Get-ChildItem $src -Recurse -File -EA SilentlyContinue).Count
Write-Host "Total em 'Fenice bRain\': $total arquivos"
# Anote esse número — vai verificar depois
```

Esperado: ~13.645 arquivos

- [ ] **Step 2: Migrar CF88 → 00_APEX/**

```powershell
$base = "C:\Fenice_bRain"
$src  = "$base\Fenice bRain"
Move-Item "$src\00_ESTRUTURA_CONSTITUCIONAL\*" "$base\00_APEX\" -Force -EA SilentlyContinue
Write-Host "CF88 migrado. Arquivos em 00_APEX: $((Get-ChildItem "$base\00_APEX" -Recurse -File).Count)"
```

- [ ] **Step 3: Migrar Código Civil → 01_PRIVADO/Codigos/CC/**

```powershell
$base = "C:\Fenice_bRain"
$src  = "$base\Fenice bRain"
Move-Item "$src\02_DIREITO_PRIVADO\DIREITO_CIVIL\*" "$base\01_PRIVADO\Codigos\CC\" -Force -EA SilentlyContinue
Write-Host "CC migrado: $((Get-ChildItem "$base\01_PRIVADO\Codigos\CC" -Recurse -File).Count) arquivos"
```

- [ ] **Step 4: Migrar CPC → 01_PRIVADO/Codigos/CPC/**

```powershell
$base = "C:\Fenice_bRain"
$src  = "$base\Fenice bRain"
Move-Item "$src\03_PROCESSO_CIVIL\*" "$base\01_PRIVADO\Codigos\CPC\" -Force -EA SilentlyContinue
Write-Host "CPC migrado: $((Get-ChildItem "$base\01_PRIVADO\Codigos\CPC" -Recurse -File).Count) arquivos"
```

- [ ] **Step 5: Migrar CP (DEL2848) → 02_PENAL/Codigos/CP/DEL2848/**

```powershell
$base = "C:\Fenice_bRain"
$src  = "$base\Fenice bRain"
Move-Item "$src\04_DIREITO_PENAL\CÓDIGO_PENAL\Artigos\DEL2848\*" "$base\02_PENAL\Codigos\CP\DEL2848\" -Force -EA SilentlyContinue
Write-Host "DEL2848 migrado: $((Get-ChildItem "$base\02_PENAL\Codigos\CP\DEL2848" -Recurse -File).Count) arquivos"
```

- [ ] **Step 6: Migrar CP/Crimes → 02_PENAL/Codigos/CP/Crimes/**

```powershell
$base = "C:\Fenice_bRain"
$src  = "$base\Fenice bRain"
Move-Item "$src\04_DIREITO_PENAL\CÓDIGO_PENAL\Crimes\*" "$base\02_PENAL\Codigos\CP\Crimes\" -Force -EA SilentlyContinue
Move-Item "$src\04_DIREITO_PENAL\CÓDIGO_PENAL\Dosimetria\*" "$base\02_PENAL\Codigos\CP\Crimes\" -Force -EA SilentlyContinue
# Arquivos soltos do CÓDIGO_PENAL (INDEX, etc.)
Move-Item "$src\04_DIREITO_PENAL\CÓDIGO_PENAL\*.md" "$base\02_PENAL\Codigos\CP\" -Force -EA SilentlyContinue
Write-Host "CP/Crimes migrado: $((Get-ChildItem "$base\02_PENAL\Codigos\CP" -Recurse -File).Count) arquivos"
```

- [ ] **Step 7: Migrar CPP → 02_PENAL/Codigos/CPP/**

```powershell
$base = "C:\Fenice_bRain"
$src  = "$base\Fenice bRain"
Move-Item "$src\04_DIREITO_PENAL\CÓDIGO_PROCESSO_PENAL\*" "$base\02_PENAL\Codigos\CPP\" -Force -EA SilentlyContinue
Write-Host "CPP migrado: $((Get-ChildItem "$base\02_PENAL\Codigos\CPP" -Recurse -File).Count) arquivos"
```

- [ ] **Step 8: Migrar Direito Público → 03_PUBLICO/**

```powershell
$base = "C:\Fenice_bRain"
$src  = "$base\Fenice bRain"
Move-Item "$src\07_DIREITO_ADMINISTRATIVO\*" "$base\03_PUBLICO\Codigos\Admin\" -Force -EA SilentlyContinue
Move-Item "$src\06_DIREITO_TRIBUTARIO\*"     "$base\03_PUBLICO\Codigos\Tributario\" -Force -EA SilentlyContinue
Write-Host "Público migrado: $((Get-ChildItem "$base\03_PUBLICO" -Recurse -File).Count) arquivos"
```

- [ ] **Step 9: Migrar CLT → 04_TRABALHO/**

```powershell
$base = "C:\Fenice_bRain"
$src  = "$base\Fenice bRain"
Move-Item "$src\05_DIREITO_LABORAL\*" "$base\04_TRABALHO\Codigos\CLT\" -Force -EA SilentlyContinue
Write-Host "Trabalho migrado: $((Get-ChildItem "$base\04_TRABALHO" -Recurse -File).Count) arquivos"
```

- [ ] **Step 10: Migrar Legislação Especial → 05_ESPECIAL/**

```powershell
$base = "C:\Fenice_bRain"
$src  = "$base\Fenice bRain"
Move-Item "$src\08_DIREITOS_ESPECIALIZADOS\*" "$base\05_ESPECIAL\Codigos\" -Force -EA SilentlyContinue
Write-Host "Especial migrado: $((Get-ChildItem "$base\05_ESPECIAL" -Recurse -File).Count) arquivos"
```

- [ ] **Step 11: Migrar Referências → 07_FILOSOFIA/ e 09_FENICE_BRAIN/**

```powershell
$base = "C:\Fenice_bRain"
$src  = "$base\Fenice bRain"
# Referências de filósofos/juristas
Move-Item "$src\09_REFERENCIAS\*" "$base\07_FILOSOFIA\" -Force -EA SilentlyContinue
# Sistema PKM
Move-Item "$src\_sistema\*"       "$base\09_FENICE_BRAIN\Sistema\" -Force -EA SilentlyContinue
# Leis fundamentais (complementares)
Move-Item "$src\01_LEIS_FUNDAMENTAIS\*" "$base\_SISTEMA\LeisComplementares\" -Force -EA SilentlyContinue
Write-Host "Refs/sistema migrados"
```

- [ ] **Step 12: Migrar arquivos soltos de Fenice bRain/**

```powershell
$base = "C:\Fenice_bRain"
$src  = "$base\Fenice bRain"
# Arquivos .md soltos na raiz da subfolder
Get-ChildItem "$src\*.md" | Move-Item -Destination "$base\09_FENICE_BRAIN\" -Force -EA SilentlyContinue
Write-Host "Arquivos soltos migrados"
```

- [ ] **Step 13: Verificar que Fenice bRain/ está vazia (ou só com pastas vazias)**

```powershell
$src = "C:\Fenice_bRain\Fenice bRain"
$restantes = (Get-ChildItem $src -Recurse -File -EA SilentlyContinue).Count
Write-Host "Arquivos restantes em 'Fenice bRain\': $restantes"
if ($restantes -gt 0) {
  Get-ChildItem $src -Recurse -File | Select-Object -First 20 FullName
}
```

Esperado: 0 arquivos (ou listar os restantes para análise manual)

- [ ] **Step 14: Commit da migração canônica**

```powershell
cd "C:\Fenice_bRain"
git add -u
git add .
git commit -m "refactor: migra Fenice bRain/ (canônico) para estrutura kelseniana (Plano A Task 2)"
```

---

### Task 3: Mesclar e Eliminar Pastas ⚖️ da Raiz

**Files:**
- Source: `⚖️ Direito Civil\`, `⚖️ Direito Penal\`, `⚖️ constFederal88\`, `⚖️ c_l_t_trabalho\`, `⚖️ c_d_consumidor\`, `⚖️ Direito - OAB\`, `⚖️ direito tributário\`
- Consumes: nova estrutura canônica da Task 2
- Produces: exclusivos mesclados; pastas ⚖️ deletadas

- [ ] **Step 1: Identificar exclusivos em ⚖️ Direito Civil/**

```powershell
$base    = "C:\Fenice_bRain"
$emojis  = "$base\⚖️ Direito Civil"
$novo    = "$base\01_PRIVADO\Codigos\CC"

# Lista arquivos em ⚖️ que NÃO existem em 01_PRIVADO por nome
$novosNomes = Get-ChildItem $novo -Recurse -File | Select-Object -ExpandProperty Name
$exclusivos = Get-ChildItem $emojis -Recurse -File |
  Where-Object { $novosNomes -notcontains $_.Name }
Write-Host "Exclusivos em ⚖️ Direito Civil: $($exclusivos.Count)"
$exclusivos | Select-Object -First 10 FullName
```

- [ ] **Step 2: Mover exclusivos de ⚖️ Direito Civil → 01_PRIVADO/**

```powershell
$base    = "C:\Fenice_bRain"
$emojis  = "$base\⚖️ Direito Civil"
$novo    = "$base\01_PRIVADO\Codigos\CC"
$novosNomes = Get-ChildItem $novo -Recurse -File | Select-Object -ExpandProperty Name

Get-ChildItem $emojis -Recurse -File |
  Where-Object { $novosNomes -notcontains $_.Name } |
  ForEach-Object { Move-Item $_.FullName $novo -Force -EA SilentlyContinue }
Write-Host "Exclusivos movidos para 01_PRIVADO\Codigos\CC\"
```

- [ ] **Step 3: Deletar ⚖️ Direito Civil/**

```powershell
Remove-Item "C:\Fenice_bRain\⚖️ Direito Civil" -Recurse -Force -Confirm:$false
Write-Host "⚖️ Direito Civil deletado"
```

- [ ] **Step 4: Repetir para ⚖️ Direito Penal → 02_PENAL/**

```powershell
$base    = "C:\Fenice_bRain"
$emojis  = "$base\⚖️ Direito Penal"
$novo    = "$base\02_PENAL\Codigos\CP\Crimes"
$novosNomes = Get-ChildItem "$base\02_PENAL" -Recurse -File | Select-Object -ExpandProperty Name

$excl = Get-ChildItem $emojis -Recurse -File | Where-Object { $novosNomes -notcontains $_.Name }
Write-Host "Exclusivos ⚖️ Penal: $($excl.Count)"
$excl | ForEach-Object { Move-Item $_.FullName $novo -Force -EA SilentlyContinue }
Remove-Item $emojis -Recurse -Force -Confirm:$false
Write-Host "⚖️ Direito Penal deletado"
```

- [ ] **Step 5: Mesclar ⚖️ constFederal88 → 00_APEX/**

```powershell
$base   = "C:\Fenice_bRain"
$emojis = "$base\⚖️ constFederal88"
$novo   = "$base\00_APEX"
$novosNomes = Get-ChildItem $novo -Recurse -File | Select-Object -ExpandProperty Name

Get-ChildItem $emojis -Recurse -File |
  Where-Object { $novosNomes -notcontains $_.Name } |
  ForEach-Object { Move-Item $_.FullName $novo -Force -EA SilentlyContinue }
Remove-Item $emojis -Recurse -Force -Confirm:$false
Write-Host "⚖️ constFederal88 deletado"
```

- [ ] **Step 6: Mesclar ⚖️ c_l_t_trabalho → 04_TRABALHO/**

```powershell
$base   = "C:\Fenice_bRain"
$emojis = "$base\⚖️ c_l_t_trabalho"
$novo   = "$base\04_TRABALHO\Codigos\CLT"
$novosNomes = Get-ChildItem $novo -Recurse -File | Select-Object -ExpandProperty Name

Get-ChildItem $emojis -Recurse -File |
  Where-Object { $novosNomes -notcontains $_.Name } |
  ForEach-Object { Move-Item $_.FullName $novo -Force -EA SilentlyContinue }
Remove-Item $emojis -Recurse -Force -Confirm:$false
Write-Host "⚖️ c_l_t_trabalho deletado"
```

- [ ] **Step 7: Mesclar ⚖️ c_d_consumidor → 05_ESPECIAL/**

```powershell
$base   = "C:\Fenice_bRain"
$emojis = "$base\⚖️ c_d_consumidor"
$novo   = "$base\05_ESPECIAL\Codigos\ECA"
$novosNomes = Get-ChildItem "$base\05_ESPECIAL" -Recurse -File | Select-Object -ExpandProperty Name

Get-ChildItem $emojis -Recurse -File |
  Where-Object { $novosNomes -notcontains $_.Name } |
  ForEach-Object { Move-Item $_.FullName $novo -Force -EA SilentlyContinue }
Remove-Item $emojis -Recurse -Force -Confirm:$false
Write-Host "⚖️ c_d_consumidor deletado"
```

- [ ] **Step 8: Mover OAB → _SISTEMA/OAB/**

```powershell
$base = "C:\Fenice_bRain"
Move-Item "$base\⚖️ Direito - OAB\*" "$base\_SISTEMA\OAB\" -Force -EA SilentlyContinue
Move-Item "$base\oab\*"              "$base\_SISTEMA\OAB\" -Force -EA SilentlyContinue
Remove-Item "$base\⚖️ Direito - OAB" -Recurse -Force -Confirm:$false
Remove-Item "$base\oab"              -Recurse -Force -Confirm:$false
Write-Host "OAB consolidado em _SISTEMA\OAB\"
```

- [ ] **Step 9: Deletar ⚖️ direito tributário (subconjunto)**

```powershell
$base   = "C:\Fenice_bRain"
$emojis = "$base\⚖️ direito tributário"
$novo   = "$base\03_PUBLICO\Codigos\Tributario"
$novosNomes = Get-ChildItem $novo -Recurse -File | Select-Object -ExpandProperty Name

Get-ChildItem $emojis -Recurse -File |
  Where-Object { $novosNomes -notcontains $_.Name } |
  ForEach-Object { Move-Item $_.FullName $novo -Force -EA SilentlyContinue }
Remove-Item $emojis -Recurse -Force -Confirm:$false
Write-Host "⚖️ direito tributário deletado"
```

- [ ] **Step 10: Commit da limpeza ⚖️**

```powershell
cd "C:\Fenice_bRain"
git add -u
git add .
git commit -m "refactor: mescla e elimina pastas emoji raiz (Plano A Task 3)"
```

---

### Task 4: Consolidar e Eliminar 02 - Áreas/

**Files:**
- Source: `02 - Áreas\Base Jurídica\` (4.058 arquivos — subconjunto de Fenice bRain/)
- Produces: exclusivos mesclados; `02 - Áreas\` deletado

- [ ] **Step 1: Checar exclusivos em 02 - Áreas/**

```powershell
$base  = "C:\Fenice_bRain"
$areas = "$base\02 - Áreas\Base Jurídica"

# Nomes já na nova estrutura
$novosNomes = Get-ChildItem "$base\00_APEX","$base\01_PRIVADO","$base\02_PENAL",
  "$base\03_PUBLICO","$base\04_TRABALHO","$base\05_ESPECIAL" -Recurse -File -EA SilentlyContinue |
  Select-Object -ExpandProperty Name

$exclusivos = Get-ChildItem $areas -Recurse -File -EA SilentlyContinue |
  Where-Object { $novosNomes -notcontains $_.Name }

Write-Host "Exclusivos em 02 - Áreas: $($exclusivos.Count)"
$exclusivos | Select-Object -First 20 FullName
```

- [ ] **Step 2: Mover exclusivos para domínio correto**

```powershell
# Exclusivos identificados no Step 1 — mover manualmente ou em lote:
$base       = "C:\Fenice_bRain"
$novosNomes = Get-ChildItem "$base\00_APEX","$base\01_PRIVADO","$base\02_PENAL",
  "$base\03_PUBLICO","$base\04_TRABALHO","$base\05_ESPECIAL" -Recurse -File -EA SilentlyContinue |
  Select-Object -ExpandProperty Name

Get-ChildItem "$base\02 - Áreas\Base Jurídica" -Recurse -File -EA SilentlyContinue |
  Where-Object { $novosNomes -notcontains $_.Name } |
  ForEach-Object {
    # Destino heurístico por path
    $dest = if     ($_.FullName -match "DIREITO_CIVIL|02_DIREITO_PRIVADO") { "$base\01_PRIVADO\Codigos\CC" }
            elseif ($_.FullName -match "PROCESSO_CIVIL|03_PROCESSO")      { "$base\01_PRIVADO\Codigos\CPC" }
            elseif ($_.FullName -match "DIREITO_PENAL|04_DIREITO_PENAL")  { "$base\02_PENAL\Codigos\CP\Crimes" }
            elseif ($_.FullName -match "CONSTITUCIONAL|00_ESTRUTURA")     { "$base\00_APEX" }
            elseif ($_.FullName -match "TRIBUTARIO|06_DIREITO")           { "$base\03_PUBLICO\Codigos\Tributario" }
            elseif ($_.FullName -match "LABORAL|05_DIREITO")              { "$base\04_TRABALHO\Codigos\CLT" }
            elseif ($_.FullName -match "ESPECIALIZADOS|08_DIREITO")       { "$base\05_ESPECIAL\Codigos" }
            else                                                           { "$base\_SISTEMA\Arquivo" }
    Move-Item $_.FullName $dest -Force -EA SilentlyContinue
  }
Write-Host "Exclusivos de 02 - Áreas movidos"
```

- [ ] **Step 3: Deletar 02 - Áreas/**

```powershell
$remaining = (Get-ChildItem "C:\Fenice_bRain\02 - Áreas" -Recurse -File -EA SilentlyContinue).Count
Write-Host "Arquivos restantes em 02 - Áreas: $remaining"
if ($remaining -eq 0) {
  Remove-Item "C:\Fenice_bRain\02 - Áreas" -Recurse -Force -Confirm:$false
  Write-Host "✅ 02 - Áreas deletado"
} else {
  Write-Host "⚠️  Ainda há $remaining arquivos — revisar antes de deletar"
}
```

- [ ] **Step 4: Commit**

```powershell
cd "C:\Fenice_bRain"
git add -u && git add .
git commit -m "refactor: consolida e elimina 02 - Áreas/ (Plano A Task 4)"
```

---

### Task 5: Consolidar Pastas Numeradas → _SISTEMA/

**Files:**
- Source: `00 - Inbox\`, `01 - Projetos\`, `04 - Arquivo\`, `05 - Templates\`, `06 - NotebookLM\`, `Briefing Claude diário\`, `backend-python\`, `Lei X\`
- Produces: conteúdo em `_SISTEMA\`; pastas numeradas deletadas

- [ ] **Step 1: Mover para _SISTEMA/**

```powershell
$base = "C:\Fenice_bRain"
$moves = @{
  "00 - Inbox"             = "_SISTEMA\Inbox"
  "01 - Projetos"          = "_SISTEMA\Projetos"
  "04 - Arquivo"           = "_SISTEMA\Arquivo"
  "05 - Templates"         = "_SISTEMA\Templates"
  "06 - NotebookLM"        = "_SISTEMA\NotebookLM"
  "Briefing Claude diário" = "_SISTEMA\Briefings"
  "backend-python"         = "scripts\backend-python"
  "Lei X"                  = "_SISTEMA\LeisComplementares"
  "docs"                   = "_SISTEMA\docs"
  "_sistema"               = "_SISTEMA\sistema-legado"
}
foreach ($src in $moves.Keys) {
  $srcPath  = "$base\$src"
  $destPath = "$base\$($moves[$src])"
  if (Test-Path $srcPath) {
    New-Item -ItemType Directory -Force -Path $destPath | Out-Null
    Move-Item "$srcPath\*" $destPath -Force -EA SilentlyContinue
    Remove-Item $srcPath -Recurse -Force -Confirm:$false -EA SilentlyContinue
    Write-Host "✅ $src → $($moves[$src])"
  } else {
    Write-Host "⚠️  Não encontrado: $src"
  }
}
```

- [ ] **Step 2: Verificar raiz limpa**

```powershell
$base     = "C:\Fenice_bRain"
$esperado = @("_SISTEMA","00_APEX","01_PRIVADO","02_PENAL","03_PUBLICO",
              "04_TRABALHO","05_ESPECIAL","06_JURISCONSULTOS","07_FILOSOFIA",
              "08_ENSINO","09_FENICE_BRAIN","scripts",
              ".git",".obsidian",".claude","Fenice bRain","copilot","Excalidraw")
$atual = Get-ChildItem $base -Directory | Select-Object -ExpandProperty Name
$inesperadas = $atual | Where-Object { $esperado -notcontains $_ }
if ($inesperadas) {
  Write-Host "⚠️  Pastas inesperadas na raiz: $($inesperadas -join ', ')"
} else {
  Write-Host "✅ Raiz limpa"
}
```

- [ ] **Step 3: Deletar Fenice bRain/ (agora vazia)**

```powershell
$restantes = (Get-ChildItem "C:\Fenice_bRain\Fenice bRain" -Recurse -File -EA SilentlyContinue).Count
Write-Host "Arquivos restantes em 'Fenice bRain\': $restantes"
if ($restantes -eq 0) {
  Remove-Item "C:\Fenice_bRain\Fenice bRain" -Recurse -Force -Confirm:$false
  Write-Host "✅ Fenice bRain\ (subfolder) deletado"
} else {
  Write-Host "⚠️  $restantes arquivos — mover manualmente antes de deletar"
  Get-ChildItem "C:\Fenice_bRain\Fenice bRain" -Recurse -File | Select-Object -First 10 FullName
}
```

- [ ] **Step 4: Commit**

```powershell
cd "C:\Fenice_bRain"
git add -u && git add .
git commit -m "refactor: consolida pastas numeradas em _SISTEMA/ e remove Fenice bRain\ (Plano A Task 5)"
```

---

### Task 6: Atualizar Plugin — Paths do Array CODIGOS

**Files:**
- Modify: `C:\Fenice_bRain\.obsidian\plugins\fenice-buscar-artigo\main.js`
- Modify: `C:\Fenice_bRain\scripts\obsidian-plugin-fenice-buscar-artigo-updated.js`

**Interfaces:**
- Consumes: nova estrutura de pastas das Tasks 1–5
- Produces: plugin v21b com paths atualizados; pronto para ser base do Plano B (v22/DomainModal)

- [ ] **Step 1: Localizar o array CODIGOS no plugin**

```powershell
Select-String -Path "C:\Fenice_bRain\.obsidian\plugins\fenice-buscar-artigo\main.js" `
  -Pattern "pastas|pasta|codigo.*CP|codigo.*CC|Fenice bRain" |
  Select-Object -First 30 | Format-Table LineNumber, Line -AutoSize
```

Identificar as linhas exatas do array para editar no VS Code.

- [ ] **Step 2: Substituir paths no plugin**

Abrir `main.js` no VS Code e substituir os paths do array CODIGOS.  
Paths a substituir (usar Find & Replace — Ctrl+H):

| De (old) | Para (new) |
|---|---|
| `'Fenice bRain/02_DIREITO_PRIVADO/DIREITO_CIVIL` | `'01_PRIVADO/Codigos/CC` |
| `'02 - Áreas/Base Jurídica/02_DIREITO_PRIVADO` | `'01_PRIVADO/Codigos/CC` |
| `'Fenice bRain/03_PROCESSO_CIVIL` | `'01_PRIVADO/Codigos/CPC` |
| `'02 - Áreas/Base Jurídica/03_PROCESSO_CIVIL` | `'01_PRIVADO/Codigos/CPC` |
| `'Fenice bRain/04_DIREITO_PENAL/CÓDIGO_PENAL/Artigos/DEL2848'` | `'02_PENAL/Codigos/CP/DEL2848'` |
| `'02 - Áreas/Base Jurídica/04_DIREITO_PENAL/CÓDIGO_PENAL/Crimes'` | `'02_PENAL/Codigos/CP/Crimes'` |
| `'Fenice bRain/04_DIREITO_PENAL/CÓDIGO_PROCESSO_PENAL` | `'02_PENAL/Codigos/CPP` |
| `'Fenice bRain/07_DIREITO_ADMINISTRATIVO` | `'03_PUBLICO/Codigos/Admin` |
| `'Fenice bRain/06_DIREITO_TRIBUTARIO` | `'03_PUBLICO/Codigos/Tributario` |
| `'Fenice bRain/05_DIREITO_LABORAL` | `'04_TRABALHO/Codigos/CLT` |
| `'Fenice bRain/08_DIREITOS_ESPECIALIZADOS` | `'05_ESPECIAL/Codigos` |
| `'Fenice bRain/00_ESTRUTURA_CONSTITUCIONAL` | `'00_APEX` |
| `'02 - Áreas/Base Jurídica/00_ESTRUTURA_CONSTITUCIONAL` | `'00_APEX` |

- [ ] **Step 3: Atualizar console.log de versão**

No `main.js`, linha ~750:
```javascript
console.log('✅ Fenice Buscar Artigo v21b — paths migração kelseniana');
```

- [ ] **Step 4: Sincronizar scripts/**

```powershell
Copy-Item "C:\Fenice_bRain\.obsidian\plugins\fenice-buscar-artigo\main.js" `
          "C:\Fenice_bRain\scripts\obsidian-plugin-fenice-buscar-artigo-updated.js" -Force
Write-Host "Scripts sincronizado"
```

- [ ] **Step 5: Commit**

```powershell
cd "C:\Fenice_bRain"
git add -u
git commit -m "fix: atualiza paths do plugin para estrutura kelseniana (v21b)"
```

---

### Task 7: Atualizar Scripts de Backup e Extração

**Files:**
- Modify: `C:\Fenice_bRain\scripts\` — verificar paths de backup e extratores

- [ ] **Step 1: Listar scripts com paths antigos**

```powershell
Select-String -Path "C:\Fenice_bRain\scripts\*" -Pattern "Fenice bRain|02 - Áreas|⚖️" -Recurse |
  Select-Object Filename, LineNumber, Line | Format-Table -AutoSize
```

- [ ] **Step 2: Atualizar paths em cada script identificado**

Para cada arquivo listado no Step 1, substituir paths usando VS Code (Find & Replace com as mesmas substituições da Task 6).

- [ ] **Step 3: Verificar script de backup**

```powershell
# Verificar que o backup ainda aponta para o vault correto
Get-Content "C:\Fenice_bRain\scripts\setup-gdrive.ps1" -ErrorAction SilentlyContinue |
  Select-String "Fenice|vault|source" | Format-Table
```

- [ ] **Step 4: Commit**

```powershell
cd "C:\Fenice_bRain"
git add -u
git commit -m "fix: atualiza paths de scripts para estrutura kelseniana (Plano A Task 7)"
```

---

### Task 8: Verificação Final e Abertura no Obsidian

**Files:**
- Verify: `.obsidian\graph.json` — atualizar filtro para nova estrutura
- Verify: plugin funcionando com novos paths
- Verify: wikilinks não quebrados

- [ ] **Step 1: Atualizar filtro do Graph View**

```powershell
$graph = Get-Content "C:\Fenice_bRain\.obsidian\graph.json" | ConvertFrom-Json
$graph.search = 'path:"02_PENAL/Codigos/CP/DEL2848"'
$graph | ConvertTo-Json -Depth 5 | Set-Content "C:\Fenice_bRain\.obsidian\graph.json"
Write-Host "graph.json atualizado"
```

- [ ] **Step 2: Contagem final do vault**

```powershell
$base  = "C:\Fenice_bRain"
$total = (Get-ChildItem $base -Recurse -File -EA SilentlyContinue |
          Where-Object { $_.FullName -notmatch '\.git\\' }).Count
Write-Host "Total de arquivos no vault: $total"

@("00_APEX","01_PRIVADO","02_PENAL","03_PUBLICO","04_TRABALHO",
  "05_ESPECIAL","06_JURISCONSULTOS","07_FILOSOFIA","08_ENSINO",
  "09_FENICE_BRAIN","_SISTEMA") | ForEach-Object {
  $c = (Get-ChildItem "$base\$_" -Recurse -File -EA SilentlyContinue).Count
  Write-Host "  $_: $c arquivos"
}
```

- [ ] **Step 3: Abrir Obsidian e verificar plugin**

1. Abrir Obsidian apontando para `C:\Fenice_bRain`
2. Abrir Developer Console (Ctrl+Shift+I → Console)
3. Verificar: `✅ Fenice Buscar Artigo v21b — paths migração kelseniana`
4. Testar: Ctrl+Shift+B → buscar CP Art. 121 → InfoModal com redação legal ✅
5. Testar: Ctrl+Shift+B → buscar CC Art. 1 → InfoModal com redação ✅

- [ ] **Step 4: Verificar broken links no Obsidian**

1. Obsidian → Settings → Files & Links → verificar "Broken links"
2. Ou usar Omnisearch para buscar `[[` e checar links órfãos
3. Documentar links quebrados encontrados (não bloqueia — são reparados incrementalmente)

- [ ] **Step 5: Commit final**

```powershell
cd "C:\Fenice_bRain"
git add -u && git add .
git commit -m "feat: Plano A concluído — vault kelseniano com estrutura canônica única

Elimina 3 cópias redundantes (Fenice bRain/ + emojis + 02-Áreas).
Nova estrutura: 00_APEX → 09_FENICE_BRAIN + _SISTEMA.
Plugin v21b com paths atualizados.
Pronto para Plano B: DomainModal + JurisconsultoModal + FilosofoModal."
```

---

## Próximo Passo — Plano B

Após Task 8 aprovada, invocar `/writing-plans` com:

> "Criar Plano B: Plugin v22 — DomainModal (Ctrl+Shift+B dois níveis), JurisconsultoModal (Ctrl+Shift+J), FilosofoModal (Ctrl+Shift+F). Vault já na estrutura kelseniana do Plano A."
