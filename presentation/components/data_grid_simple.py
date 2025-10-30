"""
Componente simples de grid de dados para vendas
"""

import io
from datetime import datetime
from typing import Any, Dict, Optional

import pandas as pd
import streamlit as st


class DataGrid:
    """Componente simples de grid de dados"""

    def render_data_grid(
        self,
        df: pd.DataFrame,
        title: str = "Dados",
        show_download: bool = True,
        filename_prefix: str = "dados",
    ) -> None:
        """
        Renderiza grid de dados com opções de download

        Args:
            df: DataFrame com os dados
            title: Título da seção
            show_download: Mostrar botão de download
            filename_prefix: Prefixo do arquivo de download
        """
        if df.empty:
            st.info("Nenhum dado disponível")
            return

        st.subheader(title)

        # Mostrar informações do dataset
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total de Registros", len(df))
        with col2:
            st.metric("Colunas", len(df.columns))

        # Exibir dataframe
        st.dataframe(df, height=400, use_container_width=True)

        # Botão de download
        if show_download:
            self._render_download_section(df, filename_prefix)

    def _render_download_section(self, df: pd.DataFrame, filename_prefix: str):
        """Renderiza seção de download"""
        st.subheader("📥 Download dos Dados")

        col1, col2 = st.columns(2)

        with col1:
            # Download CSV
            csv_data = df.to_csv(index=False)
            st.download_button(
                label="📄 Download CSV",
                data=csv_data,
                file_name=f"{filename_prefix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True,
            )

        with col2:
            # Download Excel
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
                df.to_excel(writer, index=False, sheet_name="Dados")

            st.download_button(
                label="📊 Download Excel",
                data=buffer.getvalue(),
                file_name=f"{filename_prefix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.ms-excel",
                use_container_width=True,
            )


class SimpleTable:
    """Componente de tabela simples"""

    @staticmethod
    def render_metrics_table(metrics: Dict[str, Any]) -> None:
        """Renderiza tabela de métricas"""
        if not metrics:
            st.info("Nenhuma métrica disponível")
            return

        # Converter para DataFrame
        data = []
        for key, value in metrics.items():
            data.append({"Métrica": key.replace("_", " ").title(), "Valor": value})

        df = pd.DataFrame(data)
        st.table(df)

    @staticmethod
    def render_summary_table(df: pd.DataFrame, group_by: str, value_col: str) -> None:
        """Renderiza tabela resumo"""
        if df.empty:
            st.info("Nenhum dado para resumo")
            return

        # Criar resumo
        summary = (
            df.groupby(group_by)[value_col]
            .agg(["count", "sum", "mean", "min", "max"])
            .round(2)
        )

        summary.columns = ["Quantidade", "Total", "Média", "Mínimo", "Máximo"]

        st.subheader(f"Resumo por {group_by}")
        st.dataframe(summary, use_container_width=True)
