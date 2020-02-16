import datetime, urllib.parse, typing
from requests_html import HTMLSession
from E_Sic.pedidos_respostas.conts import _SEARCH_REQUEST_PROTOCOL


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
