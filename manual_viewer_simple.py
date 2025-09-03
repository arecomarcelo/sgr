import streamlit as st
import os

def show_manual():
    """Exibe o manual usando apenas recursos nativos do Streamlit"""
    
    # CSS para tema dark
    st.markdown("""
    <style>
        .stExpander {
            background-color: #1e1e1e !important;
            border: 1px solid #404040 !important;
        }
        .stExpander > div {
            background-color: #1e1e1e !important;
        }
        .stMarkdown {
            color: #ffffff !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    try:
        # Ler arquivo do manual
        manual_path = "documentacao/Manual_Relatorio_Vendas.md"
        with open(manual_path, "r", encoding="utf-8") as file:
            content = file.read()
        
        # Usar expander como modal
        with st.expander("📖 Manual do Relatório de Vendas - Clique para expandir/recolher", expanded=True):
            # Usar st.markdown direto com o conteúdo
            st.markdown(content)
            
            # Botões de ação
            col1, col2, col3 = st.columns([1, 1, 2])
            
            with col1:
                st.download_button(
                    label="📥 Download Manual",
                    data=content,
                    file_name="Manual_Relatorio_Vendas.md",
                    mime="text/markdown",
                    key="download_manual"
                )
            
            with col2:
                if st.button("❌ Fechar Manual", key="close_manual"):
                    st.session_state["show_manual"] = False
                    st.rerun()
                    
    except FileNotFoundError:
        st.error("❌ Arquivo do manual não encontrado.")
    except Exception as e:
        st.error(f"❌ Erro ao carregar manual: {str(e)}")

def render_manual_if_requested():
    """Renderiza o manual se foi solicitado"""
    if st.session_state.get("show_manual", False):
        st.markdown("---")
        show_manual()