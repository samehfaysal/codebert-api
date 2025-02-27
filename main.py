from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

# Initialize FastAPI app
app = FastAPI()

# Load CodeBERT model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("microsoft/codebert-base")
model = AutoModelForSeq2SeqLM.from_pretrained("Salesforce/codet5-small")

# Define request model
class CodeInput(BaseModel):
    code: str

@app.post("/summarize")
def summarize_code(data: CodeInput):
    input_code = data.code
    inputs = tokenizer.encode(input_code, return_tensors="pt", max_length=512, truncation=True)
    
    # Generate summary
    summary_ids = model.generate(inputs, max_length=50, num_return_sequences=1)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    return {"summary": summary}

# Run the server (if running locally)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

