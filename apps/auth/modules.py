# modules_improved_v1.py - Menu com Cards e Ícones
import streamlit as st
from utils.style_utils import apply_default_style


def menu():
    """Menu moderno com cards e ícones na sidebar"""
    apply_default_style()
    
    # CSS customizado para o menu com sidebar mínima
    st.markdown("""
    <style>
    /* Sidebar com largura mínima */
    .css-1d391kg {
        width: 280px !important;
        min-width: 280px !important;
        max-width: 280px !important;
    }
    
    .menu-card {
        background: linear-gradient(135deg, #1E88E5 0%, #1565C0 100%);
        border-radius: 10px;
        padding: 12px;
        margin: 8px 0;
        color: white;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(30, 136, 229, 0.3);
    }
    
    .menu-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 16px rgba(30, 136, 229, 0.4);
        background: linear-gradient(135deg, #1976D2 0%, #1E88E5 100%);
    }
    
    .menu-card-selected {
        background: linear-gradient(135deg, #43A047 0%, #388E3C 100%);
        transform: translateY(-1px);
        box-shadow: 0 3px 12px rgba(67, 160, 71, 0.4);
    }
    
    .menu-icon {
        font-size: 20px;
        margin-bottom: 6px;
        display: block;
    }
    
    .menu-title {
        font-size: 13px;
        font-weight: 600;
        margin: 0;
        line-height: 1.2;
    }
    
    .logout-card {
        background: linear-gradient(135deg, #E53935 0%, #C62828 100%);
    }
    
    .logout-card:hover {
        background: linear-gradient(135deg, #F44336 0%, #E53935 100%);
    }
    
    /* Compactar ainda mais a sidebar */
    .block-container {
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.sidebar.markdown("""
    <div style='text-align: center; margin-bottom: 25px; background: linear-gradient(135deg, #1E88E5 0%, #1976D2 100%); padding: 20px; border-radius: 15px; box-shadow: 0 4px 12px rgba(30, 136, 229, 0.3);'>
        <h3 style='color: white; margin: 0; font-size: 26px; font-weight: bold;'>🏢 SGR</h3>
        <p style='color: white; font-size: 11px; margin: 5px 0 0 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; font-weight: 500; text-shadow: 1px 1px 2px rgba(0,0,0,0.1);'>
            Sistema de Gestão de Relatórios
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Definindo os módulos com nomes atualizados
    module_config = {
        "Dashboard Produtos": {
            "permission": "view_produtos",
            "icon": "📦",
            "original_name": "Estoque"
        },
        "Dashboard Boletos": {
            "permission": "view_boletos", 
            "icon": "💰",
            "original_name": "Cobrança"
        },
        "Dashboard Extratos": {
            "permission": "view_extratos",
            "icon": "💳", 
            "original_name": "Financeiro"
        },
        "Dashboard Vendas": {
            "permission": "view_venda",
            "icon": "📊",
            "original_name": "Relatório de Vendas"
        },
        "Dashboard Clientes": {
            "permission": "view_clientes",
            "icon": "👥",
            "original_name": "Relatório de Clientes"
        }
    }

    # Verificar módulos disponíveis
    available_modules = []
    for module, config in module_config.items():
        if (config["permission"] in st.session_state.permissions or 
            st.session_state.username == "admin"):
            available_modules.append(module)

    # Renderizar cards dos módulos
    selected_module = None
    current_module = st.session_state.get("current_module", "")
    
    for module in available_modules:
        config = module_config[module]
        
        # Determinar se está selecionado (comparar com nome original)
        is_selected = current_module == config["original_name"]
        
        # Criar container clicável
        with st.sidebar.container():
            clicked = st.button(
                f"{config['icon']}\n{module}", 
                key=f"menu_{module}",
                help=f"Acessar {module}",
                use_container_width=True,
                type="primary" if is_selected else "secondary"
            )
            
            if clicked:
                # Retornar o nome original para compatibilidade com app.py
                selected_module = config["original_name"]
                st.session_state.current_module = config["original_name"]
                st.rerun()

    # Separador
    st.sidebar.markdown("---")
    
    # Informações do usuário (mais compactas)
    st.sidebar.markdown(f"""
    <div style='
        background: #F5F5F5; 
        border-radius: 8px; 
        padding: 10px; 
        text-align: center;
        margin: 15px 0;
    '>
        <div style='color: #1E88E5; font-weight: 600; font-size: 14px;'>👤 {st.session_state.username}</div>
        <div style='color: #666; font-size: 11px;'>Conectado</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Botão de logout compacto
    if st.sidebar.button("🚪 Sair", key="logout", use_container_width=True, type="secondary"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.current_module = None
        st.success("Você saiu com sucesso.")
        st.rerun()

    return selected_module if selected_module else current_module