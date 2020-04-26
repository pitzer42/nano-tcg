line_break = '\n'
read_command = '$read'


def compile_command(command: str):
    return (command + line_break).encode()


compiled_read_command = compile_command(read_command)


def compile_commands(commands):
    return list(
        map(
            compile_command,
            commands
        )
    )
