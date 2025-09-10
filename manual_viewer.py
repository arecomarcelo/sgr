import os

import streamlit as st


def convert_markdown_to_html(markdown_content):
    """
    Converte markdown para HTML com tema dark
    """
    try:
        import markdown

        html = markdown.markdown(
            markdown_content, extensions=['tables', 'fenced_code', 'toc']
        )
    except ImportError:
        # Fallback básico se não tiver a biblioteca
        html = basic_markdown_to_html(markdown_content)

    return f'<div class="manual-container">{html}</div>'


def basic_markdown_to_html(content):
    """
    Conversão básica de markdown para HTML
    """
    import re

    # Títulos
    content = re.sub(r'^# (.*)', r'<h1>\1</h1>', content, flags=re.MULTILINE)
    content = re.sub(r'^## (.*)', r'<h2>\1</h2>', content, flags=re.MULTILINE)
    content = re.sub(r'^### (.*)', r'<h3>\1</h3>', content, flags=re.MULTILINE)
    content = re.sub(r'^#### (.*)', r'<h4>\1</h4>', content, flags=re.MULTILINE)

    # Negrito e itálico
    content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', content)
    content = re.sub(r'\*(.*?)\*', r'<em>\1</em>', content)

    # Código inline
    content = re.sub(r'`(.*?)`', r'<code>\1</code>', content)

    # Links
    content = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', content)

    # Separadores
    content = re.sub(r'^---$', '<hr>', content, flags=re.MULTILINE)

    # Quebras de linha
    content = content.replace('\n\n', '</p><p>').replace('\n', '<br>')
    content = f'<p>{content}</p>'

    return content


def show_manual_in_dialog():
    """
    Exibe o manual em um dialog/modal do Streamlit
    Funciona tanto local quanto no deploy
    """
    try:
        # Ler o conteúdo do manual
        manual_path = "documentacao/Manual_Relatorio_Vendas.md"

        with open(manual_path, "r", encoding="utf-8") as file:
            markdown_content = file.read()

        # Usar expander expandido como "modal"
        with st.expander("📖 Manual do Relatório de Vendas", expanded=True):
            # CSS para tema dark no modal
            st.markdown(
                """
            <style>
                .manual-container {
                    background-color: #1e1e1e;
                    color: #ffffff;
                    padding: 20px;
                    border-radius: 10px;
                    border: 1px solid #404040;
                    max-height: 70vh;
                    overflow-y: auto;
                    font-family: 'Roboto', Arial, sans-serif;
                    line-height: 1.6;
                }
                
                .manual-container h1 {
                    color: #1E88E5;
                    border-bottom: 2px solid #1E88E5;
                    padding-bottom: 8px;
                    margin-bottom: 20px;
                }
                
                .manual-container h2 {
                    color: #1976D2;
                    border-left: 3px solid #1976D2;
                    padding-left: 12px;
                    margin-top: 25px;
                    margin-bottom: 15px;
                }
                
                .manual-container h3 {
                    color: #1565C0;
                    margin-top: 20px;
                    margin-bottom: 10px;
                }
                
                .manual-container h4 {
                    color: #1E88E5;
                    margin-top: 15px;
                    margin-bottom: 8px;
                }
                
                .manual-container table {
                    width: 100%;
                    border-collapse: collapse;
                    margin: 15px 0;
                    background: #2d2d2d;
                    border-radius: 6px;
                    overflow: hidden;
                }
                
                .manual-container th {
                    background: #1E88E5;
                    color: white;
                    padding: 10px;
                    text-align: left;
                    font-weight: 600;
                }
                
                .manual-container td {
                    padding: 10px;
                    border-bottom: 1px solid #404040;
                    color: #b0b0b0;
                }
                
                .manual-container tr:hover td {
                    background: rgba(30, 136, 229, 0.1);
                    color: #ffffff;
                }
                
                .manual-container code {
                    background: #2d2d2d;
                    color: #ff6b6b;
                    padding: 2px 6px;
                    border-radius: 4px;
                    font-family: 'Courier New', monospace;
                    border: 1px solid #404040;
                }
                
                .manual-container strong {
                    color: #1E88E5;
                    font-weight: 600;
                }
                
                .manual-container em {
                    color: #1565C0;
                }
                
                .manual-container blockquote {
                    border-left: 3px solid #1E88E5;
                    background: rgba(30, 136, 229, 0.1);
                    padding: 10px 15px;
                    margin: 15px 0;
                    border-radius: 0 6px 6px 0;
                }
                
                .manual-container ul, .manual-container ol {
                    padding-left: 20px;
                    margin: 10px 0;
                }
                
                .manual-container li {
                    margin: 5px 0;
                    color: #b0b0b0;
                }
                
                .manual-container hr {
                    border: none;
                    height: 1px;
                    background: linear-gradient(to right, transparent, #1E88E5, transparent);
                    margin: 20px 0;
                }
                
                /* Scrollbar customizada */
                .manual-container::-webkit-scrollbar {
                    width: 8px;
                }
                
                .manual-container::-webkit-scrollbar-track {
                    background: #1e1e1e;
                }
                
                .manual-container::-webkit-scrollbar-thumb {
                    background: #1E88E5;
                    border-radius: 4px;
                }
                
                .manual-container::-webkit-scrollbar-thumb:hover {
                    background: #1976D2;
                }
            </style>
            """,
                unsafe_allow_html=True,
            )

            # Espaçamento
            st.markdown("")

            # Converter markdown para HTML e exibir
            html_content = convert_markdown_to_html(markdown_content)
            st.markdown(html_content, unsafe_allow_html=True)

            # Botões de ação
            col1, col2, col3 = st.columns([1, 1, 2])

            with col1:
                # Botão de download
                st.download_button(
                    label="📥 Download Manual",
                    data=markdown_content,
                    file_name="Manual_Relatorio_Vendas.md",
                    mime="text/markdown",
                    use_container_width=True,
                )

            with col2:
                if st.button("❌ Fechar", use_container_width=True):
                    st.session_state["show_manual"] = False
                    st.rerun()

    except FileNotFoundError:
        st.error("❌ Manual não encontrado. Verifique se o arquivo existe.")
    except Exception as e:
        st.error(f"❌ Erro ao carregar o manual: {str(e)}")


def show_manual_button():
    """
    Renderiza o botão do manual que funciona em qualquer ambiente
    """
    if st.button("📖 Ler Manual", type="secondary", use_container_width=True):
        st.session_state["show_manual"] = True
        st.rerun()


def render_manual_if_requested():
    """
    Verifica se o manual foi solicitado e o exibe
    """
    if st.session_state.get("show_manual", False):
        st.markdown("---")
        show_manual_in_dialog()
