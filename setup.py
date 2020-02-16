from setuptools import setup, find_packages
from os import path
from io import open

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='E_Sic',
    version='2020.02.15',
    description='Pacote para automatização de coletas no portal E-Sic, você pode obter os dados sobre as perguntas, respostas e até mesmo baixar os arquivos anexados.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/riquedev/E-Sic-Scraper',
    author='Henrique da Silva Santos',
    keywords='dados-abertos dadosgovbr scraper e-sic brasil perguntas-e-respostas',
    packages=find_packages(where='.'),
    python_requires='>=3.6',
    install_requires=[
        'aiofile==1.5.2',
        'aiofiles==0.4.0',
        'aiohttp==3.6.2',
        'appdirs==1.4.3',
        'async-timeout==3.0.1',
        'asyncio==3.4.3',
        'attrs==19.3.0',
        'beautifulsoup4==4.8.2',
        'bs4==0.0.1',
        'certifi==2019.11.28',
        'chardet==3.0.4',
        'cssselect==1.1.0',
        'fake-useragent==0.1.11',
        'idna==2.8',
        'idna-ssl==1.1.0',
        'lxml==4.5.0',
        'multidict==4.7.4',
        'parse==1.14.0',
        'pyee==7.0.1',
        'pyppeteer==0.0.25',
        'pyquery==1.4.1',
        'requests==2.22.0',
        'requests-html',
        'six==1.14.0',
        'soupsieve==1.9.5',
        'tqdm==4.42.1',
        'typing-extensions==3.7.4.1',
        'urllib3==1.25.8',
        'w3lib==1.21.0',
        'websockets',
        'yarl',
        'codecov'
    ],

    project_urls={
        'Bug Reports': 'https://github.com/riquedev/E-Sic-Scraper/issues',
        'Source': 'https://github.com/riquedev/E-Sic-Scraper',
    },
)
