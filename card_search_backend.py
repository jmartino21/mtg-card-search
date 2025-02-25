from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
from fastapi.responses import FileResponse
import os
# Load the CSV file
CSV_PATH = os.path.join(os.path.dirname(__file__), "Combined_Card_Collections.csv")
df = pd.read_csv(CSV_PATH)

# Initialize FastAPI
app = FastAPI()

# Request model
class CardSearchRequest(BaseModel):
    cards: list[str]

print("App start up successful)")

@app.get("/")
def serve_frontend():
    return FileResponse(os.path.join(os.path.dirname(__file__), "index.html"))

@app.post("/api/search")
def search_cards(request: CardSearchRequest):
    if not request.cards:
        raise HTTPException(status_code=400, detail="No card names provided.")
    
    search_results = df[df["Card Name"].isin(request.cards)]
    
    if search_results.empty:
        return []
    
    return search_results.to_dict(orient="records")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
