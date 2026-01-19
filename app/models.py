from pydantic import BaseModel
from typing import List, Optional

class KuppiRecommendation(BaseModel):
    id: int
    title: str
    description: str
    price: float
    university_name: str
    department_name: str
    degree_name: str
    subject_name: str
    tutor_name: str
    similarity_score: float

class RecommendationResponse(BaseModel):
    student_id: int
    recommendations: List[KuppiRecommendation]