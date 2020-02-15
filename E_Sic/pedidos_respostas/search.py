import asyncio, aiohttp, atexit, aiofile, re, os, typing, glob, zipfile
from bs4 import BeautifulSoup
from E_Sic.pedidos_respostas.exceptions import InvalidYear
from E_Sic.pedidos_respostas.conts import _ENCODING_, _URL_, _SELECT_FORMAT_, _SELECT_YEAR_, _MIN_YEAR


class BuscarPedidosRespostas:

    """
    Class used to facilitate the search process within the portal
    In this class I used and abused async, maybe it was a bad thing, in the future I will add a sync version.
    """

    _loop: asyncio.AbstractEventLoop = None
    _client: aiohttp.ClientSession = None

    def __init__(self):
        self._loop = asyncio.get_event_loop()
        self._client = aiohttp.ClientSession(loop=self.loop)
        atexit.register(self._close_connection_)

    def _close_connection_(self):
        self.loop.run_until_complete(self.client.close())

    async def _download(self, year: int = 2016, file_format: str = "", path: str = ".", delete: bool = False) -> \
            typing.Iterator[str]:

        """
        Method for downloading data in the year and specified format.
        :param year: Year of the desired file
        :param file_format: Desired file format
        :param path: Place to be saved
        :param delete:  Should we delete the zip?
        :return: Generator<str>
        """

        if year < _MIN_YEAR:
            raise InvalidYear(f"The requested year ({year}) is far below the minimum ({_MIN_YEAR}).")

        # We need to retrieve the form fields to send the post.
        data = await self._get_url_submit_fields(_URL_)

        # Now, we need to inform the year and type of file we want.
        data[_SELECT_YEAR_] = year
        data[_SELECT_FORMAT_] = file_format

        # Vualá, now just download
        file_name = await self._download_file_post(_URL_, data, path)

        # Let's extract the zip
        zip_output = os.path.join(path, f"download_{file_format.lower()}")
        output_files = await self._uncronpress_zip(file_name, zip_output)

        # If you need, we delete the zip.
        if delete:
            os.remove(file_name)

        # Now, we return the extracted files to a generator, using iglob.
        return glob.iglob(os.path.join(output_files, f"*.{file_format.lower()}"))

    def download_csv(self, year: int = 2016, path: str = ".", delete_zip: bool = False) -> typing.Iterator[str]:
        """
        Download CSV files

        :param year: Year of the desired file
        :param path: Place to be saved
        :param delete_zip: Should we delete the zip?
        :return: Generator<str>
        """

        return self.loop.run_until_complete(self._download(
            year,
            "CSV",
            path,
            delete_zip
        ))

    def download_xml(self, year: int = 2016, path: str = ".", delete_zip: bool = False) -> typing.Iterator[str]:
        """
        Download the XML files
        :param year: Year of the desired file
        :param path: Place to be saved
        :param delete_zip: Should we delete the zip?
        :return: Generator<str>
        """
        return self.loop.run_until_complete(self._download(
            year,
            "XML",
            path,
            delete_zip
        ))

    async def _uncronpress_zip(self, zip_path: str, output: str) -> str:
        """
        Method responsible for unzipping the zip file and sending it to the destination folder.
        :param zip_path: Zip file location
        :param output: Output directory location.
        :return: Output directory location.
        """

        # We need to create the directory if it doesn't exist.
        if not os.path.exists(output):
            os.makedirs(output, exist_ok=True)

        with zipfile.ZipFile(zip_path, "r") as zip_obj:
            zip_obj.extractall(output)

        return output

    async def _write_file(self, path: str, data: bytes) -> tuple:
        """
        Function responsible for writing the file asynchronously
        :param path: File location
        :param data: Writing data
        :return: tuple(bool, path)
        """
        async with aiofile.AIOFile(path, 'wb') as afp:
            await afp.write(data)
            await afp.fsync()

        return True, path

    async def _download_file_post(self, url: str, body: dict, path: str) -> str:
        """
        Method responsible for downloading the file after performing the POST method
        :param url: URL to submit
        :param body: Form data
        :param path: Download location
        :return: Download file location
        """
        async with self.client.post(url, data=body) as response:
            response.raise_for_status()
            fname = re.findall("filename=(.+)", response.headers.get("content-disposition"))[0]
            file_path = os.path.join(path, str(fname).replace("\"", ""))

            with open(file_path, "wb") as f:
                f.write(await response.read())

        return file_path

    async def _get_content(self, url: str) -> bytes:
        """
        Method responsible for making a GET request and returning the content (in bytes), if everything went well
        :param url: request location
        :return: Request Content
        """
        async with self.client.get(url) as response:
            response.raise_for_status()
            data = await response.read()

        return data

    async def _get_url_submit_fields(self, url: str) -> dict:
        """
        Returns form fields found in the provided url (input's only)
        :param url: Form url
        :return: Fields dict
        """
        data = await self._get_content(url)
        return await self._bs4_find_fields(data)

    async def _bs4_find_fields(self, content: bytes) -> dict:
        """
        Finds content fields using bs4
        :param content: HTML Content
        :return: Form fields dict
        """
        data = {}
        soup = BeautifulSoup(content.decode(_ENCODING_), "lxml")
        for form_input in soup.find_all("input"):
            if form_input.has_attr("name") and form_input.has_attr("value"):
                data[form_input["name"]] = form_input["value"]

        return data

    @property
    def loop(self) -> asyncio.AbstractEventLoop:
        return self._loop

    @property
    def client(self) -> aiohttp.ClientSession:
        return self._client
