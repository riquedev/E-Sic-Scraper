import typing, pathlib
from bs4 import BeautifulSoup
from E_Sic.pedidos_respostas.conts import _ALOWED_FORMAT
from E_Sic.pedidos_respostas.exceptions import InvalidFile
from E_Sic.pedidos_respostas.types import Pedido, Recurso,Solicitante



class FileParser:
    _file_name: str = ""

    def __init__(self, file_name: str, delimiter=";"):
        if not FileParser.is_valid_file(file_name):
            raise InvalidFile("The file passed in is invalid for the parser.")

        self._file_name = file_name
        self.delimiter = delimiter

    def open(self) -> typing.Iterator[dict]:

        with open(self._file_name, "rb") as handler:
            if pathlib.Path(self._file_name).suffix == ".xml":
                return self._build_from_xml(contents=handler.read())
            elif pathlib.Path(self._file_name).suffix == ".csv":
                return self._build_from_csv(handler=handler.read())
            else:
                raise InvalidFile("The file passed in is invalid for the parser.")

    def _build_from_csv(self, handler) -> typing.Iterator[dict]:
        raise NotImplementedError("This method was not implemented due to several problems in the CSV file.")

    def _build_from_xml(self, contents: bytes) -> typing.Iterator[dict]:
        soup = BeautifulSoup(contents, 'xml')

        if "_Pedidos_" in self._file_name:

            for pedido in soup.find_all("Pedido"):

                data = Pedido()

                for key, value in pedido.attrs.items():
                    data[key] = value

                yield data

        elif "_Recursos_" in self._file_name:

            for recurso in soup.find_all("Recurso"):
                data = Recurso()

                for key, value in recurso.attrs.items():
                    data[key] = value
                yield data

        elif "_Solicitantes_" in self._file_name:
            for solicitante in soup.find_all("Solicitante"):
                data = Solicitante()

                for key, value in solicitante.attrs.items():
                    data[key] = value

                yield data
        else:
            raise InvalidFile("This method was not implemented due to several problems in the CSV file.")

    @staticmethod
    def is_valid_file(file_name) -> bool:
        names = ("_Pedidos_" in file_name, "_Recursos_" in file_name, "_Solicitantes_" in file_name)
        return any(names) and pathlib.Path(file_name).suffix in map(lambda t: f".{t.lower()}", _ALOWED_FORMAT)

    def __enter__(self):
        return self.open()

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
