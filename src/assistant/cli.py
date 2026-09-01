import argparse

from assistant.core.agent import AssistantCore


def main() -> None:
    parser = argparse.ArgumentParser(prog="assistant")
    sub = parser.add_subparsers(dest="command", required=True)

    add = sub.add_parser("add", help="Create a task")
    add.add_argument("title")
    add.add_argument("--minutes", type=int, default=30)

    args = parser.parse_args()
    core = AssistantCore()

    if args.command == "add":
        task = core.create_task(args.title, estimated_minutes=args.minutes)
        print(f"Created {task.id}: {task.title} ({task.estimated_minutes} min)")


if __name__ == "__main__":
    main()
