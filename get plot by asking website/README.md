# Get Plot By Asking Webapp

This FastAPI application allows users to upload a CSV dataset, generates various types of graphs based on numerical columns, and displays the graphs on a web interface. Users can also download all the generated graphs.

---

## Features
- Upload CSV datasets via the web interface.
- Automatically identifies numerical columns.
- Generates multiple plot types: line plot, scatter plot, bar chart, histogram, pie chart, and contour plot.
- Provides a download option for all generated plots as a ZIP file.

---

## Requirements
- Python 3.9 or higher
- pip (Python package manager)

---

## Installation and Running Locally

### 1. Clone the Repository
Download the project files to your local machine, change your path to the folder, open terminal

```bash
python3 -m venv venv
source venv/bin/activate  
pip install -r requirements.txt

```
- also you can use anaconda distribution, it makes easier but installs many things which might not be necessary

## Run Application

```bash 
uvicorn main:app --reload
```

Let me know if you need any help
