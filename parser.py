def parse_input(user_input: str):
    cmd, *args = user_input.split()
    cmd = cmd.lower()
    return cmd, *args
