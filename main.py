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

# import time

# while True:
#     with open('progress.txt', 'r') as file:
#         progress = file.read().strip()
#         print(f'Current progress: {progress}')

#     time.sleep(5)  # Wait for 5 seconds before checking again


@app.get("/dashboard")
async def read_users():
    # just have text of progression

    # later create front end
    return ["Pickle", "Rick"]