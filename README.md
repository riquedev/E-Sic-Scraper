# E-Sic-Scraper
[![Build Status](https://travis-ci.com/riquedev/E-Sic-Scraper.svg?branch=master)](https://travis-ci.com/riquedev/E-Sic-Scraper) 
[![codebeat badge](https://codebeat.co/badges/91ecff73-2df5-46c9-89c7-3f53d85c3738)](https://codebeat.co/projects/github-com-riquedev-e-sic-scraper-master)
[![BCH compliance](https://bettercodehub.com/edge/badge/riquedev/E-Sic-Scraper?branch=master)](https://bettercodehub.com/)
[![PyPI version](https://badge.fury.io/py/E-Sic.svg)](https://badge.fury.io/py/E-Sic)

[![Maintainability](https://api.codeclimate.com/v1/badges/4781fce01dd82b706b72/maintainability)](https://codeclimate.com/repos/5e4955e75cfea500c7000f8e/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/4781fce01dd82b706b72/test_coverage)](https://codeclimate.com/repos/5e4955e75cfea500c7000f8e/test_coverage)
[![codecov](https://codecov.io/gh/riquedev/E-Sic-Scraper/branch/master/graph/badge.svg)](https://codecov.io/gh/riquedev/E-Sic-Scraper)
[![](https://img.shields.io/badge/python-3.6-blue.svg)](https://pypi.org/project/sanic-restful/)


[![star this repo](http://githubbadges.com/star.svg?user=riquedev&style=flat-square&repo=E-Sic-Scraper)](https://github.com/riquedev/E-Sic-Scraper)
[![fork this repo](http://githubbadges.com/fork.svg?user=riquedev&style=flat-square&repo=E-Sic-Scraper)](https://github.com/riquedev/E-Sic-Scraper/fork)

![](./images/e-sic.jpg) 


Pacote para automatização de coletas no portal E-Sic, você pode obter os dados sobre as perguntas, respostas e até mesmo baixar os arquivos anexados.

#### Instalação

`pip install E-Sic`

#### Atenção

Alguns arquivos podem estar temporariamente indisponíveis, você pode conferir os anos disponíveis no portal. 

#### Como Utilizar

```python
from E_Sic.pedidos_respostas import BuscarPedidosRespostas, FileParser, types

if __name__ == "__main__":
    instance = BuscarPedidosRespostas()
    
    for file_location in instance.download_xml(year=2016, path=".", delete_zip=True):
    
        with FileParser(file_location) as parser:

            for item in parser:

                if isinstance(item, types.Recurso):
                    
                    print(item)  # dict
                    print(item.id_recurso)  # property
                    print(item.arquivos_anexados)  # tuple contains (url, file_name)
                    break

                elif isinstance(item, types.Pedido):
                                    
                    print(item)  # dict
                    print(item.id_pedido)  # property
                    print(item.arquivos_anexados)  # tuple contains (url, file_name)
                    break

                elif isinstance(item, types.Solicitante):
                    
                    print(item)  # dict
                    print(item.id_solicitante)  # property
                    break
```