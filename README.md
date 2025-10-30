# 🧬 Tratamento de dados SINAN

Biblioteca Python para **rotulação automática dos dados dos sistemas do SINAN**, utilizando dicionários JSON públicos.  
Permite **renomear variáveis e decodificar valores categóricos** de forma simples e rápida.

Obs.: PRECISA BAIXAR O BANCO ANTES VIA PYSUS
---

## ✅ Sistemas disponíveis

| Código | Sistema |
|--------|---------|
| `LTAN` | Leishmaniose Tegumentar Americana |
| `LEIV` | Leishmaniose Visceral |
Outros dicionários estarão disponíveis em breve.

---

## 🚀 Instalação

Instale diretamente do repositório:

```bash
pip install git+https://github.com/Ruanever/Sinan.git
```
💡 Exemplo de uso  
1️⃣ Importar a biblioteca
```bash
from tratamento_sus import aplicar_dicionario
import pandas as pd
```
2️⃣ Carregar seu banco de dados
```bash
# Exemplo: dataframe do LTAN baixado via PySUS ou carregado localmente
df = pd.read_csv("LTAN.csv")
```
3️⃣ Aplicar o dicionário de variáveis
```bash
# "LTAN" é o dicionário para Leishmaniose Tegumentar
df_tratado = aplicar_dicionario(df, "LTAN")

# Verificar as primeiras linhas
print(df_tratado.head())
```
---
🧑‍💻 Autor  
**Mestrando Enf. Ruan Everton**  
GitHub: @Ruanever  
Email: ruan.everton@outlook.com  
Intagram: ruan_evertonss
