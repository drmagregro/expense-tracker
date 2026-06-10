import sys
import base64
import json
from dotenv import load_dotenv
from groq import Groq
import os

class ExpenseAgent:
    def __init__(self):
        load_dotenv()
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(BASE_DIR, "context.txt"), "r", encoding="utf-8") as f:
            self.context = f.read()
        with open(os.path.join(BASE_DIR, "prompt.txt"), "r", encoding="utf-8") as f:
            self.prompt = f.read()
        

    def extract_from_bytes(self, image_bytes, media_type):
        image_b64 = base64.b64encode(image_bytes).decode("utf-8")
        response = self.client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": self.context},
                {"role": "user", "content": [
                    {"type": "text", "text": self.prompt},
                    {"type": "image_url", "image_url": {
                        "url": f"data:{media_type};base64,{image_b64}"
                    }}
                ]}
            ]
        )
        EXPECTED_FIELDS = ["type_document", "fournisseur", "date", "montant_ttc", "tva", "devise", "description", "confiance"]
        result = json.loads(response.choices[0].message.content)
        return {field: result.get(field, None) for field in EXPECTED_FIELDS}
    

if __name__ == "__main__":
    
    image_path = sys.argv[1]  # on passe le chemin de l'image en argument
    
    with open(image_path, "rb") as f:
        image_bytes = f.read()
    
    agent = ExpenseAgent()
    result = agent.extract_from_bytes(image_bytes, "photo-ticket.jpg")
    print(json.dumps(result, indent=2, ensure_ascii=False))