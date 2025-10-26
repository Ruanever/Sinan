# Sinan
Dicionários de dados Sinan em arquivo JSON

### Leishmaniose Tegumentar: https://raw.githubusercontent.com/Ruanever/Sinan/refs/heads/main/LTAN.JSON

## Exemplo de como usá-lo:

### Importa o JSON
```python
import json
import pandas as pd

# Suba o LTAN.JSON aos seus arquivos ou carregue diretamente da URL
# Exemplo de URL para Leishmaniose Tegumentar:
# url = "COLE_AQUI_A_URL_DO_ARQUIVO_JSON"

# Se você baixou o arquivo localmente:
with open("LTAN.JSON", "r", encoding="utf-8") as f:
    cod = json.load(f)

# Se quiser carregar direto da URL:
# import requests
# response = requests.get(url)
# cod = response.json()

# Renomear colunas (df é onde o banco de leishmaniose está carregado)
df = df.rename(columns={k: v["rename"] for k, v in cod.items() if "rename" in v})

# Aplicar rótulos nas variáveis categóricas
for var, info in cod.items():
    if "labels" in info:
        col = info["rename"]
        if col in df.columns:  # Verifica se a coluna renomeada existe
            df[col] = df[col].astype(str).map(info["labels"])

# Display do DataFrame transformado
display(df.head())
