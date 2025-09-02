"""
Modelos Django para SGR
Modelos existentes - NÃO criar migrações (tabelas já existem no banco)
"""
from django.db import models


# Modelo de referência - precisa ser definido ou importado
class PessoaTipos(models.Model):
    """Modelo para tipos de pessoa - manter se usado"""

    nome = models.CharField(max_length=100)

    class Meta:
        db_table = "PessoaTipos"
        managed = False  # Django não gerencia esta tabela

    def __str__(self):
        return self.nome


class Clientes(models.Model):
    TIPO_PESSOA_CHOICES = [
        ("PF", "Física"),
        ("PJ", "Jurídica"),
    ]

    SEXO_CHOICES = [
        ("M", "Masculino"),
        ("F", "Feminino"),
    ]

    class Meta:
        db_table = "Clientes"
        managed = False  # Django não gerencia esta tabela
        ordering = [
            "RazaoSocial",
        ]

        verbose_name = "Clientes"
        verbose_name_plural = "Clientes"

    id = models.AutoField(primary_key=True)
    ID_Gestao = models.CharField(max_length=10)
    TipoPessoa = models.CharField(
        max_length=2, choices=TIPO_PESSOA_CHOICES, default="PF"
    )

    PessoaTipo = models.ForeignKey(
        PessoaTipos,
        on_delete=models.CASCADE,
        related_name="tipopessoa_cliente",
        verbose_name=("Pessoa Tipo"),
        null=True,
    )

    Nome = models.CharField(max_length=100, blank=True, null=True)
    RazaoSocial = models.CharField(max_length=100, blank=True, null=True)
    CNPJ = models.CharField(max_length=30, blank=True, null=True)
    InscricaoEstadual = models.CharField(max_length=30, blank=True, null=True)
    InscricaoMunicipal = models.CharField(max_length=30, blank=True, null=True)
    Responsavel = models.CharField(max_length=100, blank=True, null=True)
    CPF = models.CharField(max_length=30, blank=True, null=True)
    RG = models.CharField(max_length=30, blank=True, null=True)
    DataNascimento = models.DateField(
        verbose_name="Data Nascimento", blank=True, null=True
    )
    Sexo = models.CharField(max_length=1, choices=SEXO_CHOICES, default="M")
    Email = models.CharField(max_length=100, blank=True, null=True)
    Ativo = models.CharField(max_length=1, blank=True, null=True)
    NomeVendedor = models.CharField(max_length=100, blank=True, null=True)
    DataCadastro = models.DateField(verbose_name="Data Cadastro", blank=True, null=True)

    def __str__(self):
        return f"{self.RazaoSocial} - {self.CNPJ}"


class Bancos(models.Model):
    class Meta:
        db_table = "Bancos"
        managed = False  # Django não gerencia esta tabela
        ordering = [
            "descricao",
        ]
        verbose_name = "Banco"

    descricao = models.CharField(max_length=255)
    codigo_instituicao = models.CharField(max_length=20)

    def __str__(self):
        return self.descricao


class CentroCustos(models.Model):
    class Meta:
        db_table = "CentroCustos"
        managed = False  # Django não gerencia esta tabela
        ordering = [
            "descricao",
        ]
        verbose_name = "Centro Custo"

    descricao = models.CharField(max_length=255)

    def __str__(self):
        return self.descricao


class Empresas(models.Model):
    class Meta:
        db_table = "Empresas"
        managed = False  # Django não gerencia esta tabela
        ordering = [
            "nome",
        ]
        verbose_name = "Empresa"

    nome = models.CharField(max_length=250)
    cnpj = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return f"{self.nome} - {self.cnpj}"


class Extratos(models.Model):
    class Meta:
        db_table = "Extratos"
        managed = False  # Django não gerencia esta tabela
        ordering = ["banco", "-data"]
        verbose_name = "Extrato"

    banco = models.ForeignKey(Bancos, on_delete=models.CASCADE)
    agencia = models.CharField(max_length=255)
    conta_corrente = models.CharField(max_length=255)
    data = models.DateField(null=True, blank=True)
    agencia_origem = models.CharField(max_length=255)
    lote = models.CharField(max_length=255)
    documento = models.CharField(max_length=255)
    historico_codigo = models.CharField(max_length=255)
    historico_descricao = models.CharField(max_length=255)
    valor = models.CharField(max_length=255)  # Use CharField se for manter como string
    debito_credito = models.CharField(max_length=1, null=True, blank=True)
    descricao = models.CharField(max_length=255)
    centrocusto = models.ForeignKey(
        CentroCustos,
        on_delete=models.PROTECT,
        related_name="extratos",
        verbose_name="Centro Custo",
        null=True,
        blank=True,
        default=0,
    )
    empresa = models.ForeignKey(
        Empresas,
        on_delete=models.PROTECT,
        verbose_name="Empresa",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.banco} - {self.data} - {self.historico_descricao} - {self.valor}"


