# Vi-Player (Lua Version)

Esta branch é uma versão experimental, instável e não representa a versão principal do projeto VI-Player

Esta versão existe para testar ideias relacionadas à integração do player com a linguagem Lua, sisema de plugins e APIs internas. Ela pode conter código incompleto, bugs, funcionalidades antigas ou partes desatualizadas em relação à branch `main`.

Para a versão oficial e instável do projeto, use a branch `main`.

# Objetivos

A branch `experimental/lua` funciona como uma área de testes para explorar:
- integração com a linguagem Lua usando a biblioteca lupa;
- criação de uma API global para plugins
- automações e extensões inspiradas no ecossistema do Neovim;
- possíveis melhorias futuras para temas, linha de comando, playlist e interface.

Esta versão não tem compromisso imediato com estabilidade. A prioridade é testar arquitetura, descobrir problemas e validar ideias antes de levar qualquer coisa para a versão principal

# Diferenças

Essa branch contém avanços significativos em relação à versão principal, já possuindo:
- sistema de API global do player, chamada de `vi`;
- integração com a linguagem Lua;
- plugins escritos totalmente em Lua, como `autopairs`, `luatheme` e `lualine`;
- adições no sistema de configuração do player;
- extensão das configurações em runtime, por meio do comando `:set`.

# Plugins

Esta versão do player já possui alguns plugins disponíveis para uso, porém, ainda em fase de testes.

Para ser possível executar os plugins, é necessário instalar a biblioteca lupa:
```bash
pip install lupa
```

## luatheme

Plugin usado para testar comandos e API de temas. A sintaxe básica de comandos do plugin é: `:lt <opção>`.

As opções atuais do plugin são:
- `:lt current`: retorna o tema atual da sessão;
- `:lt random`: muda o tema da sessão para um tema aleatório; 
- `:lt grep <texto>`: retorna o primeiro tema com o nome indicado.

## lualine

Inspirado no plugin lualine do Neovim, cria uma statusline customizada e dinâmica, utilizando a sintaxe da linguagem lua para modificar textos, posição e widgets da linha de status.

## autopairs

Primeiro plugin básico, criado para testar a integração com o player. Ele fecha parênteses, aspas, chaves e colchetes enquanto o usuário digita comandos na linha de comando.

# Licença

Esta versão segue a mesma licença do projeto principal (GPL-3.0)
