import re

def replaceregex(row):
    return re.sub("[.,\s]", "", row)


class Sanitize:
    def __init__(self):
        pass

    @staticmethod
    def clean_df(df):
        df = df.rename(columns={'segment': 'setor', 'cod': 'codigo', 'asset': 'acao', 'type': 'tipo',
                                'theoricalQty': 'quantidade_teorica', 'partAcum': 'porcentagem_participacao_acumulada',
                                'part': 'porcentagem_participacao'})
        df["quantidade_teorica"] = df["quantidade_teorica"].apply(replaceregex).astype("int64")
        df["porcentagem_participacao"] = df["porcentagem_participacao"].str.replace(",", ".").astype("float")
        df["porcentagem_participacao_acumulada"] = df["porcentagem_participacao_acumulada"].str.replace(",",
                                                                                                        ".").astype(
            "float")
        return df