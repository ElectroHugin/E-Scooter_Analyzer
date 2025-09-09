# E-Scooter Data Analyzer

A project to scrape, filter, and sort e-scooter data, available as both an interactive web application and a command-line tool. This tool helps you find the perfect e-scooter based on your specific criteria by analyzing a comprehensive table of available models in Germany.

The data is sourced from the excellent and detailed comparison table at [escooter-treff.de](https://www.escooter-treff.de/tabelle/).

## Web Application (Streamlit)

The easiest way to use the analyzer is through the interactive web application, which offers a modern graphical user interface.

[**>> Try the Live Web App Here <<**](YOUR_STREAMLIT_APP_LINK_HERE)

*(Feel free to add a screenshot of your app here!)*
`![Streamlit App Screenshot](path/to/your/screenshot.png)`

## Features

-   **Interactive Streamlit Web App**: A beautiful, modern web interface with interactive widgets (sliders, dropdowns) for filtering.
-   **Multi-Language Support**: The web app is available in both German and English.
-   **Web Scraping**: Fetches the latest e-scooter data directly from the source.
-   **Data Processing**: Cleans and converts the raw HTML table into a structured pandas DataFrame.
-   **Smart Caching**: Scrapes data only once per day to improve speed and reduce server load.
-   **Interactive CLI**: A user-friendly, menu-driven command-line interface for local analysis.
-   **Powerful Filtering & Sorting**: Both the web app and CLI provide extensive options to narrow down your search.

## Getting Started

Follow these instructions to get a local copy of the project up and running for development or local use.

### Prerequisites

-   Python 3.8+
-   pip (Python package installer)

### Installation

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/ElectroHugin/E-Scooter_Analyzer.git
    cd E-Scooter_Analyzer
    ```

2.  **(Recommended) Create and activate a virtual environment:**
    -   **Windows:**
        ```sh
        python -m venv venv
        .\venv\Scripts\activate
        ```
    -   **macOS / Linux:**
        ```sh
        python3 -m venv venv
        source venv/bin/activate
        ```

3.  **Install the required packages:**
    ```sh
    pip install -r requirements.txt
    ```

## Usage

This project can be run in two ways: as a web application or as a command-line tool.

### 1. Using the Streamlit Web App (Recommended)

To run the web application on your local machine, use the following command from the project's root directory:

```sh
streamlit run app.py
```

Your web browser will automatically open with the application.

### 2. Using the Command-Line Tool

To start the interactive CLI tool, run the `main.py` script:

```sh
python src/main.py
```

Follow the on-screen prompts to filter, sort, and display the e-scooter data in your terminal.

## Project Structure

The project is organized into several modules to ensure a clean and maintainable codebase:

```
escooter-analyzer/
├── .streamlit/
│   └── config.toml         # Theme configuration for Streamlit
├── data/
│   └── escooter_data.csv   # Local cache for the scraped data
├── src/
│   ├── scraper.py          # Handles fetching the HTML and parsing the table
│   ├── data_processor.py   # Cleans the raw data and creates the DataFrame
│   ├── filter_sort.py      # Functions for CLI filtering and sorting
│   ├── main.py             # Entry point for the CLI application
│   └── translations.py     # Language strings for the Streamlit app
├── app.py                  # Entry point for the Streamlit web application
├── .gitignore
├── requirements.txt
└── README.md
```

-   **`app.py`**: The main script for the Streamlit web application.
-   **`main.py`**: The main script for the command-line interface (CLI).
-   **`scraper.py`**: Connects to the website and extracts the raw table data.
-   **`data_processor.py`**: Takes the raw data and prepares it for analysis.
-   **`filter_sort.py`**: A set of functions used by the CLI for data manipulation.
-   **`translations.py`**: Contains the German and English text for the web app.

## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

## License

Distributed under the GNU General Public License v3.0. See the `LICENSE` file for more information.

## Acknowledgments

-   A big thank you to **escooter-treff.de** for creating and maintaining the comprehensive data table that makes this project possible.
-   [Streamlit](https://streamlit.io/) for making it so easy to build beautiful data apps.
-   [Rich](https://github.com/Textualize/rich) for the beautiful terminal formatting in the CLI.
-   [Pandas](https://pandas.pydata.org/) for the powerful data manipulation capabilities.