BOTWIPY
======
Bot para Twitter que utiliza o padrão aberto para autorização OAuth

## Introdução #
O _BOTWIPY_ é um software open-source desenvolvido em Python, que utiliza a biblioteca tweepy para a comunicação entre o bot e a conta do twitter, através da API OAUTH.

## Características #
O _BOTWIPY_ consegue visualizar mensagens onde ele foi mensionado, seguir a pessoa que o mencionou e mandar uma mensagem de agradecimento.
O _BOTWIPY_ também analisa mensagens postados por pessoas que ele segue, e verifica se existe algum usuário citado na mensagem, se sim, ele segue aquele usuário.
Para a persistência dos dados foi utilizado o banco de dados Redis, para o armazenamento temporário das chaves oauth, devido a sua fácil utilização.
Para a interface gráfica foi utilizado o PyQt4, devido a sua portabilidade e facilidade de manipulação de threads.

## Wiki do Projeto #
Contém a instalação e configuração do projeto.

https://github.com/CharlesGarrocho/BOTWIPY/wiki

## Desenvolvedor #
Charles Tim Batista Garrocho

## Screenshots #
Tela Inicial:

![alt text](https://raw.github.com/CharlesGarrocho/BOTWIPY/master/samples/tela_inicial.png "Tela Inicial")

Tela de Alteração de Chaves:

![alt text](https://raw.github.com/CharlesGarrocho/BOTWIPY/master/samples/tela_chaves.png "Tela de Alteração de Chaves")

Tela de Preferências:

![alt text](https://raw.github.com/CharlesGarrocho/BOTWIPY/master/samples/tela_preferencias.png "Tela de Preferências")

Tela Sobre o Software:

![alt text](https://raw.github.com/CharlesGarrocho/BOTWIPY/master/samples/tela_sobre.png "Tela Sobre o Software")
