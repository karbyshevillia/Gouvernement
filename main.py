from Gouvernement import create_app
import atexit
import subprocess
import os

app = create_app()

if __name__ == '__main__':

    @atexit.register
    def cleanup_pycache():
        subprocess.run(['pyclean', os.getcwd()], check=False)


    app.run(debug=True)