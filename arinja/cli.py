import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from . import news

app = typer.Typer(help="Arinja: AI-powered terminal news bot.", add_completion=False)
console = Console(theme=None)

def show_welcome():
    """Show welcome message and top stories."""
    welcome = Panel(
        "[bold green]Welcome to Arinja![/bold green]\n\n"
        "Your personal AI-powered news assistant.\n"
        f"Current time (IST): {news.get_current_ist_time().strftime('%Y-%m-%d %H:%M:%S')}\n",
        title="[green]arinja[/green]",
        border_style="green"
    )
    console.print(welcome)

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """Arinja - Your AI-powered news assistant."""
    if ctx.invoked_subcommand is None:
        show_welcome()
        # This will automatically fetch news in the future
        fetch()

@app.command()
def fetch():
    """Fetch and index latest news."""
    console.print("[green]Fetching news... (not yet implemented)")

@app.command()
def today(category: str = typer.Option(None, help="News category"), limit: int = typer.Option(20, help="Number of articles")):
    """Show today's news by category."""
    console.print(f"[green]Today's news (category={category}, limit={limit}) (not yet implemented)")

@app.command()
def search(query: str, from_date: str = typer.Option(None), to_date: str = typer.Option(None)):
    """Search news by keyword and date range."""
    console.print(f"[green]Searching for '{query}' from {from_date} to {to_date} (not yet implemented)")

@app.command()
def open(id: int):
    """Show full article by ID."""
    console.print(f"[green]Opening article {id} (not yet implemented)")

@app.command()
def star(id: int, tags: str = typer.Option(None), note: str = typer.Option(None)):
    """Bookmark/star an article with tags and note."""
    console.print(f"[green]Starred article {id} (tags={tags}, note={note}) (not yet implemented)")

@app.command()
def stars(since: str = typer.Option(None)):
    """List starred/bookmarked articles."""
    console.print(f"[green]Listing stars since {since} (not yet implemented)")

@app.command()
def highlight(id: int):
    """Highlight snippet(s) in an article."""
    console.print(f"[green]Highlighting in article {id} (not yet implemented)")

@app.command()
def export(
    pdf: bool = typer.Option(False, help="Export as PDF"),
    stars: bool = typer.Option(False, help="Export starred articles"),
    from_date: str = typer.Option(None),
    to_date: str = typer.Option(None),
    outfile: str = typer.Option(None)
):
    """Export news/bookmarks as PDF."""
    console.print(f"[green]Exporting (pdf={pdf}, stars={stars}, from={from_date}, to={to_date}, outfile={outfile}) (not yet implemented)")

@app.command()
def chat():
    """Conversational Q&A over news."""
    console.print("[green]Chat mode (not yet implemented)")

@app.command()
def tui():
    """Launch interactive terminal UI."""
    console.print("[green]TUI mode (not yet implemented)")

if __name__ == "__main__":
    app()