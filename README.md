# vi-player

Um player de música para terminal, inspirado diretamente na filosofia do Vim e NeoVim.
A proposta do projeto não é criar apenas mais um player de CLI. O objetivo central é transformar a navegação musical em uma experiência modal, rápida e orientada apenas ao teclado, utilizando motions, comandos e renderização direta no terminal.

Inspirado em feramentas como:
- [Vim](https://github.com/vim/vim)
- [NeoVim](https://github.com/neovim/neovim)
- [Ranger](https://github.com/ranger/ranger)
- [Cmus](https://github.com/cmus/cmus)
- [Ncmcpp](https://github.com/ncmpcpp/ncmpcpp)
- [tmux](https://github.com/tmux/tmux)

# Features

* Navegação modal
* Reprodução de músicas locais
* Movimentação diretamente inspirada no Vim
* Sistema de comandos em runtime
* Sistema de temas
* Arquitetura leve e modular

# Filosofia

O projeto explora uma forma alternativa de interagir com mídia dentro do terminal. 

Ao invés de mouse, botões gráficos, janelas e interfaces tradicionais, ele aposta em:
* fluxo orientado ao teclado
* interação modal
* renderização direta
* navegação rápida

A ideia de longo prazo é criar uma experiência mais próxima de editar texto no Vim do que utilizar um player convencional.

# Instalação

## Requisitos

* Python 3.11+
* mpv instalado no sistema

## Dependências

```bash
pip install python-mpv mutagen wcwidth
```

## Clonando o repositório

```bash
git clone https://github.com/not2nder/ci-player.git
cd vi-player
```

# Executando

Sempre que for executar o arquivo .py, passe como argumento o diretório onde estão os arquivos .mp3

```bash
python main.py ~/Músicas
```

# Navegação

O vi-player usa navegação diretamente inspirada no Vim.

## Movimentos básicos

| Motion | Ação             |
| ------ | ---------------- |
| `j`    | Próximo item     |
| `k`    | Item anterior    |
| `gg`   | Ir para o início |
| `G`    | Ir para o final  |
| `h`    | Primeiro item    |
| `l`    | Último item      |

## Movimentos Relativos

Assim como no Vim, é possível usar números antes dos motions.

### Exemplos

```text
10j
```

Pula 10 itens abaixo.

```text
5k
```

Volta 5 itens para cima.

---

## Navegação por porcentagem

```text
50%
```

Vai para o meio da playlist.

```text
25%
```

Vai para 25% da playlist.

---

# Modos

O player funciona através de modos.

---

## MODO NORMAL

Modo principal de navegação.

Responsável por:

* motions
* navegação
* atalhos rápidos

---

## MODO DE COMANDO

Acessado pressionando `:`.

Responsável por executar comandos.


| Comando               | Função                       |
| --------------------- | ---------------------------- |
| `:p`                  | Reproduzir música atual      |
| `:pp`                 | Pause/Resume                 |
| `:n`                  | Próxima música               |
| `:pv`                 | Música anterior              |
| `:sk <n>`             | Pular para música específica |
| `:colorscheme <tema>` | Trocar tema da sessão        |
| `:q`                  | Sair                         |

---

# Temas

Os temas são carregados de `~/.config/vi-player/themes`. O tema padrão do player é definido em `~/.config/vi-player/config.json`.
Exemplo de configuração:

```json
{
  "general": {
    "theme": "ocean"
  }
}
```

Também é possível trocar o tema durante a execução, executando o comando:

```vim
:colorscheme ocean
```

# Configuração

Antes de iniciar o player, mova os arquivos da pasta `assets/` para a pasta `~/.config/vi-player/`:

A estrutura do arquivo `config.json` deve ser algo parecido com isso:

```json
{
  "general": {
    "theme": "ocean"
  },

  "player": {
    "relativenumbers": true
  }
}
```

Para mais detalhes, acesse o arquivo README.md na pasta `assets`.

---

# Estado Atual

Implementado:

* reprodução de músicas
* comandos em runtime
* navegação modal
* dirty rendering
* suporte a resize
* temas
* relative numbers
* motions inspirados no Vim

Em desenvolvimento:

* histórico de comandos
* sistema de busca
* viewport/renderização parcial
* sistema de fila
* keymaps customizáveis
* arquitetura de plugins

---

# Objetivo de Longo Prazo

A ideia do projeto não é apenas criar um player de música para terminal.

O objetivo é construir:

* um ambiente modal para mídia
* um sistema de navegação extensível
* uma interface altamente customizável
* um workflow totalmente orientado ao teclado
* uma experiência inspirada em editores modais

---

# Contribuição

O projeto ainda está em estágio inicial e a arquitetura evolui constantemente. Refatorações são frequentes conforme novos sistemas são modularizados e desacoplados.

Sugestões, ideias e experimentações são bem-vindas.

---

# Licença

GPL License.

