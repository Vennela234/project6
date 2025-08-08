from fastapi import FastAPI, UploadFile, File, Query
from fastapi.responses import JSONResponse
from model import forecast_from_csv
import tempfile

app = FastAPI()

@app.post("/forecast/")
async def forecast_endpoint(
    file: UploadFile = File(...),
    periods: int = Query(7),
    freq: str = Query("D")
):
    try:
        contents = await file.read()
        print(f"📁 File received: {file.filename}")
        print(f"📈 Forecast periods: {periods}, freq: {freq}")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
            tmp.write(contents)
            tmp_path = tmp.name

        forecast_df = forecast_from_csv(tmp_path, periods, freq)

        print("✅ Forecast generated:")
        print(forecast_df)

        return forecast_df.to_dict(orient='records')

    except Exception as e:
        print("❌ Error:", str(e))
        return JSONResponse(status_code=500, content={"error": str(e)})
