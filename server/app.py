import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apis.auth import auth_router
from apis.apikey import apikey_router
from apis.api import api_router
import os
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
port = int(os.environ.get("PORT", 8080))

'''
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)
'''
