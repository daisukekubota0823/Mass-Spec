from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import mass_spectra
from app.core.config import settings
from app.db.session import engine
from app.models import mass_spectrum as mass_spectrum_model
from app.models import retention_time_structure as retention_time_structure_model
from app.models import retention_time_library as retention_time_library_model
from app.models import user_defined_structure as user_defined_structure_model
from app.models import ccs_library as ccs_library


mass_spectrum_model.Base.metadata.create_all(bind=engine)
retention_time_structure_model.Base.metadata.create_all(bind=engine)
retention_time_library_model.Base.metadata.create_all(bind=engine)
user_defined_structure_model.Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Add your frontend origin here
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(mass_spectra.router, prefix=settings.API_V1_STR)
