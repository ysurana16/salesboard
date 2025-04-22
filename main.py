# app.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from analyzer import SalesAnalyzer  
app = FastAPI()

# Optional: allow frontend (FlutterFlow) to access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or restrict to FlutterFlow domain for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/insights")
def get_insights():
    try:
        # Get data from Google Sheet
        sheet_id = "1Tm_zp9TkYLLs7ZIUFGA-qDImWU1o-IBbGiKdS8QktNc"
        gid = "9859409"
        csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
        df = pd.read_csv(csv_url)

        analyzer = SalesAnalyzer(df)
        return analyzer.to_json_summary()
    except Exception as e:
        return {"error": str(e)}
    
@app.get("/analyze")
def read_root():
    return {"message": "Welcome to the Sales Insights API!"}
