import pandas as pd
import requests
import json


def carregar_dicionario(banco: str) -> dict:
    """
    Carrega o dicionário JSON correspondente ao banco especificado
    diretamente do repositório GitHub.
    Exemplo: banco = "LTAN"
    """
    base_url = "https://raw.githubusercontent.com/Ruanever/Sinan/refs/heads/main/"
    url = f"{base_url}{banco}.JSON"
    resposta = requests.get(url)
    resposta.raise_for_status()
    return json.loads(resposta.text)


def aplicar_dicionario(df: pd.DataFrame, banco: str) -> pd.DataFrame:
    """
    Aplica o dicionário do banco informado ao DataFrame:
      - Renomeia as colunas conforme o campo 'rename'
      - Decodifica os valores conforme o campo 'labels'
    
    Parâmetros:
      df: DataFrame com os dados originais
      banco: código do banco (ex: 'LTAN')
    
    Retorna:
      DataFrame com variáveis tratadas e valores decodificados
    """
    dicionario = carregar_dicionario(banco)
    df = df.copy()

    # Renomear colunas
    renomear = {var: info["rename"] for var, info in dicionario.items() if "rename" in info}
    df.rename(columns=renomear, inplace=True)

    # Decodificar valores categóricos
    for var_original, info in dicionario.items():
        if "labels" in info:
            nova_col = info.get("rename", var_original)
            labels = info["labels"]
            if nova_col in df.columns:
                df[nova_col] = df[nova_col].astype(str).replace(labels)

    return df
