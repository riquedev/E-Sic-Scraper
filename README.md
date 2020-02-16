# E-Sic-Scraper
[![Build Status](https://travis-ci.com/riquedev/E-Sic-Scraper.svg?branch=master)](https://travis-ci.com/riquedev/E-Sic-Scraper) 
[![codecov](https://codecov.io/gh/riquedev/E-Sic-Scraper/branch/master/graph/badge.svg)](https://codecov.io/gh/riquedev/E-Sic-Scraper)
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