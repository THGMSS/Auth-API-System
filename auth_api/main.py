from fastapi import FastAPI
from auth import router

# FastAPI como a api principal
app = FastAPI()

app.include_router(router) # Inclui o router que organiza os endpoints

