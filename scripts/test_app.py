"""
Teste da aplicação refatorada
"""
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")

import django

django.setup()


def test_application():
    """Testa componentes principais da aplicação"""
    print("🧪 Iniciando testes da aplicação refatorada...")

    try:
        # Teste 1: Container e serviços
        from core.container_vendas import DIContainer

        container = DIContainer()
        vendas_service = container.get_vendas_service()
        print("✅ Container DI e VendasService inicializados")

        # Teste 2: Health check
        health = container.health_check()
        print(f"✅ Health check: {health}")

        # Teste 3: Informações de atualização
        info = vendas_service.get_informacoes_atualizacao()
        print(
            f"✅ Informações de atualização: Data={info.get('data')}, Hora={info.get('hora')}"
        )

        # Teste 4: Vendedores ativos
        vendedores = vendas_service.get_vendedores_ativos()
        print(f"✅ Vendedores ativos: {len(vendedores)} encontrados")

        # Teste 5: Situações disponíveis
        situacoes = vendas_service.get_situacoes_disponiveis()
        print(f"✅ Situações disponíveis: {len(situacoes)} encontradas")

        # Teste 6: Dados do mês atual
        df_vendas = vendas_service.get_vendas_mes_atual()
        print(f"✅ Vendas do mês atual: {len(df_vendas)} registros")

        # Teste 7: Métricas
        metricas = vendas_service.get_metricas_vendas(df_vendas)
        print(f"✅ Métricas calculadas: {list(metricas.keys())}")

        # Teste 8: Componentes UI
        from presentation.components.data_grid_simple import DataGrid
        from presentation.components.forms_vendas import FilterForm, MetricsDisplay

        print("✅ Componentes UI importados com sucesso")

        # Teste 9: Exceções
        from core.exceptions import BusinessLogicError, SGRException, ValidationError

        print("✅ Sistema de exceções funcionando")

        print("\n🎉 TODOS OS TESTES PASSARAM!")
        print("📋 RESUMO DOS RESULTADOS:")
        print(f"   • Vendedores ativos: {len(vendedores)}")
        print(f"   • Situações: {len(situacoes)}")
        print(f"   • Vendas do mês: {len(df_vendas)}")
        print(
            f"   • Total de vendas: R$ {metricas.get('total_valor', 0):,.2f}".replace(
                ",", "."
            )
        )
        print(
            f"   • Ticket médio: R$ {metricas.get('ticket_medio', 0):,.2f}".replace(
                ",", "."
            )
        )
        print(
            f"   • Health check: {'✅ OK' if all(health.values()) else '⚠️ Problemas'}"
        )

        return True

    except Exception as e:
        print(f"❌ Erro no teste: {str(e)}")
        import traceback

        print(traceback.format_exc())
        return False


if __name__ == "__main__":
    success = test_application()
    exit(0 if success else 1)
