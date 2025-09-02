#!/usr/bin/env python3
"""
Script de formatação rápida - foca apenas no essencial
"""
import subprocess

from rich.console import Console
from rich.panel import Panel

console = Console()


def run_command_simple(command: str, description: str) -> bool:
    """Executa comando de forma simples"""
    console.print(f"\n[yellow]🔧 {description}[/yellow]")
    try:
        result = subprocess.run(
            command.split(), check=True, capture_output=True, text=True
        )
        console.print(f"[green]✅ {description} - OK![/green]")
        return True
    except subprocess.CalledProcessError as e:
        console.print(f"[red]❌ {description} - Erro![/red]")
        if e.stderr:
            # Mostrar apenas primeira linha do erro
            first_error = e.stderr.split("\n")[0]
            console.print(f"[dim]{first_error}[/dim]")
        return False


def main():
    console.print(
        Panel.fit(
            "[bold]⚡ Formatação Rápida[/bold]\n"
            "[dim]Formatação essencial sem verificações rigorosas[/dim]",
            border_style="green",
        )
    )

    # Formatação básica
    black_ok = run_command_simple(
        "python -m black . --line-length=88", "Formatando código com Black"
    )

    isort_ok = run_command_simple(
        "python -m isort . --profile black", "Organizando imports com Isort"
    )

    # Verificação básica apenas nos arquivos principais
    mypy_ok = run_command_simple(
        "python -m mypy app.py --ignore-missing-imports",
        "Verificação básica do arquivo principal",
    )

    # Resumo
    console.print(f"\n[bold]📊 Resultado:[/bold]")
    console.print(f"• Black: {'✅' if black_ok else '❌'}")
    console.print(f"• Isort: {'✅' if isort_ok else '❌'}")
    console.print(f"• Mypy: {'✅' if mypy_ok else '⚠️'}")

    if black_ok and isort_ok:
        console.print(f"\n[green]🎉 Formatação concluída com sucesso![/green]")
    else:
        console.print(f"\n[yellow]⚠️  Alguns problemas encontrados[/yellow]")


if __name__ == "__main__":
    main()
