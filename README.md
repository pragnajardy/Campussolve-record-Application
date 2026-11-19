# CampusSolve — Library Record Application

A beginner-friendly, zero-dependency Python 3.10+ terminal application for managing library books, members, issue/return transactions, and executive summaries.

## Features
- Menu-driven terminal interface with defensive input validation.
- Add books and members; issue and return books with inventory tracking.
- Prevent duplicate ISBNs/emails, invalid IDs, unavailable stock, duplicate active issues, and past due dates.
- Persistent local JSON database (`data/library.json`) with atomic saves and recovery backup for malformed data.
- Keyword/category book search, overdue alerts, executive metrics, and report exports (Markdown, TXT audit log, CSV transactions).
- Standard-library unit tests.

## Run in VS Code
1. Extract the project ZIP.
2. Open the `CampusSolve_Library_Record_Application` folder in VS Code.
3. Ensure Python 3.10 or newer is installed. No pip packages are required.
4. Open Terminal → New Terminal.
5. Run:

   ```bash
   python main.py
   ```

   On some Windows systems use `py main.py`.

## First demo workflow
1. Choose `1` and add a book. Try entering an invalid number to demonstrate validation.
2. Choose `2` and register a member.
3. Choose `3` to issue the book (use its displayed Book ID and Member ID).
4. Choose `8` to show analytics and `9` to check overdue alerts.
5. Choose `10` to export reports into the `reports/` folder.
6. Choose `0`, relaunch the app, and verify that records remain.

## Run tests
From the project root:

```bash
python -m unittest discover -s tests -v
```

## Data files
- `data/library.json`: live application database. It is created automatically on first launch.
- `data/sample_books.csv`: sample book catalogue.
- `data/sample_members.csv`: sample member list.
- `data/sample_transactions.csv`: sample transaction list.
- `data/sample_dataset.json`: 40 realistic sample records across books, members, and transactions.

Sample files are for demonstration/reference; the application starts with a clean database so you can perform a live demo without confusing preloaded data. You may copy sample data into `data/library.json` if you want a populated demonstration, ensuring the three top-level arrays are retained.

## Project structure

```text
CampusSolve_Library_Record_Application/
├── main.py
├── library_app/
│   ├── __init__.py
│   ├── cli.py
│   ├── core.py
│   ├── reports.py
│   ├── storage.py
│   └── validators.py
├── data/
│   ├── library.json
│   ├── sample_books.csv
│   ├── sample_members.csv
│   ├── sample_transactions.csv
│   └── sample_dataset.json
├── reports/
├── tests/
│   └── test_core.py
└── README.md
```

## Notes
- The current app uses JSON as its operational database and provides CSV report export. CSV sample datasets are included for the requested legacy-data demonstration.
- Late fees are intentionally not calculated because the brief does not specify a fine policy.
