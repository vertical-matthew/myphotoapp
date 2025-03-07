import os
import datetime
import logging
import pyperclip

def main():
    # Get the project root directory (assumes the script is run at the root)
    project_root = os.getcwd()
    print(f"Scanning Django project at: {project_root}")

    # Setup a log file with a date-timestamp in its name (file name safe)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"project_log_{timestamp}.txt"
    logging.basicConfig(
        filename=log_filename,
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    print(f"Logging details will be saved to: {log_filename}")
    logging.info("Script started.")

    # Only include files that represent your custom logic
    allowed_extensions = {'.py', '.html', '.css', '.js'}

    # Directories to be skipped during the scan
    skip_dirs = {'.git', '.idea', 'static', 'staticfiles', 'migrations', '__pycache__', 'venv'}

    project_text = []

    # Walk through the project directories
    for root, dirs, files in os.walk(project_root):
        # Remove directories we want to skip so they are not walked into
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        print(f"Scanning directory: {root}")
        logging.info(f"Scanning directory: {root}")
        
        for file in files:
            # Check file extension; ignore files that are not in our allowed list
            file_ext = os.path.splitext(file)[1].lower()
            if file_ext not in allowed_extensions:
                continue

            # Construct the full file path
            file_path = os.path.join(root, file)
            print(f"Processing file: {file_path}")
            logging.info(f"Processing file: {file_path}")
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                # Append header with file location and its contents
                header = f"\n\n----- FILE: {file_path} -----\n\n"
                project_text.append(header)
                project_text.append(content)
            except Exception as e:
                error_msg = f"Could not read file {file_path}: {e}"
                print(error_msg)
                logging.error(error_msg)

    # Combine all collected content into a single string
    full_text = "\n".join(project_text)

    # Copy the full text to the system clipboard
    try:
        pyperclip.copy(full_text)
        print("Project contents have been copied to the clipboard.")
        logging.info("Project contents copied to clipboard successfully.")
    except Exception as e:
        error_msg = f"Failed to copy project contents to clipboard: {e}"
        print(error_msg)
        logging.error(error_msg)

    # Append the complete project content to the log file
    try:
        with open(log_filename, 'a', encoding='utf-8') as log_file:
            log_file.write("\n\n=== Full Project Content ===\n\n")
            log_file.write(full_text)
        print(f"Project contents have been appended to the log file: {log_filename}")
        logging.info("Project contents appended to log file successfully.")
    except Exception as e:
        error_msg = f"Failed to write project content to log file: {e}"
        print(error_msg)
        logging.error(error_msg)

    print("Script finished successfully.")
    logging.info("Script finished successfully.")

if __name__ == '__main__':
    main()
