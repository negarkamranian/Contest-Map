from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Configure Jinja2Templates
templates = Jinja2Templates(directory="templates")

# Mount static files (e.g., images) from the templates directory
# This allows files like /static/image.png to be served directly.
app.mount("/static", StaticFiles(directory="templates"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/submit_flag")
async def submit_flag(flag: str = Form(...)):
    # This endpoint could be used for flag submission in the future
    return {"message": "Flag received", "flag": flag}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)