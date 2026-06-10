from fastapi import FastAPI, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from backend import ExpenseAgent
from sheets import GoogleSheetsClient
import base64

app = FastAPI()
agent = ExpenseAgent()
sheets_client = GoogleSheetsClient()
app.mount("/static", StaticFiles(directory="static"), name="static")    

@app.get("/")
async def index():
    return FileResponse("static/index.html")

@app.post("/api/analyze")
async def analyze(file: UploadFile = File(...)):
    image_bytes = await file.read()
    data = agent.extract_from_bytes(image_bytes, file.content_type)
    html = f"""
    <form hx-post="/api/submit" hx-target="#confirmation-container" hx-encoding="multipart/form-data">
        <input name="type_document" value="{data.get('type_document', '')}">
        <input name="fournisseur" value="{data.get('fournisseur', '')}">
        <input name="date" value="{data.get('date', '')}">
        <input name="montant_ttc" value="{data.get('montant_ttc', '')}">
        <input name="tva" value="{data.get('tva', '')}">
        <input name="devise" value="{data.get('devise', '')}">
        <input name="description" value="{data.get('description', '')}">
        <input name="confiance" value="{data.get('confiance', '')}">
        <input type="hidden" name="image_data" value="{base64.b64encode(image_bytes).decode('utf-8')}">
        <button type="submit">Envoyer</button>
    </form>
    """
    return HTMLResponse(html)

@app.post("/api/submit")
async def submit(
    type_document: str = Form(None),
    fournisseur: str = Form(None),
    date: str = Form(None),
    montant_ttc: str = Form(None),
    tva: str = Form(None),
    devise: str = Form(None),
    description: str = Form(None),
    confiance: str = Form(None),
    image_data: str = Form(None)
):
    data = {
        "type_document": type_document,
        "fournisseur": fournisseur,
        "date": date,
        "montant_ttc": montant_ttc,
        "tva": tva,
        "devise": devise,
        "description": description,
        "confiance": confiance
    }
    sheets_client.append_expense(data)
    return HTMLResponse("<p>✅ Note de frais envoyée avec succès !</p>")