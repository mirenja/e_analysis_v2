# agora
Energy data analysis
##load the modules for the python using
python3 -m pip install -r requirements.txt

Activate source venv/bin/activate

start server using app.py
 run.py


## folder structure
dataprocessing functions are under backend/app/visualization/services/agg_generation.py
API call is on routes.py which forwads the json file to the FE for visualization

The running FE is under backend/app/templates/index.html inline with flask folder structure, but there is a separate folder duplicate

## best representation is in thought process.pdf