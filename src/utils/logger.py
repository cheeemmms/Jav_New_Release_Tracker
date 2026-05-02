from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt

_console = Console(force_terminal=False)


def log_info(msg):
    _console.print(f"[dim][INFO][/dim] {msg}")


def log_success(msg):
    _console.print(f"[bold green][OK][/bold green] {msg}")


def log_warning(msg):
    _console.print(f"[bold yellow][WARN][/bold yellow] {msg}")


def log_error(msg):
    _console.print(f"[bold red][ERR][/bold red] {msg}")


def log_title(msg):
    _console.print()
    _console.print(Panel(Text(msg, style="bold white"), border_style="cyan"))
    _console.print()


def ask_choice(question, choices):
    _console.print(f"\n[bold]{question}[/bold]")
    for idx, label in enumerate(choices, 1):
        _console.print(f"  [cyan]{idx}.[/cyan] {label}")
    while True:
        answer = Prompt.ask("请输入序号", default="1")
        if answer.isdigit() and 1 <= int(answer) <= len(choices):
            return int(answer)
        _console.print(f"[red]请输入 1-{len(choices)} 之间的数字[/red]")


def ask_date(prompt_text):
    import arrow
    while True:
        raw = Prompt.ask(f"[bold]{prompt_text}[/bold] (YYYY-MM-DD)")
        try:
            arrow.get(raw, "YYYY-MM-DD")
            return raw
        except Exception:
            _console.print("[red]日期格式错误，请使用 YYYY-MM-DD[/red]")
