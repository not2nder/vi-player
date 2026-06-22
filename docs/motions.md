# Movimentos e Operadores

O vi-player utiliza um modelo de interação inspirado em editores modais como o Vim.

A ideia central é simples: comandos são compostos por movimento, operação e contexto. Existem 3 camadas que compõem os comandos:

- Movimentos: Navegação pela playlist
- Operadores: Ações sobre itens
- Ações: Comandos imediatos do player

Essa separação permite que a navegação e manipulação da playlist seja feita diretamente pelo teclado, com comandos curtos, consistentes e previsíveis.

# Movimentos

Movimentos são responsáveis exclusivamente pela navegação na playlist. Eles não executam nenhuma ação por si só, apenas alteram a posição do cursor.

Os movimentos básicos são:

| Tecla | Ação               |
| ----- | ------------------ |
| `j`   | Próximo item       |
| `k`   | Item anterior      |
| `gg`  | Início da playlist |
| `G`   | Final da playlist  |

## Contadores

Alguns movimentos aceitam um contador numérico antes da tecla. Eles modificam a posição final do cursor. Por exemplo:

```text
3j
```

Move o cursor 3 itens abaixo.

```text
3k
```

Move o cursor 3 itens acima.

```text
10gg
```

Move o cursor para o item de número 10. Equivalente ao comando `10G`.

O padrão sempre é **contador + movimento**. Quando o contador não é especificado, ele assume o valor de 1. Então:

```text
j = 1j
k = 1k
```

# Operadores

Operadores são comandos que atuam sobre itens da playlist. Diferente dos movimentos, operadores executam ações reais sobre itens da playlist. Atualmente, existem apenas 2 operadores, que são:

| Tecla | Ação                     |
| ----- | ------------------------ |
| `d`   | Deletar item da playlist |
| `y`   | Copiar item da playlist  |

Os operadores atuam sobre um alvo, definido por um movimento, então o padrão de uso é: **operador + movimento**

Por exemplo:

```text
dj = delete + avance 1 item
```

Resultado: 2 linhas deletadas

```text
dk = delete + volte 1 item
```

Resultado: 2 dlinhas deletadas

Como os operadores funcionam em conjunto com movimentos, eles também interpretam os contadores de movimento.

```text
d2j = delete + avance 2 itens
```

Resultado: 3 linhas deletadas

Existe um caso específico em que o operador não recebe um motion como argumento, que é quando o usuário digita o mesmo operador duas vezes.

```text
dd
```

Quando um operador recebe ele mesmo como argumento, ele opera sobre o item indicado, então:

```text
dd = delete o item atual
```

O mesmo se aplica ao operador `y`:

```text
yy = copie o item atual
```

## Contadores de Operadores

Assim como os movimentos utilizam contadores para modificar a posição, os operadores também podem receber contadores para modificar operações, por exemplo:

```text
2dd = delete 2 itens
```

Combinando isso com os movimentos apresentados anteriormante, temos um padrão:

```text
[contador] operador [contador] movimento
```

Esse sistema permite o uso de diversas combinações entre comandos. Por exemplo:

```text
d2j = delete + 2 linhas na frente
```

Resultado: 3 linhas deletadas

```text
2dj = delete + mover 2 itens
```

Resultado: 3 linhas deletadas.

A principal diferença nessa abordagem é que: o contador do operador expande o alcance da operação.

O comando `d2j` primeiro calcula o movimento `2j` e remove o intervalo entre o cursor e o destino. Já o `2dj` mantém o movimento `j` e aplica o alcance da operação duas vezes.

Em ambos os casos o operador é executado como uma única ação sobre o resultado final, não como vários comandos separados. Embora tenham resultados parecidos, os dois comandos sõ interpretados de forma distinta.

Ambos os operadores `y` e `d` armazenam o conteúdo selecionado no registrador da playlist, que funciona como uma área de transferência. Para colar o conteúdo, basta apertar `p` que representa a ação de colar.

# Ações

Existe uma outra classe de comandos na aplicação que não realiza operações ou navega na playlist, mas executa ações imediatas sobre o player.

| Ação | Descrição                     |
| ---- | ----------------------------- |
| `h`  | Voltar 5 segundos na música   |
| `l`  | Avançar 5 segundos na música  |
| `:`  | Entrar em modo de comando     |
| `q`  | Sair do player                |
| `p`  | Colar conteúdo do registrador |

Essas ações não recebem contadores nem operadores.
