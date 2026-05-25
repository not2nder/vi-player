# Configurações

Antes de executar o arquivo `main.py`, é preciso fazer algumas configurações externas. Os arquivos de configurações, pré definições e esquemas de cores do player tem ue se encontrar em `~/.config/vi-player/`

```
~/.config/vi-player/
├── config.toml
└── themes/
    ├── defult.toml
    ├── gruvbox.toml
    └── nord.toml
```

Antes de executar o arquivo principal, mova o conteúdo da pasta `assets` para a pasta de configuração padrão do vi-player. No arquivo de configuração `config.toml`, você pode definiro esquema de cores padrão alterando o campo `theme`

```toml
theme="nord"
```

A partir disso, você já pode criar os próprios temas. Basta criar um arquivo .toml com o nome do seu tema e definir as cores de sua preferência.

```toml
[colors]

bg = "#282828" # Cor de fundo do player
fg = "#ebdbb2" # Cor do texto

secondary_bg = "#3c3836" # Cor de fundo secundária (statusline e header)
secondary_fg = "#ebdbb2" # Cor do texto secundária

statusline_bg = "#98971a" # Cor de fundo da linha de status
statusline_fg = "#1s2021" # Cor do texto da linha de status

highlight_bg = "#b8bb26" # Cor do texto da música selecionada
highlight_fg = "#1d2021" # Cor de fundo da música selecionada

index_bg = "#458588" # Cor de fundo dos números indicadores
index_fg = "#ebdbb2" # Cor do textoo dos números indicadores
```

Alguns parâmetros são opcionais, mas para o tema funcionar corretamente, é recomendado que tenha no mínimo bg e fg (primário e secundário).
