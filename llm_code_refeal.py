import openai
import paramiko
import json
import pandas as pd

# Initialize your API key
openai.api_key = "sk-REDACTED"

# Generate code using LLM
def generate_code(prompt, model="gpt-3.5-turbo"):
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful coding assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150,
        temperature=0.5
    )
    return response['choices'][0]['message']['content'].strip()

# Function to analyze the error log and regenerate the task prompt if needed
def analyze_and_regenerate(error_log, task_prompt):
    if "KeyError: 'quantity'" in error_log:
        print("Error detected: Missing 'quantity' column.")
        # Adjust the prompt to handle missing columns
        task_prompt = "The previous code failed due to a missing 'quantity' column. Generate new code that checks for missing columns and handles them appropriately."
    elif "NaN" in error_log or not error_log:
        print("Error detected: Incomplete or missing output.")
        # Adjust the prompt for incomplete results
        task_prompt = "The previous code did not produce complete results. Generate new code that checks for missing or incomplete data and handles it properly."

    return task_prompt

# Function to store results in a structured format (JSON or CSV)
def store_results(results, file_format="json"):
    if file_format == "json":
        with open('results.json', 'w') as f:
            json.dump(results, f)
        print("Results saved in results.json")
    elif file_format == "csv":
        # Convert the results into a DataFrame and save as CSV
        df = pd.DataFrame(results)
        df.to_csv('results.csv', index=False)
        print("Results saved in results.csv")

# Function to prepare data for the next LLM task
def prepare_for_next_llm(results, step="data analysis"):
    workflow_data = {
        "step": step,
        "status": "completed",
        "results": results
    }
    # Save the workflow data for interpretation by the next LLM
    with open('workflow_results.json', 'w') as f:
        json.dump(workflow_data, f)
    print("Workflow results prepared for the next LLM in workflow_results.json")

# Function to execute code on EC2
def execute_code_on_ec2(code, EC2_HOST, EC2_USER, EC2_KEY_FILE):
    try:
        # Create SSH client
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=EC2_HOST, username=EC2_USER, key_filename=EC2_KEY_FILE)

        # Transfer the script to EC2
        sftp_client = ssh_client.open_sftp()
        sftp_client.put("generated_code.py", "/home/ec2-user/generated_code.py")
        sftp_client.close()

        # Execute the code on EC2
        stdin, stdout, stderr = ssh_client.exec_command("python3 /home/ec2-user/generated_code.py")

        # Capture the output
        execution_output = stdout.read().decode()
        error_output = stderr.read().decode()

        print("\nExecution Output:\n", execution_output)
        if error_output:
            print("Execution Error:\n", error_output)

        # Check if there are any errors in execution
        if error_output:
            print("Error detected, regenerating prompt...")
            # Regenerate the task prompt based on the error
            new_prompt = f"Fix this error: {error_output}"
            new_code = generate_code(new_prompt)

            # Recursively call the function to re-execute the code
            return execute_code_on_ec2(new_code, EC2_HOST, EC2_USER, EC2_KEY_FILE)

        return execution_output

    except Exception as e:
        print(f"An error occurred during EC2 execution: {e}")
        return None
    finally:
        ssh_client.close()

# Prompt user for task details
task_prompt = input("Enter the task prompt: ")

# Call the LLM to generate the code
generated_code = generate_code(task_prompt)
print("\nGenerated Code:\n")
print(generated_code)

# Save the generated code to a local file
with open("generated_code.py", "w") as code_file:
    code_file.write(generated_code)

# Prompt user for EC2 connection details
EC2_HOST = input("Enter the EC2 host (public DNS): ")
EC2_USER = input("Enter the EC2 username: ")
EC2_KEY_FILE = input("Enter the path to your EC2 private key file: ")

# Execute the code on EC2 with error handling
execution_output = execute_code_on_ec2(generated_code, EC2_HOST, EC2_USER, EC2_KEY_FILE)

if execution_output:
    # Collect and store results in a structured format
    results = {
        "execution_output": execution_output,
        "error_output": None
    }

    # Store results in JSON (or CSV if needed)
    store_results(results, file_format="json")

    # Prepare results for the next LLM task
    prepare_for_next_llm(results)

else:
    print("Failed to execute the code after multiple attempts.")
