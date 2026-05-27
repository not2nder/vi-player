# Configurações

Antes de executar o arquivo `main.py`, é preciso fazer algumas configurações externas. Os arquivos de configurações, pré definições e esquemas de cores do player tem que se encontrar em: `~/.config/vi-player/`

```
~/.config/vi-player/
├── config.json
└── themes/
    ├── deep-blue.toml
    ├── linen-light.toml
    ├── ocean.toml
    ├── retro.toml
    ├── slate.toml
    └── warm.toml
```

Mova o conteúdo da pasta `assets` para a pasta de configuração padrão do vi-player. No arquivo de configuração `config.json`, você pode definir o esquema de cores padrão alterando o campo `theme`.

```json
"general": {
    "theme": "ocean"
}
```

A partir disso, você já pode criar os próprios temas. Basta criar um arquivo .toml com o nome do seu tema e definir as cores de sua preferência.

```toml
[colors] # Obrigatóriamente tem que estar no início do arquivo

bg = "#20282B" # Cor de fundo do player
fg = "#D8DEE4" # Cor do texto do player

# Header
secondary_bg = "#5FA8B8" 
secondary_fg = "#F4F7F8"

# Statusline
statusline_bg = "#2D6F7A"
statusline_fg = "#F4F7F8"

# Números das faixas
index_bg = "#20282B"
index_fg = "#7E909A"

# Linha dos indicadores
indicator_line_bg = "#4EA8B9"
indicator_line_fg = "#F4F7F8"

# Número dos indicadores
indicator_num_bg = "#20282B"
indicator_num_fg = "#5FA8B8"

# Barra de avisos
warning_bg = "#D65D8F"
warning_fg = "#FDFDFD"
```

Alguns parâmetros são opcionais, mas para o tema funcionar corretamente, é recomendado que tenha no mínimo bg e fg (primário e secundário).

Para alterar o tema durante a execução do player, basta executar o comando `:theme` com o nome do seu tema na frente do comando, sem a extensão .toml
