echo Starting the Notebook Server

:: Print Python version
python --version

:: Print a specific module version (e.g., numpy)
python -c "import numpy; print('numpy version:', numpy.__version__)"

:: Print a specific module version (e.g., numpy)
python -c "import arcgis; print('arcgis version:', arcgis.__version__)"

:: Print a message
echo Launching Jupyter Notebook...


poetry run python -m notebook
