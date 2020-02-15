import datetime, urllib.parse, typing
from requests_html import HTMLSession
from E_Sic.pedidos_respostas.conts import _SEARCH_REQUEST_PROTOCOL


"""
    http://www.consultaesic.cgu.gov.br/arquivosRelatorios/PedidosRespostas/Dicionario-Dados-Exportacao.txt
"""


class Pedido(dict):
    _direct_url = None

    @property
    def id_pedido(self) -> int:
        """
        :return: identificador único do recurso (não mostrado no sistema);
        :rtype: inteiro
        """
        return int(self.get("IdPedido", "0"))

    @property
    def protocolo_pedido(self) -> str:
        """
        :return: número do protocolo do pedido
        :rtype: text(17):
        """
        return self.get("ProtocoloPedido", "")

    @property
    def orgao_superior_associado_ao_destinatario(self) -> str:
        """
        :return: Quando o órgão for vinculado, este campo traz o nome do seu órgão superior
        :rtype: text(250)
        """
        return self.get("OrgaoSuperiorAssociadoaoDestinatario", "")

    @property
    def orgao_destinatario(self) -> str:
        """
        :return: nome do órgão destinatário do pedido
        :rtype: text(250)
        """
        return self.get("OrgaoDestinatario", "")

    @property
    def situacao(self) -> str:
        """
        :return: descrição da situação do pedido
        :rtype: text(200)
        """
        return self.get("Situacao", "")

    @property
    def data_registro(self) -> datetime.datetime:
        """
        :return: data de abertura do pedido
        :rtype: Date DD/MM/AAAA HH:MM:SS
        """
        return datetime.datetime.strptime(self.get("DataRegistro", ""), '%d/%m/%Y %H:%M:%S')

    @property
    def resumo_solicitacao(self) -> str:
        """
        :return: resumo do pedido
        :rtype: text(255)
        """
        return self.get("ResumoSolicitacao", "")

    @property
    def detalhamento_solicitacao(self) -> str:
        """
        :return: detalhamento do pedido
        :rtype: text(2048)
        """
        return self.get("DetalhamentoSolicitacao", "")

    @property
    def prazo_atendimento(self) -> datetime.datetime:
        """
        :return: data limite para atendimento ao pedido
        :rtype: Date DD/MM/AAAA HH:MM:ss
        """
        return datetime.datetime.strptime(self.get("PrazoAtendimento", ""), '%d/%m/%Y %H:%M:%S')

    @property
    def foi_prorrogado(self) -> bool:
        """
        :return: "Sim" ou "Não" : informa se houve prorrogação do prazo do pedido;
        :rtype: bool
        """
        return self.get("FoiProrrogado", "") == "SIM"

    @property
    def foi_reencaminhado(self) -> bool:
        """
        :return: "Sim" ou "Não": informa se o pedido foi reencaminhado
        :rtype: bool
        """
        return self.get("FoiReencaminhado", "") == "SIM"

    @property
    def forma_resposta(self) -> str:
        """
        :return: tipo de resposta escolhida pelo solicitante na abertura do pedido
        :rtype: text(200)
        """
        return self.get("FormaResposta", "")

    @property
    def origem_solicitacao(self) -> str:
        """
        :return: informa se o pedido foi aberto em um Balcão SIC ou pela Internet
        :rtype: text(50)
        """
        return self.get("OrigemSolicitacao", "")

    @property
    def id_solicitante(self) -> int:
        """
        :return: identificador único do solicitante (não mostrado no sistema)
        :rtype: int
        """
        return int(self.get("IdSolicitante", "0"))

    @property
    def categoria_pedido(self) -> str:
        """
        :return: categoria do pedido atribuída pel SIC de acordo com o VCGE (Vocabulário COntrolado do GOverno Eletrônico)
        :rtype: text(200)
        """
        return self.get("CategoriaPedido", "")

    @property
    def sub_categoria_pedido(self) -> str:
        """
        :return: subcategoria do pedido atribuída pel SIC de acordo com o VCGE (Vocabulário COntrolado do GOverno Eletrônico)
        :rtype: text(200)
        """
        return self.get("SubCategoriaPedido", "")

    @property
    def numero_perguntas(self) -> int:
        """
        :return: número de perguntas feitas no pedido
        :rtype: int
        """
        return int(self.get("NumeroPerguntas", "0"))

    @property
    def data_resposta(self) -> datetime.datetime:
        """
        :return: data da resposta ao pedido (campo em branco para pedidos que ainda estejam na situação "Em Tramitação")
        :rtype: Date DD/MM/AAAA HH:MM:SS
        """
        return datetime.datetime.strptime(self.get("DataResposta", ""), '%d/%m/%Y %H:%M:%S')

    @property
    def resposta(self) -> str:
        """
        :return: resposta ao pedido
        :rtype: text(8000)
        """
        return self.get("Resposta", "")

    @property
    def tipo_resposta(self) -> str:
        """
        :return: tipo resposta dada ao pedido (campo em branco para pedidos que ainda estejam na situação "Em Tramitação")
        :rtype: text(100)
        """
        return self.get("TipoResposta", "")

    @property
    def classificacao_resposta(self) -> str:
        """
        :return: subtipo da resposta dada ao pedido (campo em branco para pedidos que ainda estejam na situação "Em Tramitação"
        :rtype: text(200)
        """
        return self.get("ClassificacaoTipoResposta", "")

    @property
    def search_url(self) -> str:
        """
        :return: Portal search URL
        :rtype: Search URL
        """
        nup = urllib.parse.quote(f"NUP={self.protocolo_pedido}")
        return f"{_SEARCH_REQUEST_PROTOCOL}{nup}"

    @property
    def url(self) -> str:
        """
        Behind this method we use Selenium, which can make the process a little slow.
        todo: Try to remove the use of automated browsers
        :return: Direct url to page
        :rtype: url
        """
        if self._direct_url:
            return self._direct_url

        session = HTMLSession()
        r = session.get(self.search_url)
        r.html.render(wait=1, sleep=1)
        url = ""

        for link in r.html.find("a"):
            if "href" in link.attrs:
                url = link.attrs["href"]
                if "ID=" in url:
                    break

        r.close()
        self._direct_url = url
        return url

    @property
    def arquivos_anexados(self) -> typing.Set[tuple]:
        """
        Behind this method we use Selenium, which can make the process a little slow.
        todo: Try to remove the use of automated browsers
        :return: List of files, with access url and link
        :rtype: Set( file_url, file_name )
        """

        session = HTMLSession()
        r = session.get(self.url)
        r.html.render(wait=1, sleep=1)

        urls = set()

        for link in r.html.find("a"):

            if "href" in link.attrs:
                url = link.attrs["href"]

                if "Attachments" in url:
                    tp = (url, link.text)

                    if tp not in urls and str(link.text).strip():
                        urls.add(tp)

        r.close()
        return urls


