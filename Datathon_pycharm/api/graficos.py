import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import (
    train_test_split,
)
from sklearn.inspection import permutation_importance


RANDOM_STATE = 42

#Graficos Pergunta 1
class dados_ian:
    @staticmethod
    def classificar_ian(valor):
        if pd.isna(valor):
            return np.nan
        if valor >= 7.5:
            return "Adequado"
        if valor >= 5:
            return "Defasagem moderada"
        return "Defasagem severa"

    @staticmethod
    def tabela_ian(dados):
        dados["Nivel_IAN"] = dados["IAN"].apply(dados_ian.classificar_ian)
        ian_ano = pd.crosstab(
        dados["Ano"],
        dados["Nivel_IAN"],
        normalize="index"
        ).mul(100)
        ian_contagem = pd.crosstab(dados["Ano"], dados["Nivel_IAN"])
        return ian_contagem

    @staticmethod
    def tabela_melhora(dados):
        # Evolução individual da defasagem entre anos consecutivos
        painel_defas = dados.pivot_table(
            index="RA",
            columns="Ano",
            values="Defasagem",
            aggfunc="last"
        )
        transicoes = []
        for ano_atual, ano_seguinte in [(2022, 2023), (2023, 2024)]:
            pares = painel_defas[[ano_atual, ano_seguinte]].dropna().copy()
            pares["Mudanca"] = pares[ano_seguinte] - pares[ano_atual]
            pares["Situacao"] = np.select(
                [
                    pares["Mudanca"] < 0,
                    pares["Mudanca"] == 0,
                    pares["Mudanca"] > 0
                ],
                [
                    "Piorou",
                    "Permaneceu",
                    "Melhorou"
                ],
                default="Sem classificação"
            )
            resumo = pares["Situacao"].value_counts().rename_axis("Situacao").reset_index(name="Alunos")
            resumo["Transicao"] = f"{ano_atual} → {ano_seguinte}"
            transicoes.append(resumo)

            resumo_transicoes = pd.concat(transicoes, ignore_index=True)

            resumo_transicoes = resumo_transicoes.pivot(
                index="Transicao",
                columns="Situacao",
                values="Alunos"
            ).reset_index()
            resumo_transicoes = resumo_transicoes.set_index("Transicao")
        return resumo_transicoes

#Graficos Pergunta 2
class dados_ida:
    @staticmethod
    def ida_media(dados):
        ida_ano = dados.groupby("Ano")["IDA"].agg(["count", "mean", "median", "std"])
        plt.figure(figsize=(9, 5))
        sns.pointplot(data=dados, x="Ano", y="IDA", errorbar=("ci", 95), capsize=.1)
        plt.ylim(0, 10)
        plt.title("Evolução do IDA médio")
        plt.ylabel("IDA médio")
        plt.xlabel("Ano")
        plt.tight_layout()
        return plt.gcf()
    @staticmethod
    def ida_heatmap(dados):
        ida_fase_ano = dados.pivot_table(
            index="Fase",
            columns="Ano",
            values="IDA",
            aggfunc="mean"
        )
        ordem_fases = ["ALFA"] + [f"FASE {i}" for i in range(1, 9)]
        ida_fase_ano = ida_fase_ano.reindex(
            [f for f in ordem_fases if f in ida_fase_ano.index]
        )
        plt.figure(figsize=(12, 8))
        sns.heatmap(ida_fase_ano, annot=True, fmt=".2f", cmap="YlGnBu", vmin=0, vmax=10)
        plt.title("IDA médio por fase e ano")
        plt.xlabel("Ano")
        plt.ylabel("Fase")
        return plt.gcf()
    @staticmethod
    def evo_ida(dados):
        painel_ida = dados.pivot_table(
            index="RA",
            columns="Ano",
            values="IDA",
            aggfunc="last"
        )
        resultados = []
        for a, b in [(2022, 2023), (2023, 2024)]:
            pares = painel_ida[[a, b]].dropna()
            delta = pares[b] - pares[a]
            resultados.append({
                "Transição": f"{a} → {b}",
                "Alunos": len(delta),
                "Variação média": delta.mean(),
                "% Melhorou": (delta > 0).mean() * 100
            })
        df_resultados = pd.DataFrame(resultados)
        return df_resultados