class Produtos(models.Model):
    class Meta:
        db_table = "Produtos"
        managed = False  # Django não gerencia esta tabela
        ordering = [
            "Nome",
        ]
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"

    ID_Gestao = models.CharField(max_length=100, blank=False, null=False)
    ID_Loja = models.CharField(max_length=10)
    Nome = models.CharField(max_length=200, blank=False, null=False)
    Descricao = models.CharField(max_length=200, blank=False, null=False)
    CodigoInterno = models.CharField(max_length=100, blank=True, null=True)
    CodigoBarra = models.CharField(max_length=100, blank=True, null=True)
    PossuiVariacao = models.CharField(max_length=10, blank=True, null=True)
    PossuiComposicao = models.CharField(max_length=10, blank=True, null=True)
    MovimentaEstoque = models.CharField(max_length=10, blank=True, null=True)
    Peso = models.CharField(max_length=10, blank=True, null=True)
    Largura = models.CharField(max_length=10, blank=True, null=True)
    Altura = models.CharField(max_length=10, blank=True, null=True)
    Comprimento = models.CharField(max_length=10, blank=True, null=True)
    Ativo = models.CharField(max_length=10, blank=True, null=True)
    ID_Grupo = models.CharField(max_length=10)
    NomeGrupo = models.CharField(max_length=100, blank=True, null=True)
    Estoque = models.CharField(max_length=10, blank=True, null=True)
    ValorCusto = models.CharField(max_length=10, blank=True, null=True)
    ValorVenda = models.CharField(max_length=10, blank=True, null=True)
    LucroUtilizado = models.CharField(max_length=10, blank=True, null=True)
    CodigoExpedicao = models.CharField(max_length=100, blank=True, null=True)
    EstoqueGalpao = models.CharField(max_length=10, blank=True, null=True, default="0")
    EstoqueSeparado = models.CharField(
        max_length=10, blank=True, null=True, default="0"
    )
    EstoqueMovimentado = models.CharField(
        max_length=10, blank=True, null=True, default="0"
    )
    Localizacao = models.CharField(max_length=20, blank=True, null=True)
    Foto = models.ImageField(upload_to="estoque/", blank=True, null=True)
    QrCode = models.BooleanField(
        verbose_name="QR Code Gerado", default=False, null=True, blank=True
    )

    @property
    def EstoqueDisponivel(self):
        """
        Calcula o estoque disponível como:
        EstoqueGalpao - (EstoqueSeparado + EstoqueMovimentado)
        """
        try:
            estoque_galpao = int(self.EstoqueGalpao) if self.EstoqueGalpao else 0
            estoque_separado = int(self.EstoqueSeparado) if self.EstoqueSeparado else 0
            estoque_movimentado = (
                int(self.EstoqueMovimentado) if self.EstoqueMovimentado else 0
            )

            disponivel = estoque_galpao - (estoque_separado + estoque_movimentado)
            return max(disponivel, 0)  # Retorna 0 se o valor for negativo
        except (ValueError, TypeError):
            return 0  # Retorna 0 em caso de erro na conversão

    def __str__(self):
        return self.Nome  # nome do Campo a ser exibido


class BoletosEnviados(models.Model):
    class Meta:
        db_table = "BoletosEnviados"
        managed = False  # Django não gerencia esta tabela
        ordering = ["-DataHoraEnvio"]
        verbose_name = "Boleto Enviado"

    id = models.AutoField(primary_key=True)
    Nome = models.CharField(max_length=250)
    Boleto = models.CharField(max_length=250)
    Vencimento = models.DateField(verbose_name="Data Vencimento")
    Importacao = models.DateField(null=True, blank=True, verbose_name="Data Importação")
    DataHoraEnvio = models.DateTimeField(verbose_name="Data Hora Envio")

    # Definindo as opções de status
    STATUS_CHOICES = [
        ("Enviado", "Enviado"),
        ("Errado", "Errado"),
        ("Sem Contato", "Sem Contato"),
    ]

    STATUS_MAPPING = {
        "1": {"label": "Enviado", "class": "text-success"},
        "2": {"label": "Errado", "class": "text-danger"},
        "3": {"label": "Sem Contato", "class": "text-secondary"},
    }

    def get_status_class(self):
        for key, value in self.STATUS_MAPPING.items():
            if value["label"] == self.Status:
                return value["class"]
        return ""

    # Aplicando as opções ao campo Status
    Status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, verbose_name="Status"
    )

    def __str__(self):
        return f"{self.Boleto} - {self.Vencimento}"
