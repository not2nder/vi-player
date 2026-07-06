# Motions, Operators and Actions

Vi-Player uses a modal command system inspired by Vim.

Instead of assigning a dedicated key to every action, commands are built by combining a small set of reusable components. This makes the interface compact, expressive and easy to learn.

There are three categories of commands:

| Category      | Purpose                              |
| ------------- | ------------------------------------ |
| **Motions**   | Move the cursor through the playlist |
| **Operators** | Perform actions on playlist items    |
| **Actions**   | Execute immediate player commands    |

Most commands are composed by combining these building blocks.

For example:

```text
[count] operator [count] motion
```

or simply:

```text
motion
```

or

```text
action
```

---

# Motions

A motion is responsible only for moving the cursor.

Motions **never modify the playlist** or affect playback. Their only purpose is to define a destination.

## Available motions

| Motion | Description                           |
| ------ | ------------------------------------- |
| `j`    | Move to the next item                 |
| `k`    | Move to the previous item             |
| `gg`   | Jump to the beginning of the playlist |
| `G`    | Jump to the end of the playlist       |

---

## Motion counts

Most motions accept a numeric count placed before the motion. If no count is provided, the default value is always 1.

So:

```text
j
```

Is equivalent to:

```text
1j
```

It moves the cursor down one item.

---

```text
3j
```

Moves the cursor down three items.

---

```text
5k
```

Moves the cursor up five items.

---

```text
10gg
```

Moves the cursor directly to item **10**.

It's also equivalent to:

```text
10G
```

---

## Summary

| Command | Result                            |
| ------- | --------------------------------- |
| `j`     | Move down one item                |
| `k`     | Move up one item                  |
| `5j`    | Move down five items              |
| `3k`    | Move up three items               |
| `gg`    | Jump to the beginning of the list |
| `G`     | Jump to the end of the list       |
| `10gg`  | Jump to item number 10            |
| `10G`   | Jump to item number 10            |

---

# Operators

Operators perform actions on playlist items. Unlike motions, operators modify the playlist.

An operator always acts on a **target**, and that target is normally defined by a motion.

The general pattern is:

```text
operator + motion
```

Currently Vi-Player provides two operators:

| Operator | Description           |
| -------- | --------------------- |
| `d`      | Delete playlist items |
| `y`      | Copy playlist items   |

---

## Operator + Motion

The simplest form combines an operator with a motion.

Example:

```text
dj
```

It's equivalent to:

```text
delete + move one item down
```

Result:
Current item and next item removed.

---

```text
dk
```

Deletes current item and previous item

---

```text
dG
```

Deletes everything from the current position to the end of the playlist.

---

```text
d2j
```

It's equivalent to:

```text
delete + move two items
```

Result:
Current item plus the next two items are deleted.

---

## Operator counts

Operators also accept counts.

Just like motions, if omitted, the default count is 1.

Example:

```text
2dd
```

Deletes two consecutive items.

---

```text
4yy
```

Yanks (copies) four consecutive items.

---

## Operator repetition

A special case occurs when an operator receives itself as its argument.

```text
dd
```

Deletes only the current item.

Likewise:

```text
yy
```

Copies only the current item.

---

## Combining operator and motion counts

Both operators and motions can receive independent counts.

General syntax:

```text
[count] operator [count] motion
```

Examples:

```text
d3j
```

Delete the current item and the next three.

---

```text
3dd
```

Delete three consecutive items.

---

```text
2yy
```

Copy two consecutive items.

---

```text
2d3j
```

Combines both operator and motion counts.

The motion defines the range, while the operator count expands the operation according to the command grammar.

---

## Understanding the difference

Although these commands may produce similar results, they are interpreted differently.

### Motion count

```text
d2j
```

Meaning:

```text
delete + move two items
```

The motion is evaluated first, producing a range. The operator is then applied to that range.

---

### Operator count

```text
2dj
```

Means:

```text
operator count = 2

motion = j
```

The operator count extends the operation while keeping the original motion.

Both commands may affect the same number of items depending on the situation, but they are parsed differently.

---

# Registers

Both `d` and `y` store their result in the playlist register.

The register behaves like a clipboard.

Current behavior:

* `d` deletes and copies.
* `y` copies without deleting.
* `p` pastes the register contents.
* Each new operation replaces the previous register contents.

Example:

```text
yy
```

Copy current item.

```text
p
```

Paste copied items.

---

# Actions

Actions execute immediately.

Unlike motions and operators, they:

* do not accept counts;
* cannot be combined with motions;
* cannot be combined with operators.

Current actions:

| Action | Description                                 |
| ------ | ------------------------------------------- |
| `h`    | Seek backward 5 seconds of the playing song |
| `l`    | Seek forward 5 seconds of the playing song  |
| `H`    | Go to the beginning of the song             |
| `L`    | Skip to the end of the song                 |
| `m`    | Mute player                                 |
| `n`    | Skips to the next song                      |
| `N`    | Go back to the previous song                |
| `:`    | Enter Command mode                          |
| `q`    | Quit Vi-Player                              |
| `p`    | Paste register contents                     |

