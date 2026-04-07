from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Create the FastAPI app instance
app = FastAPI()

# Allow the frontend (plain HTML file opened in browser) to call this backend
# Without this, the browser blocks cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the shape of the data we expect from the frontend form
class OnboardRequest(BaseModel):
    business_name: str
    owner_name: str
    phone: str
    area: str
    url: str = ""  # optional — existing website or Dapei Zahav minisite

# The main endpoint — will run the full pipeline once all parts are built
@app.post("/onboard")
async def onboard(data: OnboardRequest):
    # Placeholder: just echo back what we received so we can test the connection
    return {"status": "ok", "received": data.model_dump()}
