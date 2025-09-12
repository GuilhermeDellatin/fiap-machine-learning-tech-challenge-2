O seguinte script gera o zip da Lambda

```powershell
$ErrorActionPreference = 'Stop'

# (a) Limpar e preparar pasta de build
Remove-Item -Recurse -Force build -ErrorAction Ignore
New-Item -ItemType Directory -Path build | Out-Null

# (b) Criar venv para evitar o erro de --user e usar o pip correto
py -m venv .venv
.\.venv\Scripts\Activate.ps1

# (c) Instalar SOMENTE o que precisa dentro de build/
python -m pip install --upgrade pip
python -m pip install --no-cache-dir --target build requests==2.32.3

# (d) Copiar seu código para build/
Copy-Item sanitize -Destination build\sanitize -Recurse
Copy-Item scrapper -Destination build\scrapper -Recurse
# (opcional) se precisar dessa pasta:
# Copy-Item outra_pasta -Destination build\outra_pasta -Recurse

# (e) Limpar lixos (opcional, só para reduzir tamanho)
Get-ChildItem build -Recurse -Include "__pycache__", "*.pyc", "tests" | Remove-Item -Recurse -Force

# (f) Gerar o ZIP  -> ZIP **do conteúdo** da pasta build (não zipar a pasta build em si!)
Compress-Archive -Path build\* -DestinationPath function.zip -Force

# (g) Desativar o venv
deactivate
```