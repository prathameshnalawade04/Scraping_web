# 🚀 Django Hybrid Async Scraper

A high-performance web scraper built with **Django 5.0**, **aiohttp**, and **BeautifulSoup**.

This project demonstrates a **Hybrid Architecture** that solves a common Django challenge: it combines standard **Synchronous Views** (for robust security and authentication) with **Asynchronous Python** (for high-speed, non-blocking scraping).

## 🌟 Key Features

* **Hybrid Async/Sync Architecture:** Uses `asgiref.sync.async_to_sync` to bridge secure Django views with fast `asyncio` scraping logic.
* **Non-Blocking Execution:** Fetches URL data in the background using `aiohttp` without freezing the server.
* **Concurrency Control:** Offloads heavy HTML parsing (BeautifulSoup) to separate threads using `asyncio.to_thread`, keeping the event loop free.
* **Smart Data Management:** Custom `ScrapDataManager` implements "Update or Create" logic to prevent duplicate database entries.
* **Secure:** Fully protected by Django's standard authentication system (`@login_required`).

## 🛠️ Tech Stack

* **Framework:** Django 5.0+
* **Scraping:** aiohttp (Async HTTP Client)
* **Parsing:** BeautifulSoup4
* **Async Utilities:** asgiref
* **Database:** SQLite (Default) / PostgreSQL (Production ready)

## ⚡ Installation & Setup

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/django-async-scraper.git](https://github.com/YOUR_USERNAME/django-async-scraper.git)
    cd django-async-scraper
    ```

2.  **Create a Virtual Environment**
    ```bash
    python -m venv venv
    # Windows:
    venv\Scripts\activate
    # Mac/Linux:
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Apply Migrations**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5.  **Run the Server**
    ```bash
    python manage.py runserver
    ```

## 🧠 How It Works (The Architecture)

1.  **The View (`views.py`):** A standard Synchronous Django view handles the request. This ensures `@login_required` works perfectly and securely.
2.  **The Bridge:** The view calls `async_to_sync(run_scraper)(url)`. This helper pauses the sync view, runs the async scraper on the event loop, and waits for the result.
3.  **The Network Layer (`aiohttp`):** The scraper fetches the HTML asynchronously, allowing for concurrent requests.
4.  **The CPU Layer (`to_thread`):** Since HTML parsing is CPU-bound, we wrap the BeautifulSoup logic in `asyncio.to_thread`. This runs parsing in a separate thread so the main Async Event Loop is never blocked.

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
