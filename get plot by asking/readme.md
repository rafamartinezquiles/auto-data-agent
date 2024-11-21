# Get Plot By Asking

This program enables you to generate bar plots by simply answering prompts. After uploading a dataset, it will display the available features and guide you in selecting numerical variables for plotting. Ensure that variable names are correctly labeled for optimal results.

## Installation

First, install the necessary dependencies using the `requirements.txt` file:

```bash
pip install -r requirements.txt

python -m spacy download en_core_web_sm

```

# Usage
Upload Dataset: The program will prompt you to upload your dataset.
Choose Variables: Once the dataset is loaded, it will list the available features. Select the numerical variables you wish to plot.
Generate Plot: A bar plot based on your input will be generated and displayed.
# Dependencies
spaCy: For processing language-based interactions.
Pandas: For data manipulation and analysis.
Matplotlib: To create and customize bar plots.
# Notes
Ensure your dataset is in a format compatible with pandas.
Choose only numerical variables for accurate plotting.
Please check the jupyter notebook for using it via google colab
Enjoy interactive plotting by just answering a few questions!



