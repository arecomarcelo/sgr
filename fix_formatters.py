#!/usr/bin/env python3
"""
Script para corrigir dependências do formatador de código
"""
import subprocess
import sys
from pathlib import Path

from rich.console import Console
from rich.panel import Panel

console = Console()


def run_pip_command(command: str, description: str) -> bool:
    """Executa comando pip com feedback visual"""
    console.print(f"\n[yellow]📦 {description}[/yellow]")
    console.print(f"[dim]Executando: {command}[/dim]")

    try:
        result = subprocess.run(
            command.split(), check=True, capture_output=True, text=True
        )
        console.print(f"[green]✅ {description} - Sucesso![/green]")
        return True
    except subprocess.CalledProcessError as e:
        console.print(f"[red]❌ {description} - Erro![/red]")
        console.print(f"[red]{e.stderr}[/red]")
        return False


def main():
    console.print(
        Panel.fit(
            "[bold]🔧 Correção de Dependências do Formatador[/bold]\n"
            "[dim]Corrigindo incompatibilidades de versão[/dim]",
            border_style="blue",
        )
    )

    # 1. Atualizar pip
    run_pip_command("pip install --upgrade pip", "Atualizando pip")

    # 2. Corrigir Black e Click
    console.print("\n[bold]📋 Corrigindo Black e Click...[/bold]")
    run_pip_command("pip uninstall -y black click", "Removendo versões conflitantes")
    run_pip_command("pip install black==23.12.1", "Instalando Black compatível")

    # 3. Instalar plugin Django para Mypy
    console.print("\n[bold]📋 Configurando Mypy para Django...[/bold]")
    run_pip_command(
        "pip install django-stubs mypy-extensions", "Instalando plugins Django"
    )

    # 4. Instalar outras ferramentas de qualidade
    console.print("\n[bold]📋 Instalando ferramentas adicionais...[/bold]")
    run_pip_command("pip install flake8 autopep8", "Instalando ferramentas de linting")

    console.print(
        Panel.fit(
            "[green]✅ Correções aplicadas![/green]\n"
            "[dim]Agora você pode executar o formata.py novamente[/dim]",
            border_style="green",
        )
    )

    console.print("\n[bold]🚀 Para testar:[/bold]")
    console.print("[cyan]python formata.py[/cyan]")


if __name__ == "__main__":
    main()