#Graficos Pergunta 3
class dados_ieg:
    @staticmethod
    def ieg(dados):
        correlacoes_engajamento = dados[["IEG", "IDA", "IPV"]].corr(method="spearman")
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        sns.regplot(
            data=dados,
            x="IEG",
            y="IDA",
            scatter_kws={"alpha": 0.25},
            line_kws={"color": "red"},
            ax=axes[0]
        )
        axes[0].set_title("Engajamento × Desempenho")
        axes[0].set_xlim(0, 10)
        axes[0].set_ylim(0, 10)

        sns.regplot(
            data=dados,
            x="IEG",
            y="IPV",
            scatter_kws={"alpha": 0.25},
            line_kws={"color": "red"},
            ax=axes[1]
        )
        axes[1].set_title("Engajamento × Ponto de virada")
        axes[1].set_xlim(0, 10)
        axes[1].set_ylim(0, 10)
        plt.tight_layout()
        return plt.gcf(), correlacoes_engajamento
#Graficos Pergunta 4
class dados_iaa:
    @staticmethod
    def grafico_iaa(dados):
        dados["Gap_IAA_IDA"] = dados["IAA"] - dados["IDA"]

        dados["Perfil_Autoavaliacao"] = pd.cut(
            dados["Gap_IAA_IDA"],
            bins=[-np.inf, -1, 1, np.inf],
            labels=["Subestima desempenho", "Coerente", "Superestima desempenho"]
        )
        autoavaliacao = (
            dados.groupby(["Ano", "Perfil_Autoavaliacao"], observed=False)
            .size()
            .groupby(level=0)
            .apply(lambda x: 100 * x / x.sum())
            .rename("Percentual")
        )
        autoavaliacao = autoavaliacao.droplevel(1)
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))

        sns.scatterplot(data=dados, x="IDA", y="IAA", hue="Ano", alpha=.4, ax=axes[0])
        axes[0].plot([0, 10], [0, 10], "--", color="black")
        axes[0].set_title("Autoavaliação versus desempenho real")
        axes[0].set_xlim(0, 10)
        axes[0].set_ylim(0, 10)

        sns.boxplot(data=dados, x="Ano", y="Gap_IAA_IDA", ax=axes[1])
        axes[1].axhline(0, ls="--", color="black")
        axes[1].set_title("Diferença IAA − IDA")
        axes[1].set_ylabel("Gap de autoavaliação")

        plt.tight_layout()
        return plt.gcf()
#Graficos Pergunta 5
class dados_ips:
    @staticmethod
    def criar_pares_longitudinais(df, ano_atual, ano_seguinte):
        atual = df[df["Ano"] == ano_atual].copy()
        seguinte = df[df["Ano"] == ano_seguinte].copy()

        pares = atual.merge(
            seguinte,
            on="RA",
            how="inner",
            suffixes=("_atual", "_seguinte")
        )

        pares["Delta_IDA"] = pares["IDA_seguinte"] - pares["IDA_atual"]
        pares["Delta_IEG"] = pares["IEG_seguinte"] - pares["IEG_atual"]
        pares["Queda_IDA"] = (pares["Delta_IDA"] < 0).astype(int)
        pares["Queda_IEG"] = (pares["Delta_IEG"] < 0).astype(int)
        pares["Transicao"] = f"{ano_atual} → {ano_seguinte}"

        return pares
    @staticmethod
    def df_ips(dados):
        pares_22_23 = dados_ips.criar_pares_longitudinais(dados, 2022, 2023)
        pares_23_24 = dados_ips.criar_pares_longitudinais(dados, 2023, 2024)
        pares_long = pd.concat([pares_22_23, pares_23_24], ignore_index=True)

        print("Pares longitudinais:", len(pares_long))
        pares_long["Faixa_IPS"] = pd.qcut(
            pares_long["IPS_atual"],
            q=4,
            duplicates="drop"
        )

        risco_ips = (
            pares_long.groupby("Faixa_IPS", observed=False)
            .agg(
                Alunos=("RA", "count"),
                Taxa_Queda_IDA=("Queda_IDA", "mean"),
                Taxa_Queda_IEG=("Queda_IEG", "mean"),
                Delta_IDA_Medio=("Delta_IDA", "mean"),
                Delta_IEG_Medio=("Delta_IEG", "mean")
            )
        )
        risco_ips[["Taxa_Queda_IDA", "Taxa_Queda_IEG"]] *= 100
        return risco_ips
