# Sinan
Dicionários de dados Sinan em arquivo JSON

## Exemplo de como usá-lo:

### Importa o JSON
```python
import json

# Suba o LTAN.JSON aos seus arquivos
with open("LTAN.JSON", "r", encoding="utf-8") as f:
    cod = json.load(f)

# Renomear colunas (df é onde o banco de leishmaniose visceral está carregado)
df = df.rename(columns={k: v["rename"] for k, v in cod.items() if "rename" in v})

# Aplicar rótulos nas variáveis categóricas
for var, info in cod.items():
    if "labels" in info:
        col = info["rename"]
        if col in df.columns:  # Verifica se a coluna renomeada existe
            # Garante que a coluna seja do tipo string antes de mapear os rótulos
            df[col] = df[col].astype(str).map(info["labels"])

# Display do DataFrame transformado
display(df.head())
