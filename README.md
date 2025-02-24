# FastAPI Project

A simple FastAPI project demonstrating various API endpoints with data handling and testing.

## Table of Contents

- [Project Overview](#project-overview)
- [Installation Instructions](#installation-instructions)
- [Run the Project](#run-the-project)
- [API Endpoints](#api-endpoints)
  - [GET /](#get-root)
  - [GET /data](#get-all-data)
  - [GET /data/country/{country_code}](#get_data_by_country)
- [Testing](#testing)
- [Documentation](#documentation)

---

## Project Overview

This project is built with **FastAPI** and demonstrates basic CRUD functionality with file handling and testing:

- Serving static data from an Excel file (`TestData.xlsx` located in the `/uploads` folder).
- Reusable functions for filtering and data handling.
- Exception handling for missing files or invalid data.
- Unit testing using **pytest**.

---

## Installation Instructions

### Prerequisites

Before you begin, make sure you have Python 3.7+ installed.

### Step 1: Create a Virtual Environment

- Create a virtual environment to keep dependencies isolated.

```bash
python -m venv testApi
```
# fastApi_backend
