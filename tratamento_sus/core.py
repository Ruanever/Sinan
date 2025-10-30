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
    for cname in df.columns:
        # --- DATAS: tenta dd/mm/YYYY primeiro, depois fallback ---
        if cname.startswith("DT_"):
            orig = df[cname]
            # tenta formato comum do SINAN
            df[cname] = pd.to_datetime(orig, format="%d/%m/%Y", errors="coerce")

            # se algum valor não era nulo e virou NaT, tenta conversão geral
            mask = orig.notna() & df[cname].isna()
            if mask.any():
                df.loc[mask, cname] = pd.to_datetime(orig[mask], errors="coerce")

        # --- IDS: regra segura para não apagar CID alfanumérico ---
        elif cname.startswith("ID_"):
            # sempre manter ID_AGRAVO como string (CID alfanumérico)
            if cname == "ID_AGRAVO":
                df[cname] = df[cname].astype(str)
                continue

            s = df[cname].astype(str)

            # se houver pelo menos um caractere alfabético, manter como string
            if s.str.contains(r"[A-Za-z]", na=False).any():
                df[cname] = s
                continue

            # caso contrário, tenta converter para numérico
            num = pd.to_numeric(s.str.replace(r"[,\s]", "", regex=True), errors="coerce")

            # se todos os valores numéricos (não-nulos) forem inteiros, usar Int64 (nullable)
            non_na = num.dropna()
            if not non_na.empty and (non_na % 1 == 0).all():
                df[cname] = num.astype("Int64")
            else:
                # mantém float (ou NaN) para valores com casas decimais
                df[cname] = num

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
