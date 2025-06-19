from fastapi import FastAPI
from app.routers import tasks, auth
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.requests import Request

app = FastAPI()

# ✅ Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://task-tracker-frontend-tcqz.vercel.app"],  # replace with your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register your routers
app.include_router(auth.router)
app.include_router(tasks.router)

# Optional: Catch exceptions
@app.middleware("http")
async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": str(e)})

# Root route
@app.get("/")
def root():
    return {"message": "Task Tracker API is working!"}