class Recurso(dict):
    _direct_url = None

    @property
    def id_recurso(self) -> int:
        """
        :return: identificador único do recurso (não mostrado no sistema);
        :rtype: int
        """
        return int(self.get("IdRecurso", "0"))

    @property
    def id_recurso_precedente(self) -> int:
        """
        :return: identificador único do recurso que precedeu este (não mostrado no sistema e em branco no caso de Recursos de 1ª Instância e Reclamações)
        :rtype: int
        """
        return int(self.get("IdRecursoPrecedente", "0"))

    @property
    def desc_recurso(self) -> str:
        """
        :return: descrição do recurso
        :rtype: text(8000)
        """
        return self.get("DescRecurso", "")

    @property
    def id_pedido(self) -> int:
        """
        :return: identificador único do pedido ao qual o recurso pertence (não mostrado no sistema)
        :rtype: int
        """
        return int(self.get("IdPedido", "0"))

    @property
    def id_solicitante(self) -> int:
        """
        :return: identificador único do solicitante (não mostrado no sistema)
        :rtype: int
        """
        return int(self.get("IdSolicitante", "0"))

    @property
    def protocolo_pedido(self) -> str:
        """
        :return: número do protocolo do pedido ao qual o recurso pertence
        :rtype: text(17)
        """
        return self.get("ProtocoloPedido", "")

    @property
    def orgao_superior_associado_ao_destinatario(self) -> str:
        """
        :return: Quando o órgão for vinculado, este campo traz o nome do seu órgão superior
        :rtype: text(250)
        """
        return self.get("OrgaoSuperiorAssociadoaoDestinatario", "")

    @property
    def orgao_destinatario(self) -> str:
        """
        :return: nome do órgão destinatário do recurso
        :rtype: text(250)
        """
        return self.get("OrgaoDestinatario", "")

    @property
    def instancia(self) -> str:
        """
        :return: descrição da instância do recurso
        :rtype: text(80)
        """
        return self.get("Instancia", "")

    @property
    def situacao(self) -> str:
        """
        :return: descrição da situação do recurso
        :rtype: text(80)
        """
        return self.get("Situacao", "")

    @property
    def data_registro(self) -> datetime.datetime:
        """
        :return: data de abertura do recurso;
        :rtype: Date DD/MM/AAAA HH:MM:SS
        """
        return datetime.datetime.strptime(self.get("DataRegistro", ""), '%d/%m/%Y %H:%M:%S')

    @property
    def prazo_atendimento(self) -> datetime.datetime:
        """
        :return: data limite para atendimento ao recurso;
        :rtype: Date DD/MM/AAAA HH:MM:SS
        """
        return datetime.datetime.strptime(self.get("PrazoAtendimento", ""), '%d/%m/%Y %H:%M:%S')

    @property
    def origem_solicitacao(self) -> str:
        """
        :return: informa se o recurso foi aberto em um Balcão SIC ou pela Internet
        :rtype: text(50)
        """
        return self.get("OrigemSolicitacao", "")

    @property
    def tipo_recurso(self) -> str:
        """
        :return: motivo de abertura do recurso
        :rtype: text(80)
        """
        return self.get("TipoRecurso", "")

    @property
    def data_resposta(self) -> datetime.datetime:
        """
        :return: data da resposta ao recurso (campo em branco para recursos que ainda estejam na situação "Em Tramitação")
        :rtype: Date DD/MM/AAAA HH:MM:SS
        """
        return datetime.datetime.strptime(self.get("DataResposta", ""), '%d/%m/%Y %H:%M:%S')

    @property
    def resposta_recurso(self) -> str:
        """
        :return: resposta ao recurso;
        :rtype: text(8000)
        """
        return self.get("RespostaRecurso", "")

    @property
    def tipo_resposta(self) -> str:
        """
        :return: tipo resposta dada ao recurso (campo em branco para recursos que ainda estejam na situação "Em Tramitação")
        :rtype: text(80)
        """
        return self.get("TipoResposta", "")

    @property
    def search_url(self) -> str:
        """
        :return: Portal search URL
        :rtype: Search URL
        """
        nup = urllib.parse.quote(f"NUP={self.protocolo_pedido}")
        return f"{_SEARCH_REQUEST_PROTOCOL}{nup}"

    @property
    def url(self) -> str:
        """
        Behind this method we use Selenium, which can make the process a little slow.
        todo: Try to remove the use of automated browsers
        :return: Direct url to page
        :rtype: url
        """
        if self._direct_url:
            return self._direct_url

        session = HTMLSession()
        r = session.get(self.search_url)
        r.html.render(wait=1, sleep=1)
        url = ""

        for link in r.html.find("a"):
            if "href" in link.attrs:
                url = link.attrs["href"]
                if "ID=" in url:
                    break

        r.close()
        self._direct_url = url
        return url

    @property
    def arquivos_anexados(self) -> typing.Set[tuple]:
        """
        Behind this method we use Selenium, which can make the process a little slow.
        todo: Try to remove the use of automated browsers
        :return: List of files, with access url and link
        :rtype: Set( file_url, file_name )
        """

        session = HTMLSession()
        r = session.get(self.url)
        r.html.render(wait=1, sleep=1)

        urls = set()

        for link in r.html.find("a"):

            if "href" in link.attrs:
                url = link.attrs["href"]

                if "Attachments" in url:
                    tp = (url, link.text)

                    if tp not in urls and str(link.text).strip():
                        urls.add(tp)

        r.close()
        return urls


