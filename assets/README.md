# Configuração

Antes de executar o `vi-player`, é necessário configurar os arquivos padrões do projeto.

O player procura automaticamente seus arquivos de configuração em:

```text
~/.config/vi-player/
```

A estrutura esperada atualmente é:

```text
~/.config/vi-player/
├── config.json
└── themes/
    ├── deep-blue.toml
    ├── linen-light.toml
    └── ... 
```

---

# Instalando os arquivos padrões

Copie o conteúdo da pasta `assets/` do projeto para:

```text
~/.config/vi-player/
```

Exemplo:

```bash
mkdir -p ~/.config/vi-player
cp -r assets/* ~/.config/vi-player/
```

---

# config.json

O arquivo principal de configuração do player é o:

```text
~/.config/vi-player/config.json
```

Exemplo:

```json
{
  "general": {
    "theme": "ocean"
  },

  "player": {
    "relativenumbers": true
  },

  "statusline": {
      "left": ["mode", "state"],
      "right": ["theme", "position"],
      "separator": "|"
  }
}
```

---

# Opções atuais

## General

| Campo   | Função                                    |
| ------- | ----------------------------------------- |
| `theme` | Define o tema padrão carregado ao iniciar |

---

## Player

| Campo             | Função                                             |
| ----------------- | -------------------------------------------------- |
| `relativenumbers` | Ativa números relativos inspirados no Vim          |
| `usearrows`       | Ativa alterna entre o uso das setas para navegação |

---

## Statusline

Na última atualização do player, foi implementada a função de customização (ainda parcial) da statusline. podendo ser definidos os widgets da esquerda e direita e o separador dos textos.

```json
"statusline": {
    "left": ["mode", "state"],
    "right": ["theme", "position"],

    "separator": "|"
}
```

| Módulo   | DESCRIÇÃO                             |
|----------|---------------------------------------|
| mode     | Modo atual do player (NORMAL/COMANDO) |
| song     | Música atual tocando                  |
| state    | Estado do player                      |
| theme    | Tema configurado em config.json       |
| position | Posição do cursor na lista de músicas |

# Temas

Os temas ficam em:

```text
~/.config/vi-player/themes/
```

Cada tema é um arquivo `.toml`.

Exemplo:

```text
ocean.toml
retro.toml
slate.toml
```

---

# Estrutura de um tema

A pasta assets/themes já disponibiliza exemplos de temas padrão que podem ser usados no player. Mas novos temas também podem ser criados, seguindo a estrutura:

```toml
[colors]

# Fundo e texto principal
bg = "#20282B"
fg = "#D8DEE4"

# Header
secondary_bg = "#5FA8B8"
secondary_fg = "#F4F7F8"

# Statusline
statusline_bg = "#2D6F7A"
statusline_fg = "#F4F7F8"

# Índices da playlist
index_bg = "#20282B"
index_fg = "#7E909A"

# Linha selecionada
indicator_line_bg = "#4EA8B9"
indicator_line_fg = "#F4F7F8"

# Número da linha selecionada
indicator_num_bg = "#20282B"
indicator_num_fg = "#5FA8B8"

```

---

# Campos obrigatórios

Para um tema funcionar corretamente, recomenda-se definir pelo menos:

```toml
bg = "#000000"
fg = "#FFFFFF"
```

Os demais campos possuem fallback automático.

---

# Alterando o tema em runtime

Durante a execução do player, o tema pode ser alterado com:

```vim
:colorscheme ocean
```

O nome deve ser informado sem a extensão `.toml`.

Exemplo:

```vim
:colorscheme retro
```

A alteração vale apenas para a sessão atual. Para definir um tema permanente, edite o próprio arquivo `config.json`

---

# Relative Numbers

O vi-player possui suporte a números relativos (`rnu`), inspirado diretamente no Vim.

Quando ativado:

* a linha atual mantém o número absoluto
* as demais mostram distância relativa até a seleção atual

Exemplo:

```text
 3
 2
 1
12
 1
 2
 3
```

Para ativar:

```json
{
  "player": {
    "relativenumbers": true
  }
}
```

Ou, em runtime:

```text
:rnu
```

Ativa e desativa a opção de relativenumber durante a execução

---

# Observações

O sistema de configuração ainda está evoluindo.

Futuramente o projeto terá:

* keybinds customizáveis
* múltiplos perfis
* configuração via Lua
* sistema de plugins
* comandos persistentes
* configuração dinâmica em runtime

Atualmente, parte das configurações ainda é experimental e sujeita a mudanças.

