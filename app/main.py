from fastapi import FastAPI
from .routers import ideas, projects, products, processes, finance, accounting, taxes, auth, subscriptions
from .config import settings
from .database import engine, Base

app = FastAPI(title="Angel in Pocket – Full Business Agent with Subscriptions")

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(subscriptions.router)
app.include_router(ideas.router)
app.include_router(projects.router)
app.include_router(products.router)
app.include_router(processes.router)
app.include_router(finance.router)
app.include_router(accounting.router)
app.include_router(taxes.router)

@app.get("/")
def root():
    return {"message": "Angel is ready with paid subscriptions"}
