import datetime


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
