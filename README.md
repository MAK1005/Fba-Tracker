# FBA Lost Inventory & Reimbursement Tracker

A project I worked on to track lost Amazon FBA inventory and manage reimbursement claims.

## What it does

- Import shipment data from an audit CSV
- Detect discrepancies between units sent and units received
- Log and track reimbursement claims with status updates
- Generate reports — total value lost, recovery rate, claims by status
- Export claims to CSV ready to submit to Amazon Seller Central
- Backup and restore all data via JSON
- OOP classes for clean data handling

## Tech

Python 3 and SQLite. No external dependencies — just the standard library.

## How to run

```bash
git clone https://github.com/MAK1005/fba-tracker.git
cd fba-tracker
python -m venv venv
venv\Scripts\activate
python main.py
```

## To import shipment data

Create a CSV file with these columns and run the import:

```
Shipment_ID, ASIN, Title, Units_Sent, Units_Received, Date
```

```bash
python csv_import.py
```

## What I want to add next

- Connect to Amazon SP-API to pull shipment data automatically
- Alert system when recovery rate drops below a threshold
- Web interface to manage claims without running scripts

## About

Built this project while learning Python, SQLite databases, and file handling.
