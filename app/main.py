from fastapi import FastAPI
from app.routers import tasks, auth

app = FastAPI()

# Register your routers
app.include_router(auth.router)
app.include_router(tasks.router)

from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi.middleware.cors import CORSMiddleware

@app.middleware("http")
async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": str(e)})
