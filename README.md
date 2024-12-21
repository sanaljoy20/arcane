# ARCANE

**Audit for Reliable Coding and Adherence to Norms and Efficiency**

## Overview
ARCANE is a Python-based tool designed to assist developers by:
- Properly documenting R and Python programming files using Large Language Models (LLMs).
- Detecting potential issues or inefficiencies in the code.

The tool integrates a Python Dash application as the user interface, providing an intuitive platform for interacting with its features.

## Features
- **Code Documentation**: Automatically generates comprehensive and accurate comments for R and Python scripts.
- **Issue Detection**: Identifies potential issues, bugs, or inefficiencies in the code and provides actionable recommendations.
- **User-Friendly Interface**: Built using Python Dash, the application offers a clean and responsive UI.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/arcane.git
   cd arcane/via-chat-gpt

   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   venv/Scripts/activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up OPENAI_API_KEY in .env file

## Usage
1. Start the ARCANE application:
   ```bash
   python app.py
   ```

2. Open the application in your web browser by navigating to:
   ```
   http://127.0.0.1:8050/
   ```

3. Upload R or Python files and let ARCANE:
   - Automatically document your code.
   - Highlight potential issues.