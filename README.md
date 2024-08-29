# Playwright Test Suite

This repository contains a suite of Playwright tests for an online poker platform. The tests cover user registration, login, and game functionality.

## Prerequisites

Ensure you have Python 3.11 or higher installed on your system.

## Installation

To set up the testing environment, follow these steps:

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-repository-url.git
   cd your-repository-folder
   
2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. **Install Dependencies**
   ```bash
   pip install pytest-playwright==0.5.1
   pip install playwright==1.46.0
   playwright install chromium

4. **Run the tests**
   ```bash
    pytest