#Graficos Pergunta 6
class dados_ipp_VS_ian:
    @staticmethod
    def ippVSian(dados):
        ipp_ian = dados.dropna(subset=["IPP", "IAN"]).copy()
        ordem_ian = ["Adequado", "Defasagem moderada", "Defasagem severa"]
        df_VS = (
            ipp_ian.groupby("Nivel_IAN")["IPP"]
            .agg(["count", "mean", "median", "std"])
            .reindex(ordem_ian)
        )

        plt.figure(figsize=(10, 5))
        sns.boxplot(data=ipp_ian, x="Nivel_IAN", y="IPP", order=ordem_ian)
        plt.title("Avaliação psicopedagógica por nível de adequação")
        plt.xlabel("Classificação IAN")
        plt.ylabel("IPP")
        plt.tight_layout()
        return plt.gcf(), df_VS
#ML e grafico Pergunta 7:
class dados_ipv:
    @staticmethod
    def ipv(dados):
        features_ipv = ["IDA", "IEG", "IAA", "IPS", "IPP", "IAN", "Idade", "Fase"]
        base_ipv = dados.dropna(subset=["IPV"]).copy()

        X_ipv = base_ipv[features_ipv]
        y_ipv = base_ipv["IPV"]

        num_ipv = X_ipv.select_dtypes(include=np.number).columns.tolist()
        cat_ipv = X_ipv.select_dtypes(exclude=np.number).columns.tolist()

        pre_ipv = ColumnTransformer([
            ("num", Pipeline([
                ("imputer", SimpleImputer(strategy="median"))
            ]), num_ipv),
            ("cat", Pipeline([
                ("imputer", SimpleImputer(strategy="most_frequent")),
                ("onehot", OneHotEncoder(handle_unknown="ignore"))
            ]), cat_ipv)
        ])

        from sklearn.ensemble import RandomForestRegressor
        from sklearn.metrics import mean_absolute_error, r2_score

        modelo_ipv = Pipeline([
            ("preprocessamento", pre_ipv),
            ("modelo", RandomForestRegressor(
                n_estimators=300,
                random_state=RANDOM_STATE,
                min_samples_leaf=5,
                n_jobs=-1
            ))
        ])

        X_train_ipv, X_test_ipv, y_train_ipv, y_test_ipv = train_test_split(
            X_ipv, y_ipv, test_size=.25, random_state=RANDOM_STATE
        )

        modelo_ipv.fit(X_train_ipv, y_train_ipv)
        pred_ipv = modelo_ipv.predict(X_test_ipv)

        perm_ipv = permutation_importance(
            modelo_ipv,
            X_test_ipv,
            y_test_ipv,
            n_repeats=10,
            random_state=RANDOM_STATE,
            scoring="r2"
        )

        importancia_ipv = pd.DataFrame({
            "Variavel": X_test_ipv.columns,
            "Importancia": perm_ipv.importances_mean
        }).sort_values("Importancia", ascending=False)
        plt.figure(figsize=(9, 5))
        sns.barplot(data=importancia_ipv, x="Importancia", y="Variavel")
        plt.title("Importância das variáveis para explicar o IPV")
        plt.xlabel("Queda média no R² após permutação")
        plt.ylabel("")
        plt.tight_layout()
        return plt.gcf()
