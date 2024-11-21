# AutoDataAgent

AutoDataAgent is a powerful, modular system designed to automate the entire data analysis pipeline — from ingestion to report generation. It leverages open-source AI models and frameworks to streamline task assignment, code generation, debugging, and analysis. This project aims to provide a fully integrated workflow, focusing on efficiency and scalability with minimal manual intervention.

## Key Features

1. **Dataset Ingestion and Preprocessing**  
   - Uses **Pandas** and **NumPy** to handle data formatting, cleaning, and transformation.  
   - Easily extendable to integrate open-source AI models from **Hugging Face** for data handling.

2. **Task Assignment and Workflow Generation**  
   - Employs **GPT-J** to break down analysis into smaller tasks such as data cleaning, statistical evaluation, and machine learning training.  
   - **FastAPI** manages task orchestration, ensuring smooth and organized workflows.

3. **Job Execution and Code Generation**  
   - Utilizes models like **Codex** from Hugging Face to generate Python/SQL code for analytical tasks.  
   - Ensures high efficiency in generating machine-readable code for complex data operations.

4. **Error Handling and Debugging**  
   - Integrates open-source models for automatic error correction and debugging.  
   - In case of complex issues, the system falls back to **OpenAI GPT-4** to analyze logs and suggest detailed solutions.

5. **Result Interpretation and Insights**  
   - Leverages models like **GPT-J** or **Bloom** to summarize results, detect patterns, and generate actionable insights.  

6. **Report Generation**  
   - Uses **GPT-Neo** and **WeasyPrint** for creating reports with visualized data and detailed summaries.  
   - For more complex narratives, integrates higher-level models for advanced reporting capabilities.
7. **Plot Generation from csv files**
   - Uses matplotlib to generate plots when the user uploads csv file
   - plots can be downloaded as .zip file or individually

## Dependencies
- Python 3.8+
- Pandas and NumPy for data manipulation
- Matplotlib for plotting
- FastAPI for task management
- Hugging Face Transformers for model integration
- WeasyPrint for report generation
- OpenAI API (Optional, for complex debugging)


## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any suggestions or bugs you find.

Thanks [Rafael](https://rafamartinezquiles.github.io)'s great work for AutoDataAgent main feature! 

## License

This project is licensed under the MIT License.
