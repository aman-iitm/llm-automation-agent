# Phase B: LLM-based Automation Agent for DataWorks Solutions

# B1 & B2: Security Checks
from flask import Flask, request, jsonify
import pandas as pd
import os
app = Flask(__name__)

def B12(filepath):
    """Ensure that the filepath is within the /data directory."""
    if not filepath.startswith('/data'):
        raise PermissionError("Access outside /data is not allowed.")
    
@app.route('/filter_csv', methods=['POST'])


# B3: Fetch Data from an API
def B3(url, save_path):
    """Fetch data from an API and save it to the specified path."""
    B12(save_path)  # Ensure the save path is within /data
    import requests
    response = requests.get(url)
    with open(save_path, 'w') as file:
        file.write(response.text)

# B4: Clone a Git Repo and Make a Commit
def B4(repo_url, commit_message):
    """Clone a git repo and make a commit."""
    import subprocess
    repo_path = "/data/repo"
    B12(repo_path)  # Ensure the repo path is within /data
    subprocess.run(["git", "clone", repo_url, repo_path])
    subprocess.run(["git", "-C", repo_path, "add", "."])
    subprocess.run(["git", "-C", repo_path, "commit", "-m", commit_message])

# B5: Run SQL Query
def B5(db_path, query, output_filename):
    """Run a SQL query on a SQLite or DuckDB database and save the result."""
    B12(db_path)  # Ensure the database path is within /data
    B12(output_filename)  # Ensure the output file path is within /data
    import sqlite3, duckdb 
    conn = sqlite3.connect(db_path) if db_path.endswith('.db') else duckdb.connect(db_path)
    cur = conn.cursor()
    cur.execute(query)
    result = cur.fetchall()
    conn.close()
    with open(output_filename, 'w') as file:
        file.write(str(result))
    return result

# B6: Web Scraping
def B6(url, output_filename):
    """Extract data from a website and save it to the specified file."""
    B12(output_filename)  # Ensure the output file path is within /data
    import requests
    result = requests.get(url).text
    with open(output_filename, 'w') as file:
        file.write(str(result))
        
# B7: Image Processing
def B7(image_path, output_path, resize=None):
    """Compress or resize an image and save it to the specified path."""
    B12(image_path)  # Ensure the input image path is within /data
    B12(output_path)  # Ensure the output image path is within /data
    from PIL import Image
    img = Image.open(image_path)
    if resize:
        img = img.resize(resize)
    img.save(output_path)

# B8: Audio Transcription
def B8(audio_path, output_path):
    """Transcribe audio from an MP3 file and save the transcription."""
    B12(audio_path)  # Ensure the audio path is within /data
    B12(output_path)  # Ensure the output file path is within /data
    import openai
    with open(audio_path, 'rb') as audio_file:
        transcription = openai.Audio.transcribe("whisper-1", audio_file)
    with open(output_path, 'w') as file:
        file.write(transcription['text'])

# B9: Markdown to HTML Conversion
def B9(md_path, output_path):
    """Convert a Markdown file to HTML and save it to the specified path."""
    B12(md_path)  # Ensure the Markdown file path is within /data
    B12(output_path)  # Ensure the output file path is within /data
    import markdown
    with open(md_path, 'r') as file:
        html = markdown.markdown(file.read())
    with open(output_path, 'w') as file:
        file.write(html)


@app.route('/filter_csv', methods=['POST'])
def filter_csv():
    """Filter a CSV file based on the provided column and value, and return JSON data."""
    try:
        data = request.get_json()
        csv_path = data.get('csv_path')
        filter_column = data.get('filter_column')
        filter_value = data.get('filter_value')

        if not csv_path or not filter_column or filter_value is None:
            return jsonify({"error": "Missing required parameters"}), 400

        # Security check
        B12(csv_path)

        # Ensure the file exists
        if not os.path.exists(csv_path):
            return jsonify({"error": "CSV file not found"}), 404

        # Read and filter CSV
        df = pd.read_csv(csv_path)
        if filter_column not in df.columns:
            return jsonify({"error": f"Column '{filter_column}' not found in CSV"}), 400

        filtered = df[df[filter_column] == filter_value]
        return jsonify(filtered.to_dict(orient='records'))

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Prevent Flask from running when imported as a module
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)