#Graficos Pergunta 8
class dados_Muldidimensao:
    @staticmethod
    def indicador(dados):
        cols_corr = ["INDE", "IDA", "IEG", "IAA", "IPS", "IPP", "IPV", "IAN"]
        corr = dados[cols_corr].corr(method="spearman")
        sns.heatmap(corr, annot=True, fmt=".2f", cmap="RdBu_r", center=0)
        plt.title("Correlação entre indicadores")
        plt.tight_layout()
        base_multi = dados.dropna(subset=["INDE", "IDA", "IEG", "IPS", "IPP"]).copy()

        for col in ["IDA", "IEG", "IPS", "IPP"]:
            base_multi[f"{col}_Alto"] = (
                    base_multi[col] >= base_multi[col].median()
            ).map({True: "Alto", False: "Baixo"})
        combinacoes = (
            base_multi.groupby(
                ["IDA_Alto", "IEG_Alto", "IPS_Alto", "IPP_Alto"],
                observed=False
            )
            .agg(
                Alunos=("RA", "count"),
                INDE_Medio=("INDE", "mean")
            )
            .query("Alunos >= 10")
            .sort_values("INDE_Medio", ascending=False)
        )
        return plt.gcf(),combinacoes
#Graficos Pergunta 9
# Graficos Pergunta 9
class dados_risco:
    @staticmethod
    def _obter_caminho_dados(nome_arquivo):
        # Localiza a pasta do próprio arquivo graficos.py
        diretorio_atual = os.path.dirname(os.path.abspath(__file__))
        # Monta o caminho dinâmico para a pasta data/
        return os.path.join(diretorio_atual, "data", nome_arquivo)

    @staticmethod
    def comp_model():
        caminho = dados_risco._obter_caminho_dados("comparacao_modelos.csv")
        df = pd.read_csv(caminho)
        return df

    @staticmethod
    def imp_var():
        caminho = dados_risco._obter_caminho_dados("importancia_variaveis.csv")
        importancia = pd.read_csv(caminho)
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(
            data=importancia.head(15),
            x="Importancia_Media",
            y="Variavel",
            ax=ax
        )
        ax.set_title("Variáveis mais relevantes para prever risco")
        ax.set_xlabel("Redução média da ROC-AUC após permutação")
        ax.set_ylabel("")
        fig.tight_layout()
        return fig

    @staticmethod
    def st_prior():
        caminho = dados_risco._obter_caminho_dados("alunos_priorizados_teste.csv")
        df = pd.read_csv(caminho)
        return df.head(50)
#Graficos Pergunta 10
class dados_efetivo:
    @staticmethod
    def efetividade(dados):
        indicadores_programa = ["INDE", "IDA", "IEG", "IAA", "IPS", "IPP", "IPV", "IAN"]
        evolucao_programa = (
            dados.groupby("Ano")[indicadores_programa]
            .mean()
            .T
        )
        return evolucao_programa
    @staticmethod
    def variacao(dados):
        variacoes = []
        indicadores_programa = ["INDE", "IDA", "IEG", "IAA", "IPS", "IPP", "IPV", "IAN"]
        for a, b in [(2022, 2023), (2023, 2024)]:
            atual = dados[dados["Ano"] == a][["RA"] + indicadores_programa]
            futuro = dados[dados["Ano"] == b][["RA"] + indicadores_programa]

            pares = atual.merge(futuro, on="RA", suffixes=(f"_{a}", f"_{b}"))

            for indicador in indicadores_programa:
                delta = pares[f"{indicador}_{b}"] - pares[f"{indicador}_{a}"]

                variacoes.append({
                    "Transicao": f"{a} → {b}",
                    "Indicador": indicador,
                    "Alunos_com_dados": delta.notna().sum(),
                    "Variacao_media": delta.mean(),
                    "%_melhorou": (delta > 0).mean() * 100
                })
        variacoes_df = pd.DataFrame(variacoes)
        return variacoes_df
    @staticmethod
    def stone(dados):
        pedra_resumo = (
            dados.groupby(["Ano", "Pedra_Atual"])
            .agg(
                Alunos=("RA", "count"),
                INDE_Medio=("INDE", "mean"),
                IDA_Medio=("IDA", "mean"),
                IEG_Medio=("IEG", "mean"),
                IPV_Medio=("IPV", "mean"),
                Defasagem_Media=("Defasagem", "mean")
            )
            .reset_index()
        )
        return pedra_resumo