
# # from fastapi import FastAPI, Depends, HTTPException
# # from sqlalchemy.orm import Session
# # from typing import List
# # import os
# # from dotenv import load_dotenv

# # from .database import get_db
# # from .models import RecommendationResponse, KuppiRecommendation
# # from .recommendation import RecommendationEngine

# # load_dotenv()

# # app = FastAPI(title="Sluni Recommendation API", version="1.0.0")

# # # Global recommendation engine
# # recommendation_engine = None

# # @app.on_event("startup")
# # async def startup_event():
# #     global recommendation_engine
# #     db = next(get_db())
# #     recommendation_engine = RecommendationEngine(db)
# #     recommendation_engine.refresh_models()
# #     db.close()

# # @app.get("/")
# # def read_root():
# #     return {"message": "Sluni Recommendation API is running"}

# # @app.get("/recommendations/{student_id}", response_model=RecommendationResponse)
# # def get_recommendations(student_id: int, top_n: int = 5, db: Session = Depends(get_db)):
# #     global recommendation_engine
    
# #     if recommendation_engine is None:
# #         raise HTTPException(status_code=500, detail="Recommendation engine not initialized")
    
# #     # Refresh models periodically (in production, you might want to do this on a schedule)
# #     # For now, we'll refresh on each request to ensure up-to-date recommendations
# #     recommendation_engine.refresh_models()
    
# #     recommendations = recommendation_engine.get_recommendations(student_id, top_n)
    
# #     if not recommendations:
# #         raise HTTPException(status_code=404, detail="No recommendations found for this student")
    
# #     # Convert to response model
# #     response_recommendations = [
# #         KuppiRecommendation(
# #             id=rec["id"],
# #             title=rec["title"],
# #             description=rec["description"],
# #             price=rec["price"],
# #             university_name=rec["university_name"],
# #             department_name=rec["department_name"],
# #             degree_name=rec["degree_name"],
# #             subject_name=rec["subject_name"],
# #             tutor_name=rec["tutor_name"],
# #             similarity_score=rec["similarity_score"]
# #         )
# #         for rec in recommendations
# #     ]
    
# #     return RecommendationResponse(
# #         student_id=student_id,
# #         recommendations=response_recommendations
# #     )

# # @app.post("/refresh")
# # def refresh_recommendations(db: Session = Depends(get_db)):
# #     global recommendation_engine
    
# #     if recommendation_engine is None:
# #         raise HTTPException(status_code=500, detail="Recommendation engine not initialized")
    
# #     recommendation_engine.refresh_models()
    
# #     return {"message": "Recommendation models refreshed successfully"}

# from fastapi import FastAPI, Depends, HTTPException
# from sqlalchemy.orm import Session
# from typing import List
# import os
# from dotenv import load_dotenv

# from .database import get_db
# from .models import RecommendationResponse, KuppiRecommendation
# from .recommendation import RecommendationEngine

# load_dotenv()

# app = FastAPI(title="Sluni Recommendation API", version="1.0.0")

# # Global recommendation engine
# recommendation_engine = None

# @app.on_event("startup")
# async def startup_event():
#     global recommendation_engine
#     db = next(get_db())
#     recommendation_engine = RecommendationEngine(db)
#     recommendation_engine.refresh_models()
#     db.close()

# @app.get("/")
# def read_root():
#     return {"message": "Sluni Recommendation API is running"}

# @app.get("/recommendations/{student_id}", response_model=RecommendationResponse)
# def get_recommendations(student_id: int, top_n: int = 5, db: Session = Depends(get_db)):
#     global recommendation_engine
    
#     if recommendation_engine is None:
#         raise HTTPException(status_code=500, detail="Recommendation engine not initialized")
    
#     # Refresh models periodically (in production, you might want to do this on a schedule)
#     # For now, we'll refresh on each request to ensure up-to-date recommendations
#     recommendation_engine.refresh_models()
    
#     # Try to get personalized recommendations
#     recommendations = recommendation_engine.get_recommendations(student_id, top_n)
    
#     # If no personalized recommendations are available, use fallback recommendations
#     if not recommendations:
#         recommendations = recommendation_engine.get_fallback_recommendations(student_id, top_n)
    
#     if not recommendations:
#         raise HTTPException(status_code=404, detail="No recommendations found for this student")
    
#     # Convert to response model
#     response_recommendations = [
#         KuppiRecommendation(
#             id=rec["id"],
#             title=rec["title"],
#             description=rec["description"],
#             price=rec["price"],
#             university_name=rec["university_name"],
#             department_name=rec["department_name"],
#             degree_name=rec["degree_name"],
#             subject_name=rec["subject_name"],
#             tutor_name=rec["tutor_name"],
#             similarity_score=rec["similarity_score"]
#         )
#         for rec in recommendations
#     ]
    
#     return RecommendationResponse(
#         student_id=student_id,
#         recommendations=response_recommendations
#     )

# @app.post("/refresh")
# def refresh_recommendations(db: Session = Depends(get_db)):
#     global recommendation_engine
    
#     if recommendation_engine is None:
#         raise HTTPException(status_code=500, detail="Recommendation engine not initialized")
    
#     recommendation_engine.refresh_models()
    
#     return {"message": "Recommendation models refreshed successfully"}

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from .database import get_db
from .models import RecommendationResponse, KuppiRecommendation
from .recommendation import RecommendationEngine

app = FastAPI(title="Sluni Recommendation API")

engine = None

@app.on_event("startup")
def startup():
    global engine
    db = next(get_db())
    engine = RecommendationEngine(db)
    engine.refresh_models()
    db.close()

@app.get("/")
def root():
    return {"message": "Recommendation API running"}

@app.get("/recommendations/{student_id}", response_model=RecommendationResponse)
def recommend(student_id: int, top_n: int = 5, db: Session = Depends(get_db)):
    if not engine:
        raise HTTPException(500, "Engine not initialized")

    engine.refresh_models()
    recs = engine.get_recommendations(student_id, top_n)

    if not recs:
        raise HTTPException(404, "No recommendations found")

    return RecommendationResponse(
        student_id=student_id,
        recommendations=[KuppiRecommendation(**r) for r in recs]
    )

@app.post("/refresh")
def refresh():
    engine.refresh_models()
    return {"message": "Models refreshed"}
