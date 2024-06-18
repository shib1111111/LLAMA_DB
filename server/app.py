import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apis.auth import auth_router
from apis.apikey import apikey_router
from apis.api import api_router

app = FastAPI()

# CORS configuration to allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

app.include_router(auth_router)
app.include_router(apikey_router)
app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run("app:app", host="localhost", port=8080,reload=True)
