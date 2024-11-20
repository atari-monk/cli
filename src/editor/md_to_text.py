from editor.lib.md_to_text_converter import run_app
import multiprocessing

def run(_ = None):
    process = multiprocessing.Process(target=run_app)
    process.daemon = True  # This ensures the process will be killed when the main program exits
    process.start()
