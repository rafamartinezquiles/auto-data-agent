# main.py
#Here the first dependencies are for the backend
from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

#These bellow dependencies are for plot generation
import pandas as pd
import matplotlib.pyplot as plt # infuture I will use plotly
import itertools
import os
import zipfile
from io import BytesIO

# Initializing FastAPI and setup paths
app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Directory to save uploads and also the plots 
UPLOAD_FOLDER = "uploads"
PLOTS_FOLDER = "static/plots"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PLOTS_FOLDER, exist_ok=True)

# Homepage for uploading CSV file, later I will create an option for excel files also
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# how to handle file upload, process CSV, and generate plots??
@app.post("/upload", response_class=HTMLResponse)
async def upload_file(request: Request, file: UploadFile = File(...)):
    # Saving uploaded file
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Read CSV and process data with pandas, later I will use polars as it is fast
    df = pd.read_csv(file_path)
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()

    if len(numeric_cols) < 2:
        return HTMLResponse("Dataset needs at least two numerical columns for plotting.")

    # plots nust be Clear after every use  
    for plot_file in os.listdir(PLOTS_FOLDER):
        os.remove(os.path.join(PLOTS_FOLDER, plot_file))

    # Generating plots for each pair of numerical columns
    column_pairs = list(itertools.permutations(numeric_cols, 2))
    for x_var, y_var in column_pairs:
        create_all_plots(df, x_var, y_var)

    # Rendering the template with the list of generated plots
    plot_images = [f"/static/plots/{plot}" for plot in os.listdir(PLOTS_FOLDER)]
    return templates.TemplateResponse("index.html", {"request": request, "plot_images": plot_images})

# Function to create and save all types of plots for given pairs of numerical columns. Later I will increase the variety of plots
def create_all_plots(df, x_var, y_var):
    plt.figure(figsize=(10, 6)) 
    plt.plot(df[x_var], df[y_var], marker='o', color='b', linestyle='-', linewidth=1, markersize=5)
    plt.xlabel(x_var)
    plt.ylabel(y_var)
    plt.title(f"Line Plot of {y_var} by {x_var}")
    plot_path = os.path.join(PLOTS_FOLDER, f"{x_var}_by_{y_var}_line.png")
    plt.savefig(plot_path)
    plt.close()

    # Scatter Plot
    plt.figure(figsize=(10, 6))
    plt.scatter(df[x_var], df[y_var], color='purple', alpha=0.6, edgecolor='k', s=100)
    plt.xlabel(x_var)
    plt.ylabel(y_var)
    plt.title(f"Scatter Plot of {y_var} by {x_var}")
    plot_path = os.path.join(PLOTS_FOLDER, f"{x_var}_by_{y_var}_scatter.png")
    plt.savefig(plot_path)
    plt.close()

    # Bar Plot
    plt.figure(figsize=(10, 6))
    plt.bar(df[x_var], df[y_var], color='skyblue', edgecolor='black')
    plt.xlabel(x_var)
    plt.ylabel(y_var)
    plt.title(f"Bar Plot of {y_var} by {x_var}")
    plt.xticks(rotation=45, ha='right')
    plot_path = os.path.join(PLOTS_FOLDER, f"{x_var}_by_{y_var}_bar.png")
    plt.savefig(plot_path)
    plt.close()

    # Histogram
    plt.figure(figsize=(10, 6))
    plt.hist(df[x_var], bins=20, alpha=0.5, label=x_var, color='skyblue', edgecolor='black')
    plt.hist(df[y_var], bins=20, alpha=0.5, label=y_var, color='salmon', edgecolor='black')
    plt.xlabel("Value")
    plt.title(f"Histogram of {x_var} and {y_var}")
    plt.legend()
    plot_path = os.path.join(PLOTS_FOLDER, f"{x_var}_by_{y_var}_hist.png")
    plt.savefig(plot_path)
    plt.close()

# Route to download all plots as a ZIP file
@app.get("/download_plots")
async def download_plots():
    zip_filename = "plots.zip"
    zip_path = os.path.join(UPLOAD_FOLDER, zip_filename)
    with zipfile.ZipFile(zip_path, "w") as zipf:
        for plot_file in os.listdir(PLOTS_FOLDER):
            zipf.write(os.path.join(PLOTS_FOLDER, plot_file), plot_file)
    return FileResponse(zip_path, filename=zip_filename, media_type="application/zip")
