# Arinja - Terminal News Bot 📰

Arinja is a powerful terminal-based news aggregator that brings you the latest news from various categories right in your terminal. Built with Python and powered by the GNews API, it offers a clean, efficient interface for staying updated with global and Indian news.

## Features 🌟

- 📱 Terminal-first interface with rich formatting
- 🗃️ PostgreSQL database for persistent storage
- 🔍 Multiple news categories support:
  - 🔧 Technology
  - 💼 Business
  - ⚽ Sports
  - 🎬 Entertainment
  - 🔬 Science
  - 🏥 Health
  - 🌍 World
  - 🇮🇳 India
- 📅 Date-based news fetching
- 🔗 Direct article opening in browser
- 🕒 IST timezone support

## Installation 🚀

1. Clone the repository:
\`\`\`bash
git clone https://github.com/Vishnudrm/arinja.git
cd arinja
\`\`\`

2. Install dependencies using Poetry:
\`\`\`bash
poetry install
\`\`\`

3. Set up PostgreSQL database and create a \`.env\` file:
\`\`\`bash
cp config/config.example.env config/config.env
# Edit config.env with your PostgreSQL credentials
\`\`\`

4. Initialize the database:
\`\`\`bash
poetry run python scripts/init_db.py
\`\`\`

5. Make the command globally available:
\`\`\`bash
mkdir -p ~/.local/bin
ln -sf "$(pwd)/scripts/arinja" ~/.local/bin/arinja
\`\`\`

## Usage 💻

### Basic Commands

\`\`\`bash
# Show help and categories
arinja

# Read news by category
arinja technology    # Show technology news
arinja business      # Show business news
arinja india        # Show India news

# Read specific article
arinja 1234         # Show article #1234

# Article actions
arinja source 1234  # Show article source
arinja open 1234    # Open in browser

# Update news database
arinja fetch                                        # Fetch latest news
arinja fetch --from 2025-10-30 --to 2025-10-31    # Fetch news for specific dates
\`\`\`

### Setting up Daily Updates

Add to crontab to fetch news daily:
\`\`\`bash
0 10 * * * cd /path/to/arinja && poetry run arinja fetch
\`\`\`

## Configuration ⚙️

Configure in \`config/config.env\`:
\`\`\`env
POSTGRES_URI=postgresql://user:password@localhost:5432/arinja
\`\`\`

## Dependencies 📦

- Python 3.8+
- PostgreSQL
- Required Python packages (installed via Poetry):
  - typer
  - rich
  - gnews
  - psycopg2-binary
  - python-dotenv
  - pytz

## Project Structure 📁

\`\`\`
arinja/
├── arinja/
│   ├── __init__.py    # Package initialization
│   ├── cli.py         # CLI interface
│   ├── db.py          # Database operations
│   └── news.py        # News fetching logic
├── config/
│   ├── config.env
│   └── config.example.env
├── scripts/
│   ├── arinja         # Global command script
│   └── init_db.py     # Database initialization
├── LICENSE
└── pyproject.toml
\`\`\`

## Contributing 🤝

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author ✍️

- Vishnudrm
- GitHub: [@Vishnudrm](https://github.com/Vishnudrm)

## Acknowledgments 🙏

- GNews API for news data
- Rich library for terminal formatting
- Typer for CLI interface
