from fastapi import FastAPI

app = FastAPI(
    title="Geonosis API",
    description="AI-powered software development orchestration system",
    version="0.1.0",
)


@app.get("/")
async def root():
    return {"message": "Geonosis API", "status": "operational"}


@app.get("/health")
async def health():
    return {"status": "healthy"}
