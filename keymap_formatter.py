from copy import copy

config_path = "config.txt"


def get_keymap_path() -> list[str]:
    with open(config_path) as f:
        return f.readlines()


def get_keymap(keymap_path: str) -> list[str]:
    with open(keymap_path) as f:
        return f.readlines()


def get_indices_of_layer(keymap: list[str]) -> list[tuple[int, int]]:
    is_in_keymap = False
    is_in_layer = False
    start = 0
    end = 0
    res = []
    for i, line in enumerate(keymap):
        if not is_in_keymap:
            if "keymap {" in line:
                is_in_keymap = True
            else:
                continue
        else:
            if not is_in_layer:
                if "{" in line:
                    is_in_layer = True
                    start = i + 2
                else:
                    continue
            else:
                if "}" in line:
                    end = i - 2
                    res.append((start, end))
                    is_in_layer = False
                else:
                    continue

    return res


def words(line: str) -> list[str]:
    return [w for w in line.split(" ") if w != ""]


def join_words(words: list[str]) -> list[str]:
    res = []
    word = ""
    for w in words:
        if "&" in w:
            res.append(word)
            word = w
        else:
            word += " " + w
        if "\n" in w:
            res.append(word)
    return res[1:]


EMPTY = "&&"


def add_empty_command(commands: list[str]) -> list[str]:
    # 5+5->5+e*4+e*4+5
    # 6+6->6+e*3+e*3+6
    # 6+6->6+e*3+e*3+6
    # 6+6->6+e*3+e*3+6
    # 9+9
    # 8+8->5+e+3+3+e+5
    if len(commands) == 10:
        return commands[0:5] + [EMPTY] * 8 + commands[5:]
    if len(commands) == 12:
        return commands[0:6] + [EMPTY] * 6 + commands[6:]
    if len(commands) == 18:
        return commands
    if len(commands) == 16:
        return commands[0:5] + [EMPTY] + commands[5:11] + [EMPTY] + commands[11:]
    assert False


def add_indent_head(commands: list[str]) -> list[str]:
    return [" "] * 12 + commands


def add_space(commands: list[str]) -> list[str]:
    max_len = max([len(command) for command in commands])

    def _add_space(command: str) -> str:
        if len(command) < max_len:
            return command + " " * (max_len - len(command))
        return command

    return [_add_space(command) for command in commands]


def remove_empty_marker(command: str) -> str:
    if EMPTY + " " in command:
        return command.replace(EMPTY, " " * 2)
    return command


def format(lines: list[str]) -> list[str]:
    commands = [add_empty_command(join_words(words(line))) for line in lines]
    spaced_commands = [
        add_space([command[i] for command in commands]) for i in range(len(commands[0]))
    ]
    new_commands = [
        [remove_empty_marker(sc[i]) for sc in spaced_commands]
        for i in range(len(spaced_commands[0]))
    ]
    fixed_new_commands = [
        command[:17] + [command[17].strip() + "\n"] for command in new_commands
    ]
    indented_commands = [add_indent_head(command) for command in fixed_new_commands]
    joined_commands = [" ".join(command) for command in indented_commands]

    return joined_commands


def get_new_keymap(
    keymap: list[str], layer_indices: list[tuple[int, int]]
) -> list[str]:
    new_keymap = copy(keymap)

    def replace(start: int, end: int):
        formatted_lines = format(keymap[start : end + 1])
        for i, line in enumerate(formatted_lines):
            new_keymap[i + start] = line

    for start, end in layer_indices:
        replace(start, end)
    return new_keymap


def write(keymap: list[str], path):
    with open(path, mode="w") as f:
        f.writelines(keymap)


paths = get_keymap_path()
keymap_path = paths[0].strip()
new_keymap_path = paths[1].strip()
keymap = get_keymap(keymap_path)
layer_indices = get_indices_of_layer(keymap)
new_keymap = get_new_keymap(keymap, layer_indices)
write(new_keymap, new_keymap_path)
