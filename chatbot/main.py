from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from startup import populate_db_with_random_data
from chatbot import Chatbot


app = FastAPI()


class PromptInput(BaseModel):
    prompt: str

@app.on_event("startup")
def startup_event():
    populate_db_with_random_data()

# Serve frontend files
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate_sql")
def generate_sql_from_prompt(input_data: PromptInput):
    prompt = input_data.prompt
    bot = Chatbot()
    output = bot.generate_sql_from_user_prompt(prompt)
    # result = bot.execute_sql_and_return_response(sql_code)
    bot.close()
    return {"sql": output}