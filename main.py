from fastapi import FastAPI, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI() # create instance

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

from dashboard_logic import read_progress
@app.get("/dashboard")
async def show_progress():
    # just have text of progression
    output_folder = './output'
    progress_object = read_progress(output_folder)
    # progress_object = 'test'
    # later create front end
    return progress_object