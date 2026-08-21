import os
from datetime import datetime

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.database import Base, engine
from app.routes import (
    analysis,
    audit,
    auth,
    finance,
    inventory,
    purchase_orders,
    quotations,
    rfq,
    vendors,
)

load_dotenv()

app = FastAPI(title="STAR AI Backend", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:3001", "http://127.0.0.1:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if os.path.exists("uploads"):
    app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


@app.get("/health")
async def health_check():
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}


@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(rfq.router, prefix="/rfqs", tags=["rfqs"])
app.include_router(vendors.router, prefix="/vendors", tags=["vendors"])
app.include_router(quotations.router, prefix="/quotations", tags=["quotations"])
app.include_router(analysis.router, prefix="/analysis", tags=["analysis"])
app.include_router(purchase_orders.router, prefix="/purchase-orders", tags=["purchase-orders"])
app.include_router(inventory.router, prefix="/inventory", tags=["inventory"])
app.include_router(finance.router, prefix="/finance", tags=["finance"])
app.include_router(audit.router, prefix="/audit", tags=["audit"])
