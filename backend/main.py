from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.banks.routes import router as banks_router
from app.financings.routes import router as financings_router
from app.products.routes import router as products_router
from app.pricing.routes import router as pricing_router


# Database initialization
Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers from each slice
app.include_router(banks_router)
app.include_router(financings_router)
app.include_router(products_router)
app.include_router(pricing_router)
