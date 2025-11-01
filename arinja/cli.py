"""CLI interface for arinja."""

import typer
import webbrowser
import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from typing import Optional, Union
from . import news, db

app = typer.Typer(help="Arinja: AI-powered terminal news bot.", add_completion=False)
console = Console()

CATEGORIES = ['technology', 'business', 'sports', 'entertainment', 
             'science', 'health', 'world', 'india']

def show_welcome():
    """Show welcome message with available commands."""
    console.print(Panel(
        "[bold green]Welcome to Arinja![/bold green]\n\n"
        "Your personal AI-powered news assistant.\n"
        f"Current time (IST): {news.get_current_ist_time().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        "[bold]Available Categories:[/bold]\n"
        "🔧 [cyan]technology[/cyan]  💼 [cyan]business[/cyan]  ⚽ [cyan]sports[/cyan]\n"
        "🎬 [cyan]entertainment[/cyan]  🔬 [cyan]science[/cyan]  🏥 [cyan]health[/cyan]\n"
        "🌍 [cyan]world[/cyan]  🇮🇳 [cyan]india[/cyan]\n\n"
        "[dim]Commands:[/dim]\n"
        "[dim]• arinja <category> - Show headlines for category[/dim]\n"
        "[dim]• arinja <id> - Show full article[/dim]\n"
        "[dim]• arinja fetch [--from YYYY-MM-DD] [--to YYYY-MM-DD] - Update news database[/dim]\n"
        "[dim]• arinja source <id> - Show article source[/dim]\n"
        "[dim]• arinja open <id> - Open article in browser[/dim]",
        title="[green]arinja[/green]",
        border_style="green"
    ))

@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    target: str = typer.Argument(None, help="Category name or article ID"),
):
    """Arinja news bot - show headlines by category or article by ID."""
    if not ctx.invoked_subcommand:
        if target is None:
            show_welcome()
            return

        # Try parsing as article ID first
        try:
            article_id = int(target)
            show_article(article_id)
            return
        except ValueError:
            pass

        # Handle category
        if target.lower() in CATEGORIES:
            show_category_news(target.lower())
        else:
            console.print(Panel(
                "Invalid category. Available categories:\n"
                "• technology   • business   • sports\n"
                "• entertainment   • science   • health\n"
                "• world   • india",
                title="[red]Error[/red]",
                border_style="red"
            ))

@app.command()
def fetch(
    from_date: str = typer.Option(None, "--from", help="Start date (YYYY-MM-DD)"),
    to_date: str = typer.Option(None, "--to", help="End date (YYYY-MM-DD)")
):
    """Fetch and index latest news."""
    try:
        # Parse dates if provided
        start_date = None
        end_date = None
        
        if from_date:
            start_date = datetime.datetime.strptime(from_date, "%Y-%m-%d").date()
        if to_date:
            end_date = datetime.datetime.strptime(to_date, "%Y-%m-%d").date()
        
        # Validate date range
        if start_date and end_date and end_date < start_date:
            console.print("[red]Error: End date cannot be before start date[/red]")
            raise typer.Exit(1)
        
        # Check if dates are in the future
        today = datetime.datetime.now().date()
        if (start_date and start_date > today) or (end_date and end_date > today):
            console.print("[red]Error: Dates cannot be in the future[/red]")
            raise typer.Exit(1)
            
        _fetch(from_date=start_date, to_date=end_date)
        
    except ValueError as e:
        console.print("[red]Error: Invalid date format. Use YYYY-MM-DD[/red]")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        raise typer.Exit(1)

@app.command()
def source(
    article_id: int = typer.Argument(..., help="Article ID to show source for")
):
    """Show article source information."""
    show_source(article_id)

@app.command()
def open(
    article_id: int = typer.Argument(..., help="Article ID to open in browser")
):
    """Open article in web browser."""
    open_article(article_id)

def _fetch(from_date: Optional[datetime.date] = None, to_date: Optional[datetime.date] = None):
    """Fetch and index latest news."""
    source = news.NewsSource(start_date=from_date, end_date=to_date)
    
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
        articles = []
        date_range = f" ({from_date} to {to_date})" if from_date and to_date else ""
        task = progress.add_task(f"Fetching news{date_range}...", total=None)
        
        for category in CATEGORIES:
            progress.update(task, description=f"Fetching {category} news...")
            cat_articles = source.fetch_headlines(category)
            articles.extend(cat_articles)
        
        progress.update(task, description="Storing articles...")
        article_ids = db.store_articles(articles)
    
    console.print(Panel(
        f"✓ Fetched {len(articles)} articles\n"
        f"✓ New/updated articles: {len(article_ids)}",
        title="[green]Update Complete[/green]",
        border_style="green"
    ))

def show_category_news(category: str):
    """Show headlines for a specific category."""
    articles = db.get_articles(category=category.lower())
    if not articles:
        console.print(Panel(
            f"No articles found for category: {category}",
            border_style="red"
        ))
        return
    
    icon = {
        'technology': '🔧', 'business': '💼', 'sports': '⚽',
        'entertainment': '🎬', 'science': '🔬', 'health': '🏥',
        'world': '🌍', 'india': '🇮🇳'
    }.get(category.lower(), '📰')
    
    console.print(f"\n[bold green]{icon} {category.upper()}[/bold green]")
    for article in articles:
        date = article['published_at'].strftime('%Y-%m-%d') if article.get('published_at') else ''
        console.print(f"[white]#{article['id']} {date} | {article['title']}[/white]")
    
    console.print("\n[dim]Use 'arinja <id>' to see article content[/dim]")

def show_source(id: int):
    """Show article source and URL."""
    article = db.get_article_by_id(id)
    if not article:
        console.print(Panel(f"Article {id} not found", border_style="red"))
        return
    
    console.print(Panel(
        f"[bold]Source:[/bold] {article['source']}\n"
        f"[bold]URL:[/bold] {article['url']}",
        title=f"[green]#{id} Source Info[/green]",
        border_style="green"
    ))

def open_article(id: int):
    """Open article URL in default web browser."""
    article = db.get_article_by_id(id)
    if not article:
        console.print(Panel(f"Article {id} not found", border_style="red"))
        return
    
    try:
        webbrowser.open(article['url'])
        console.print(Panel(
            "Opening article in your default web browser...",
            title="[green]Opening Article[/green]",
            border_style="green"
        ))
    except Exception as e:
        console.print(Panel(
            f"Failed to open URL: {str(e)}",
            title="[red]Error[/red]",
            border_style="red"
        ))

def show_article(id: int):
    """Show full article content."""
    article = db.get_article_by_id(id)
    if not article:
        console.print(Panel(f"Article {id} not found", border_style="red"))
        return
    
    date = article['published_at'].strftime('%Y-%m-%d') if article.get('published_at') else 'N/A'
    
    console.print(Panel(
        f"[bold]{article['title']}[/bold]\n\n"
        f"[dim]Date: {date} | Category: {article['category'].title()}[/dim]\n\n"
        + article['content'] + "\n\n"
        f"[dim]Source: {article['source']}[/dim]\n"
        f"[dim]URL: {article['url']}[/dim]",
        title=f"[green]#{id}[/green]",
        border_style="green"
    ))

if __name__ == "__main__":
    app()