# E-Scooter Data Analyzer

An interactive Command-Line Interface (CLI) tool to scrape, filter, and sort e-scooter data from the web. This tool helps you find the perfect e-scooter based on your specific criteria by analyzing a comprehensive table of available models in Germany.

The data is sourced from the excellent and detailed comparison table at [escooter-treff.de](https://www.escooter-treff.de/tabelle/).

## Features

-   **Web Scraping**: Fetches the latest e-scooter data directly from the source.
-   **Data Processing**: Cleans and converts the raw HTML table into a structured and typed pandas DataFrame.
-   **Smart Caching**: Scrapes data only once per day and uses a local cache for subsequent runs to improve speed and reduce server load.
-   **Interactive CLI**: A user-friendly, menu-driven interface for data analysis.
-   **Powerful Filtering**:
    -   Filter numeric columns with operators (`<`, `<=`, `>`, `>=`, `==`). (e.g., `gewicht_kg < 20`).
    -   Select specific values from categorical columns (e.g., `reifenart` is `tubeless`).
    -   Filter by boolean flags (e.g., `bremslicht` is `True`).
-   **Flexible Sorting**: Sort the results by any column in either ascending or descending order.
-   **Clean Output**: Displays the resulting data in a beautifully formatted table using the `rich` library.

## Demo

Here is a quick look at the interactive menu in action:

```
$ python src/main.py
✓ Loading data from local cache...
Loaded 171 e-scooters.

E-Scooter Analyzer Menu
[1] Filter Data
[2] Sort Data
[3] Display Current List
[4] Reset to Full List
[5] Exit
Choose an option (1/2/3/4/5): 1

  [0] model (object)
  [1] gewicht_kg (float64)
  [2] reichweite_km_offiziell (float64)
  ...
Enter the number of the column to filter by: 1

Filter 'gewicht_kg' | Enter operator (<, <=, >, >=, ==) [<=]: <=
Enter value: 15
```

## Getting Started

Follow these instructions to get a local copy of the project up and running.

### Prerequisites

-   Python 3.8+
-   pip (Python package installer)

### Installation

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/your-username/escooter-analyzer.git
    cd escooter-analyzer
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

To start the interactive analysis tool, run the `main.py` script from the project's root directory:

```sh
python src/main.py
```

Follow the on-screen prompts to filter, sort, and display the e-scooter data.

## Project Structure

The project is organized into several modules to ensure a clean and maintainable codebase:

```
escooter-analyzer/
├── data/
│   └── escooter_data.csv   # Local cache for the scraped data
├── src/
│   ├── scraper.py          # Handles fetching the HTML and parsing the table
│   ├── data_processor.py   # Cleans the raw data and creates the DataFrame
│   ├── filter_sort.py      # Contains functions for filtering and sorting the DataFrame
│   └── main.py             # The main application entry point and CLI logic
├── .gitignore
├── requirements.txt        # Project dependencies
└── README.md
```

-   **`scraper.py`**: Connects to the website and extracts the raw, unprocessed table data.
-   **`data_processor.py`**: Takes the raw data, cleans column names, converts data types (e.g., "25,5 kg" to a float `25.5`), and prepares it for analysis.
-   **`filter_sort.py`**: A set of pure functions that take a DataFrame and perform a specific filtering or sorting operation.
-   **`main.py`**: Orchestrates the application flow. It handles data loading (with caching), user interaction, and displays the final results.

## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

## License

Distributed under the GNU General Public License v3.0. See the `LICENSE` file for more information.

## Acknowledgments

-   A big thank you to **escooter-treff.de** for creating and maintaining the comprehensive data table that makes this project possible.
-   [Rich](https://github.com/Textualize/rich) for the beautiful terminal formatting.
-   [Pandas](https://pandas.pydata.org/) for the powerful data manipulation capabilities.