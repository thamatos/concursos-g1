# Concursos hoje

Esse repositório é um site para a aula de Algoritmos de Automação do MJD 2022-2023 do Insper. Ele foi criado para automatizar a raspagem dos concursos publicados diariamente no site PCI Conucursos e apresentá-los para o leitor de forma organizada.

O repositório possui:
- [Robô do Telegram](t.me/bothais_bot) que responde em tempo real
- Site no [Render](https://site-teste-thamatos.onrender.com/) em Flask com concursos atualizados
- Integração com Google sheets para guardar usuários que queiram se inscrever no bot

O site e o robô entregam a quantidade, a soma das vagas e os links de três categorias:
- [Concursos abertos](https://site-teste-thamatos.onrender.com/concursos)
- [Editais com cadastro reserva](https://site-teste-thamatos.onrender.com/reserva)
- [Editais com vagas de estágio](https://site-teste-thamatos.onrender.com/estagio)

## O que cada arquivo contém
- templates contém dois arquivos em html: o da página inicial e o das páginas de conteúdo
- app.py tem as funções que criam as páginas no Render usando Flask, disparam as mensagens via Telegram e e fazem integração com o Google Sheets
- funcoes.py define as funções que raspam, contam, automatizam textos e pegam os links dos concursos
- requiriments.txt tem a lista de bibliotecas necessárias para o código rodar


