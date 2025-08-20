import json
import random
import re
from pathlib import Path
from typing import Dict


dice_pattern = re.compile(r'(\d+)d(\d+)')


def roll_expression(expr: str) -> int:
    """Roll a dice expression like "2d6+1d8" and return total."""
    total = 0
    for count, sides in dice_pattern.findall(expr.lower()):
        total += sum(random.randint(1, int(sides)) for _ in range(int(count)))
    return total


class DiceRollStorage:
    """Store and execute named dice roll expressions."""

    def __init__(self, store_path: str = "stored_rolls.json") -> None:
        self.path = Path(store_path)
        if self.path.exists():
            self.rolls = json.loads(self.path.read_text())
        else:
            self.rolls = {}

    def add_roll(self, name: str, expression: str) -> None:
        """Store a new dice roll expression under *name*."""
        self.rolls[name] = expression
        self._save()

    def list_rolls(self) -> Dict[str, str]:
        """Return a copy of stored rolls."""
        return dict(self.rolls)

    def roll(self, name: str) -> int:
        """Execute a stored roll by *name* and return the total."""
        expr = self.rolls.get(name)
        if expr is None:
            raise KeyError(f"No roll stored under '{name}'")
        return roll_expression(expr)

    def _save(self) -> None:
        self.path.write_text(json.dumps(self.rolls, indent=2))


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(
        description="Store and execute prepared dice rolls."
    )
    subparsers = parser.add_subparsers(dest="command")

    add_parser = subparsers.add_parser("add", help="store a new roll expression")
    add_parser.add_argument("name", help="name of the roll")
    add_parser.add_argument("expression", help="dice expression like 2d6+1d8")

    roll_parser = subparsers.add_parser("roll", help="execute a stored roll")
    roll_parser.add_argument("name", help="name of the stored roll")

    subparsers.add_parser("list", help="list stored rolls")

    args = parser.parse_args()
    storage = DiceRollStorage()

    if args.command == "add":
        storage.add_roll(args.name, args.expression)
        print(f"Stored roll '{args.name}': {args.expression}")
    elif args.command == "roll":
        result = storage.roll(args.name)
        print(f"Roll '{args.name}' ({storage.rolls[args.name]}): {result}")
    elif args.command == "list":
        for name, expr in storage.list_rolls().items():
            print(f"{name}: {expr}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
