from flask import Flask, jsonify
from flask_cors import CORS
import subprocess
import threading
import sys
import os

app = Flask(__name__)
CORS(app)

@app.route('/run-music-script', methods=['POST'])
def run_music_script():
    """Automatically run the music data fetcher script"""
    try:
        print("🚀 Running music data fetcher script...")
        
        # Exact path to your script
        script_path = "/Users/aryantyagi/rap-news/src/music_data_fetcher.py"
        project_root = "/Users/aryantyagi/rap-news"
        
        print(f"📁 Script path: {script_path}")
        print(f"📁 Script exists: {os.path.exists(script_path)}")
        
        # Run your script in the background
        def run_script():
            try:
                # Change to the project root directory before running
                os.chdir(project_root)
                print(f"📁 Working directory: {os.getcwd()}")
                
                result = subprocess.run([sys.executable, script_path], 
                                      capture_output=True, text=True, check=True)
                print("✅ Script completed successfully!")
                print("Script output:", result.stdout)
                
            except subprocess.CalledProcessError as e:
                print(f"❌ Script failed: {e}")
                print(f"Error output: {e.stderr}")
            except Exception as e:
                print(f"❌ Unexpected error: {e}")
        
        # Start script in background thread
        thread = threading.Thread(target=run_script)
        thread.start()
        
        return jsonify({
            'success': True,
            'message': 'Music data script started successfully!'
        })
        
    except Exception as e:
        print(f"❌ Server error: {e}")
        return jsonify({
            'success': False, 
            'message': f'Error: {str(e)}'
        }), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    print("🚀 Starting auto-script server...")
    print("📡 Server will run on http://localhost:5001")
    
    # Check if script exists
    script_path = "/Users/aryantyagi/rap-news/src/music_data_fetcher.py"
    print(f"📁 Script exists: {os.path.exists(script_path)}")
    
    app.run(debug=True, port=5001, host='0.0.0.0')