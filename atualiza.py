"""
Script para atualizar a biblioteca streamlit-aggrid e suas dependências
"""
import subprocess
import sys
import os

def atualizar_ambiente():
    """
    Atualiza o ambiente virtual com as versões corretas das bibliotecas
    necessárias para o funcionamento do AgGrid com Streamlit.
    
    Retorna:
        bool: True se a atualização foi bem-sucedida, False caso contrário
    """
    try:
        print("Verificando ambiente virtual...")
        venv_path = os.path.dirname(os.path.dirname(sys.executable))
        print(f"Ambiente virtual detectado em: {venv_path}")
        
        print("\n1. Atualizando pip...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        
        print("\n2. Desinstalando a versão atual do streamlit-aggrid...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "uninstall", "-y", "streamlit-aggrid"])
        except subprocess.CalledProcessError:
            print("streamlit-aggrid não estava instalado ou houve erro na desinstalação.")
        
        print("\n3. Instalando versão compatível do streamlit...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "streamlit>=1.28.0,<1.30.0"])
        
        print("\n4. Instalando versão compatível do streamlit-aggrid...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit-aggrid==0.3.4"])
        
        print("\n5. Verificando instalação...")
        installed_packages = subprocess.check_output([sys.executable, "-m", "pip", "freeze"])
        installed_packages = installed_packages.decode("utf-8").split("\n")
        
        streamlit_version = next((p for p in installed_packages if p.startswith("streamlit==")), "streamlit não encontrado")
        aggrid_version = next((p for p in installed_packages if p.startswith("streamlit-aggrid==")), "streamlit-aggrid não encontrado")
        
        print(f"\nVersões instaladas:\n{streamlit_version}\n{aggrid_version}")
        
        print("\nAtualização concluída com sucesso!")
        print("Por favor, reinicie o servidor Streamlit para aplicar as alterações.")
        return True
        
    except Exception as e:
        print(f"\nErro durante a atualização: {str(e)}")
        return False

if __name__ == "__main__":
    print("Iniciando atualização do ambiente...")
    atualizar_ambiente()