class Commands:
    """
    Utility for preparing a set of commands for using with click
    """

    def __init__(self, commands: dict = None):
        self._commands = commands if commands is not None else dict()

    def add(self, command: str, description: str) -> None:
        self._commands[command] = description

    @property
    def commands(self) -> list[str]:
        return [key for key in self._commands.keys()]

    def help_text(self, column_width: int = 10) -> str:
        retVal = ""
        for command, description in self._commands.items():
            retVal += f"{command:<{column_width}}:{description}\n"
        return retVal


if __name__ == "__main__":
    pre = {"X": "Command X", "Y": "Command Y"}
    cmds = Commands(pre)
    cmds.add("A", "Command A")
    cmds.add("B", "Command B")

    print(cmds.commands)

    print(
        cmds.help_text(),
    )
