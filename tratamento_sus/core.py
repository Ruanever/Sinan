import pandas as pd
import requests
import json


def carregar_dicionario(banco: str) -> dict:
    base_url = "https://raw.githubusercontent.com/Ruanever/Sinan/refs/heads/main/"
    url = f"{base_url}{banco}.JSON"
    resposta = requests.get(url)
    resposta.raise_for_status()
    return json.loads(resposta.text)


def aplicar_dicionario(df: pd.DataFrame, banco: str) -> pd.DataFrame:
    """
    Aplica o dicionário do banco informado ao DataFrame:
      - Pré-processa variáveis (datas e IDs) de forma robusta
      - Renomeia as colunas conforme o campo 'rename'
      - Decodifica os valores conforme o campo 'labels'
    """
    df = df.copy()

    # Pré-processamento robusto
    # === PRÉ-PROCESSAMENTO ===
    for cname in df.columns:

        # ----- Datas -----
        if cname.startswith("DT_"):
            orig = df[cname]
            df[cname] = pd.to_datetime(orig, format="%d/%m/%Y", errors="coerce")

            # fallback: só tenta converter quem falhou
            mask = orig.notna() & df[cname].isna()
            if mask.any():
                df.loc[mask, cname] = pd.to_datetime(orig[mask], errors="coerce")

        # ----- IDs (manter tudo como string) -----
        elif cname.startswith("ID_"):
            df[cname] = df[cname].astype(str)

    # Carrega dicionário e aplica renomeações / labels
    dicionario = carregar_dicionario(banco)

    # Renomear colunas
    renomear = {var: info["rename"] for var, info in dicionario.items() if "rename" in info}
    df.rename(columns=renomear, inplace=True)

    # Decodificar valores categóricos
    for var_original, info in dicionario.items():
        if "labels" in info:
            nova_col = info.get("rename", var_original)
            labels = info["labels"]
            if nova_col in df.columns:
                # Substitui valores (mantendo tipos já convertidos antes)
                df[nova_col] = df[nova_col].astype(str).replace(labels)

    print("\n✅ DataFrame processado:")
    df.info()
    return df
