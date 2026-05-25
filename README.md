# vi-player

![Player](img/player.gif)

O **vi-player** é um player de música inspirado diretamente na filosofia do [Vim](https://github.com/vim/vim) e [NeoVim](https://github.com/neovim/neovim).
A proposta do projeto não é apenas reproduzir músicas no terminal, mas transformar a experiência de navegação musical em algo novo, orientado a:

- comandos
- modos
- atalhos de teclado
- renderização direta no terminal

## Filosofia

O projeto parte da ideia de que interfaces gráficas tradicionais nem sempre são a única forma de interagir com mídia. Em vez de botões, menus, mouse, múltiplas janelas, o vi-player aposta em comandos, navegação modal, atalhos inspirados no Vim, interface renderizada diretamente via ANSI Escape Codes.

A intnção é criar uma experiência que lembre ferramentas como:

- [Ranger](https://github.com/ranger/ranger)
- [Cmus](https://github.com/cmus/cmus)
- [Ncmcpp](https://github.com/ncmpcpp/ncmpcpp)
- [tmux](https://github.com/tmux/tmux)

## Objetivos

O foco principal é:

- navegação rápída
- fluxo orientado ao teclado
- sistema de comandos extensível
- renderização manual de interface
- arquitetura leve e extensível
- customização
- futura integração com scripts/plugins

## Estado Atual

Atualmente o projeto já possui funções básicas como:

- reprodução de músicas locais
- navegação entre faixas
- modos básicos
- destaque visual de seleção
- suporte inicial a temas

Grande parte da arquitetura ainda está sendo construída e refatorada conforme o projeto evolui.

## Funcionalidades

- [x] Reprodução de músicas locais
- [x] Navegação entre faixas
- [x] Pause/Resume
- [x] Tema Customizável
- [ ] Sistema de fila 
- [ ] Keybinds customizáveis
- [ ] Busca
- [ ] Configuração via [Lua](https://www.lua.org)

## Dependências

O projeto foi desenvolvido em **Python**, utilizando renderização manual, com engine própria, sem frameworks TUI ou bibliotecas completas.

Bibliotecas atualmente utilizadas:

```
python-mpv
mutagen
```

Futuramente, o projeto terá:
- Sistema de setup automático
- instalação de dependências
- geração inicial de configurações

# Navegação

O vi-player utiliza navegação inspirada diretamente no Vim.

## Movimento

| Tecla | Ação |
|---|---|
| `j` | Próxima música |
| `k` | Música anterior |
| `h` | Início da lista |
| `l` | Final da lista |

## Modos

O player funciona através de modos.

### MODO NORMAL
Modo principal de navegação. usando `h`, `j`, `k` e `l` para escolher a faixa

### MODO DE COMANDO
Acessado pressionando `:`. É o modo que controla o play, pause e skips

Exemplo:
```vim
:sk 10
```
Executa o comando de pular para a música de número 10

## Comandos atuais

| Comando | Função |
|---|---|
| `:p` | Reproduzir música |
| `:pp` | Pause/Resume |
| `:sk` | Pular para música |
| `:nx` | Próxima música |
| `:pv` | Música Anterior |
| `:o` | Abrir novo diretório |
| `:q` | Sair |

# Aviso

O projeto ainda está em desenvolvimento inicial e diversas partes da arquitetura estão sendo reestruturadas constantemente. Portanto, há muitos bugs e erros a serem tratados e corrigidos.