class Solicitante(dict):

    @property
    def id_solicitante(self) -> int:
        """
        :return: identificador único do solicitante (não mostrado no sistema)
        :rtype: int
        """
        return int(self.get("IdSolicitante", "0"))

    @property
    def tipo_demanda(self) -> str:
        """
        :return: Pessoa Fìsica ou Pessoa Jurídica
        :rtype: text(15)
        """
        return self.get("TipoDemandante", "")

    @property
    def data_nascimento(self) -> datetime.datetime:
        """
        :return: data de nascimento do solicitante
        :rtype: Date DD/MM/AAAA
        """
        return datetime.datetime.strptime(self.get("DataNascimento", ""), '%d/%m/%Y')

    @property
    def sexo(self) -> str:
        """
        :return: Masculino ou Feminino (em branco para pessoa jurídica)
        :rtype: texto(13)
        """
        return self.get("Sexo", "")

    @property
    def escolaridade(self) -> str:
        """
        :return: Escolaridade do solicitante (em branco para pessoa jurídica)
        :rtype: text(200)
        """
        return self.get("Escolaridade", "")

    @property
    def profissao(self) -> str:
        """
        :return: Profissão do solicitante (em branco para pessoa jurídica)
        :rtype: text(200)
        """
        return self.get("Profissao", "")

    @property
    def tipo_pessoa_juridica(self) -> str:
        """
        :return: tipo de Pessoa Jurídica do solicitante (em branco para pessoa física)
        :rtype: text(200)
        """
        return self.get("TipoPessoaJuridica", "")

    @property
    def pais(self) -> str:
        """
        :return: país de residência do solicitante;
        :rtype: text(200)
        """
        return self.get("Pais", "")

    @property
    def uf(self) -> str:
        """
        :return: UF de residência do solicitante
        :rtype: text(2)
        """
        return self.get("UF", "")

    @property
    def municipio(self) -> str:
        """
        :return: Município de residência do solicitante
        :rtype: text(200)
        """
        return self.get("Municipio", "")
