# # # # # # from sqlalchemy.orm import Session
# # # # # # from sklearn.feature_extraction.text import TfidfVectorizer
# # # # # # from sklearn.metrics.pairwise import cosine_similarity
# # # # # # import pandas as pd
# # # # # # import numpy as np
# # # # # # from typing import List, Dict, Tuple
# # # # # # import re
# # # # # # from .database import Kuppi, User, Student, Enrollment, Review, University, Department, Degree, Subject, Tutor

# # # # # # class RecommendationEngine:
# # # # # #     def __init__(self, db: Session):
# # # # # #         self.db = db
# # # # # #         self.tfidf_vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
# # # # # #         self.kuppi_vectors = None
# # # # # #         self.kuppi_df = None
# # # # # #         self.student_vectors = None
# # # # # #         self.student_df = None
        
# # # # # #     def preprocess_text(self, text: str) -> str:
# # # # # #         """Basic text preprocessing"""
# # # # # #         if not text:
# # # # # #             return ""
# # # # # #         # Convert to lowercase
# # # # # #         text = text.lower()
# # # # # #         # Remove special characters and digits
# # # # # #         text = re.sub(r'[^a-zA-Z\s]', '', text)
# # # # # #         return text
    
# # # # # #     def build_kuppi_vectors(self):
# # # # # #         """Build TF-IDF vectors for all Kuppis"""
# # # # # #         # Get all approved kuppis
# # # # # #         kuppis = self.db.query(Kuppi).filter(Kuppi.status == 'APPROVED').all()
        
# # # # # #         if not kuppis:
# # # # # #             return
        
# # # # # #         # Create a DataFrame with kuppi data
# # # # # #         kuppi_data = []
# # # # # #         for kuppi in kuppis:
# # # # # #             # Get related information
# # # # # #             university = self.db.query(University).filter(University.id == kuppi.university_id).first()
# # # # # #             department = self.db.query(Department).filter(Department.id == kuppi.department_id).first()
# # # # # #             degree = self.db.query(Degree).filter(Degree.id == kuppi.degree_id).first()
# # # # # #             subject = self.db.query(Subject).filter(Subject.id == kuppi.subject_id).first()
# # # # # #             tutor = self.db.query(User).filter(User.id == kuppi.tutor_id).first()
            
# # # # # #             # Combine text fields for content similarity
# # # # # #             combined_text = f"{kuppi.title} {kuppi.description} {subject.name if subject else ''} {subject.description if subject else ''}"
            
# # # # # #             kuppi_data.append({
# # # # # #                 'id': kuppi.id,
# # # # # #                 'title': kuppi.title,
# # # # # #                 'description': kuppi.description,
# # # # # #                 'price': float(kuppi.price),
# # # # # #                 'university_id': kuppi.university_id,
# # # # # #                 'university_name': university.name if university else '',
# # # # # #                 'department_id': kuppi.department_id,
# # # # # #                 'department_name': department.name if department else '',
# # # # # #                 'degree_id': kuppi.degree_id,
# # # # # #                 'degree_name': degree.name if degree else '',
# # # # # #                 'subject_id': kuppi.subject_id,
# # # # # #                 'subject_name': subject.name if subject else '',
# # # # # #                 'tutor_id': kuppi.tutor_id,
# # # # # #                 'tutor_name': tutor.full_name if tutor else '',
# # # # # #                 'combined_text': self.preprocess_text(combined_text)
# # # # # #             })
        
# # # # # #         self.kuppi_df = pd.DataFrame(kuppi_data)
        
# # # # # #         # Create TF-IDF vectors
# # # # # #         self.kuppi_vectors = self.tfidf_vectorizer.fit_transform(self.kuppi_df['combined_text'])
    
# # # # # #     def build_student_vectors(self):
# # # # # #         """Build interaction vectors for all students"""
# # # # # #         # Get all students
# # # # # #         students = self.db.query(Student).all()
        
# # # # # #         if not students:
# # # # # #             return
        
# # # # # #         student_data = []
        
# # # # # #         for student in students:
# # # # # #             # Get student's enrollments
# # # # # #             enrollments = self.db.query(Enrollment).filter(Enrollment.student_id == student.id).all()
# # # # # #             enrolled_kuppi_ids = [e.kuppi_id for e in enrollments]
            
# # # # # #             # Get student's reviews
# # # # # #             reviews = self.db.query(Review).filter(Review.student_id == student.id).all()
# # # # # #             reviewed_kuppi_ids = [r.kuppi_id for r in reviews]
            
# # # # # #             # Get student's questions
# # # # # #             questions = self.db.query(Question).filter(Question.student_id == student.id).all()
# # # # # #             asked_kuppi_ids = [q.kuppi_id for q in questions]
            
# # # # # #             # Combine all interactions
# # # # # #             all_interacted_kuppi_ids = list(set(enrolled_kuppi_ids + reviewed_kuppi_ids + asked_kuppi_ids))
            
# # # # # #             # Get the kuppis the student interacted with
# # # # # #             interacted_kuppis = self.db.query(Kuppi).filter(Kuppi.id.in_(all_interacted_kuppi_ids)).all()
            
# # # # # #             # Create a profile based on the content of interacted kuppis
# # # # # #             profile_text = ""
# # # # # #             for kuppi in interacted_kuppis:
# # # # # #                 subject = self.db.query(Subject).filter(Subject.id == kuppi.subject_id).first()
# # # # # #                 profile_text += f"{kuppi.title} {kuppi.description} {subject.name if subject else ''} "
            
# # # # # #             student_data.append({
# # # # # #                 'id': student.id,
# # # # # #                 'university_id': student.university_id,
# # # # # #                 'department_id': student.department_id,
# # # # # #                 'degree_id': student.degree_id,
# # # # # #                 'academic_year': student.academic_year,
# # # # # #                 'enrolled_kuppi_ids': enrolled_kuppi_ids,
# # # # # #                 'reviewed_kuppi_ids': reviewed_kuppi_ids,
# # # # # #                 'asked_kuppi_ids': asked_kuppi_ids,
# # # # # #                 'profile_text': self.preprocess_text(profile_text)
# # # # # #             })
        
# # # # # #         self.student_df = pd.DataFrame(student_data)
        
# # # # # #         # Create TF-IDF vectors for student profiles
# # # # # #         if not self.student_df['profile_text'].str.strip().empty:
# # # # # #             self.student_vectors = self.tfidf_vectorizer.transform(self.student_df['profile_text'])
    
# # # # # #     def get_recommendations(self, student_id: int, top_n: int = 5) -> List[Dict]:
# # # # # #         """Get top-N recommendations for a student"""
# # # # # #         # Build vectors if not already built
# # # # # #         if self.kuppi_vectors is None:
# # # # # #             self.build_kuppi_vectors()
        
# # # # # #         if self.student_vectors is None:
# # # # # #             self.build_student_vectors()
        
# # # # # #         # Check if student exists
# # # # # #         student_row = self.student_df[self.student_df['id'] == student_id]
# # # # # #         if student_row.empty:
# # # # # #             return []
        
# # # # # #         student_idx = student_row.index[0]
# # # # # #         student_vector = self.student_vectors[student_idx]
        
# # # # # #         # Get student's enrolled kuppis to exclude them from recommendations
# # # # # #         enrolled_kuppi_ids = student_row.iloc[0]['enrolled_kuppi_ids']
        
# # # # # #         # Calculate cosine similarity between student and all kuppis
# # # # # #         similarity_scores = cosine_similarity(student_vector, self.kuppi_vectors).flatten()
        
# # # # # #         # Get indices of top similar kuppis
# # # # # #         top_indices = similarity_scores.argsort()[-top_n*2:][::-1]  # Get more to filter out enrolled ones
        
# # # # # #         # Filter out already enrolled kuppis and get top N
# # # # # #         recommendations = []
# # # # # #         for idx in top_indices:
# # # # # #             kuppi_id = self.kuppi_df.iloc[idx]['id']
# # # # # #             if kuppi_id not in enrolled_kuppi_ids:
# # # # # #                 kuppi_data = self.kuppi_df.iloc[idx].to_dict()
# # # # # #                 kuppi_data['similarity_score'] = float(similarity_scores[idx])
# # # # # #                 recommendations.append(kuppi_data)
                
# # # # # #                 if len(recommendations) >= top_n:
# # # # # #                     break
        
# # # # # #         return recommendations
    
# # # # # #     def refresh_models(self):
# # # # # #         """Refresh the recommendation models"""
# # # # # #         self.build_kuppi_vectors()
# # # # # #         self.build_student_vectors()

# # # # # from sqlalchemy.orm import Session
# # # # # from sklearn.feature_extraction.text import TfidfVectorizer
# # # # # from sklearn.metrics.pairwise import cosine_similarity
# # # # # import pandas as pd
# # # # # import numpy as np
# # # # # from typing import List, Dict, Tuple
# # # # # import re
# # # # # from .database import Kuppi, User, Student, Enrollment, Review, University, Department, Degree, Subject, Tutor

# # # # # class RecommendationEngine:
# # # # #     def __init__(self, db: Session):
# # # # #         self.db = db
# # # # #         self.tfidf_vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
# # # # #         self.kuppi_vectors = None
# # # # #         self.kuppi_df = None
# # # # #         self.student_vectors = None
# # # # #         self.student_df = None
        
# # # # #     def preprocess_text(self, text: str) -> str:
# # # # #         """Basic text preprocessing"""
# # # # #         if not text:
# # # # #             return ""
# # # # #         # Convert to lowercase
# # # # #         text = text.lower()
# # # # #         # Remove special characters and digits
# # # # #         text = re.sub(r'[^a-zA-Z\s]', '', text)
# # # # #         return text
    
# # # # #     def build_kuppi_vectors(self):
# # # # #         """Build TF-IDF vectors for all Kuppis"""
# # # # #         # Get all approved kuppis
# # # # #         kuppis = self.db.query(Kuppi).filter(Kuppi.status == 'APPROVED').all()
        
# # # # #         if not kuppis:
# # # # #             return
        
# # # # #         # Create a DataFrame with kuppi data
# # # # #         kuppi_data = []
# # # # #         for kuppi in kuppis:
# # # # #             # Get related information
# # # # #             university = self.db.query(University).filter(University.id == kuppi.university_id).first()
# # # # #             department = self.db.query(Department).filter(Department.id == kuppi.department_id).first()
# # # # #             degree = self.db.query(Degree).filter(Degree.id == kuppi.degree_id).first()
# # # # #             subject = self.db.query(Subject).filter(Subject.id == kuppi.subject_id).first()
# # # # #             tutor = self.db.query(User).filter(User.id == kuppi.tutor_id).first()
            
# # # # #             # Combine text fields for content similarity
# # # # #             combined_text = f"{kuppi.title} {kuppi.description} {subject.name if subject else ''} {subject.description if subject else ''}"
            
# # # # #             kuppi_data.append({
# # # # #                 'id': kuppi.id,
# # # # #                 'title': kuppi.title,
# # # # #                 'description': kuppi.description,
# # # # #                 'price': float(kuppi.price),
# # # # #                 'university_id': kuppi.university_id,
# # # # #                 'university_name': university.name if university else '',
# # # # #                 'department_id': kuppi.department_id,
# # # # #                 'department_name': department.name if department else '',
# # # # #                 'degree_id': kuppi.degree_id,
# # # # #                 'degree_name': degree.name if degree else '',
# # # # #                 'subject_id': kuppi.subject_id,
# # # # #                 'subject_name': subject.name if subject else '',
# # # # #                 'tutor_id': kuppi.tutor_id,
# # # # #                 'tutor_name': tutor.full_name if tutor else '',
# # # # #                 'combined_text': self.preprocess_text(combined_text)
# # # # #             })
        
# # # # #         self.kuppi_df = pd.DataFrame(kuppi_data)
        
# # # # #         # Create TF-IDF vectors
# # # # #         self.kuppi_vectors = self.tfidf_vectorizer.fit_transform(self.kuppi_df['combined_text'])
    
# # # # #     def build_student_vectors(self):
# # # # #         """Build interaction vectors for all students"""
# # # # #         # Get all students
# # # # #         students = self.db.query(Student).all()
        
# # # # #         if not students:
# # # # #             return
        
# # # # #         student_data = []
        
# # # # #         for student in students:
# # # # #             # Get student's enrollments
# # # # #             enrollments = self.db.query(Enrollment).filter(Enrollment.student_id == student.id).all()
# # # # #             enrolled_kuppi_ids = [e.kuppi_id for e in enrollments]
            
# # # # #             # Get student's reviews
# # # # #             reviews = self.db.query(Review).filter(Review.student_id == student.id).all()
# # # # #             reviewed_kuppi_ids = [r.kuppi_id for r in reviews]
            
# # # # #             # Get student's questions
# # # # #             questions = self.db.query(Question).filter(Question.student_id == student.id).all()
# # # # #             asked_kuppi_ids = [q.kuppi_id for q in questions]
            
# # # # #             # Combine all interactions
# # # # #             all_interacted_kuppi_ids = list(set(enrolled_kuppi_ids + reviewed_kuppi_ids + asked_kuppi_ids))
            
# # # # #             # Get the kuppis the student interacted with
# # # # #             interacted_kuppis = self.db.query(Kuppi).filter(Kuppi.id.in_(all_interacted_kuppi_ids)).all()
            
# # # # #             # Create a profile based on the content of interacted kuppis
# # # # #             profile_text = ""
# # # # #             for kuppi in interacted_kuppis:
# # # # #                 subject = self.db.query(Subject).filter(Subject.id == kuppi.subject_id).first()
# # # # #                 profile_text += f"{kuppi.title} {kuppi.description} {subject.name if subject else ''} "
            
# # # # #             student_data.append({
# # # # #                 'id': student.id,
# # # # #                 'university_id': student.university_id,
# # # # #                 'department_id': student.department_id,
# # # # #                 'degree_id': student.degree_id,
# # # # #                 'academic_year': student.academic_year,
# # # # #                 'enrolled_kuppi_ids': enrolled_kuppi_ids,
# # # # #                 'reviewed_kuppi_ids': reviewed_kuppi_ids,
# # # # #                 'asked_kuppi_ids': asked_kuppi_ids,
# # # # #                 'profile_text': self.preprocess_text(profile_text)
# # # # #             })
        
# # # # #         self.student_df = pd.DataFrame(student_data)
        
# # # # #         # Create TF-IDF vectors for student profiles
# # # # #         if not self.student_df['profile_text'].str.strip().empty:
# # # # #             self.student_vectors = self.tfidf_vectorizer.transform(self.student_df['profile_text'])
    
# # # # #     def get_recommendations(self, student_id: int, top_n: int = 5) -> List[Dict]:
# # # # #         """Get top-N recommendations for a student"""
# # # # #         # Build vectors if not already built
# # # # #         if self.kuppi_vectors is None:
# # # # #             self.build_kuppi_vectors()
        
# # # # #         if self.student_vectors is None:
# # # # #             self.build_student_vectors()
        
# # # # #         # Check if student exists
# # # # #         student_row = self.student_df[self.student_df['id'] == student_id]
# # # # #         if student_row.empty:
# # # # #             return []
        
# # # # #         student_idx = student_row.index[0]
# # # # #         student_vector = self.student_vectors[student_idx]
        
# # # # #         # Get student's enrolled kuppis to exclude them from recommendations
# # # # #         enrolled_kuppi_ids = student_row.iloc[0]['enrolled_kuppi_ids']
        
# # # # #         # Calculate cosine similarity between student and all kuppis
# # # # #         similarity_scores = cosine_similarity(student_vector, self.kuppi_vectors).flatten()
        
# # # # #         # Get indices of top similar kuppis
# # # # #         top_indices = similarity_scores.argsort()[-top_n*2:][::-1]  # Get more to filter out enrolled ones
        
# # # # #         # Filter out already enrolled kuppis and get top N
# # # # #         recommendations = []
# # # # #         for idx in top_indices:
# # # # #             kuppi_id = self.kuppi_df.iloc[idx]['id']
# # # # #             if kuppi_id not in enrolled_kuppi_ids:
# # # # #                 kuppi_data = self.kuppi_df.iloc[idx].to_dict()
# # # # #                 kuppi_data['similarity_score'] = float(similarity_scores[idx])
# # # # #                 recommendations.append(kuppi_data)
                
# # # # #                 if len(recommendations) >= top_n:
# # # # #                     break
        
# # # # #         return recommendations
    
# # # # #     def get_fallback_recommendations(self, student_id: int, top_n: int = 5) -> List[Dict]:
# # # # #         """Get fallback recommendations based on popular kuppis when student has no interaction history"""
# # # # #         # Get student's university, department, and degree
# # # # #         student = self.db.query(Student).filter(Student.id == student_id).first()
# # # # #         if not student:
# # # # #             return []
        
# # # # #         # Get popular kuppis from the same university/department/degree
# # # # #         kuppis = self.db.query(Kuppi).filter(
# # # # #             Kuppi.status == 'APPROVED',
# # # # #             Kuppi.university_id == student.university_id
# # # # #         ).limit(top_n * 2).all()
        
# # # # #         # If not enough kuppis from the same university, get from the same department
# # # # #         if len(kuppis) < top_n:
# # # # #             department_kuppis = self.db.query(Kuppi).filter(
# # # # #                 Kuppi.status == 'APPROVED',
# # # # #                 Kuppi.department_id == student.department_id,
# # # # #                 Kuppi.id.notin_([k.id for k in kuppis])
# # # # #             ).limit(top_n - len(kuppis)).all()
# # # # #             kuppis.extend(department_kuppis)
        
# # # # #         # If still not enough, get from the same degree
# # # # #         if len(kuppis) < top_n:
# # # # #             degree_kuppis = self.db.query(Kuppi).filter(
# # # # #                 Kuppi.status == 'APPROVED',
# # # # #                 Kuppi.degree_id == student.degree_id,
# # # # #                 Kuppi.id.notin_([k.id for k in kuppis])
# # # # #             ).limit(top_n - len(kuppis)).all()
# # # # #             kuppis.extend(degree_kuppis)
        
# # # # #         # If still not enough, get any approved kuppis
# # # # #         if len(kuppis) < top_n:
# # # # #             any_kuppis = self.db.query(Kuppi).filter(
# # # # #                 Kuppi.status == 'APPROVED',
# # # # #                 Kuppi.id.notin_([k.id for k in kuppis])
# # # # #             ).limit(top_n - len(kuppis)).all()
# # # # #             kuppis.extend(any_kuppis)
        
# # # # #         # Convert to recommendation format
# # # # #         recommendations = []
# # # # #         for kuppi in kuppis[:top_n]:
# # # # #             # Get related information
# # # # #             university = self.db.query(University).filter(University.id == kuppi.university_id).first()
# # # # #             department = self.db.query(Department).filter(Department.id == kuppi.department_id).first()
# # # # #             degree = self.db.query(Degree).filter(Degree.id == kuppi.degree_id).first()
# # # # #             subject = self.db.query(Subject).filter(Subject.id == kuppi.subject_id).first()
# # # # #             tutor = self.db.query(User).filter(User.id == kuppi.tutor_id).first()
            
# # # # #             recommendations.append({
# # # # #                 'id': kuppi.id,
# # # # #                 'title': kuppi.title,
# # # # #                 'description': kuppi.description,
# # # # #                 'price': float(kuppi.price),
# # # # #                 'university_id': kuppi.university_id,
# # # # #                 'university_name': university.name if university else '',
# # # # #                 'department_id': kuppi.department_id,
# # # # #                 'department_name': department.name if department else '',
# # # # #                 'degree_id': kuppi.degree_id,
# # # # #                 'degree_name': degree.name if degree else '',
# # # # #                 'subject_id': kuppi.subject_id,
# # # # #                 'subject_name': subject.name if subject else '',
# # # # #                 'tutor_id': kuppi.tutor_id,
# # # # #                 'tutor_name': tutor.full_name if tutor else '',
# # # # #                 'similarity_score': 0.5  # Default similarity score for fallback recommendations
# # # # #             })
        
# # # # #         return recommendations
    
# # # # #     def refresh_models(self):
# # # # #         """Refresh the recommendation models"""
# # # # #         self.build_kuppi_vectors()
# # # # #         self.build_student_vectors()

# # # # from sqlalchemy.orm import Session
# # # # from sklearn.feature_extraction.text import TfidfVectorizer
# # # # from sklearn.metrics.pairwise import cosine_similarity
# # # # import pandas as pd
# # # # import numpy as np
# # # # from typing import List, Dict, Tuple
# # # # import re
# # # # from .database import Kuppi, User, Student, Enrollment, Review, University, Department, Degree, Subject, Tutor

# # # # class RecommendationEngine:
# # # #     def __init__(self, db: Session):
# # # #         self.db = db
# # # #         self.tfidf_vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
# # # #         self.kuppi_vectors = None
# # # #         self.kuppi_df = None
# # # #         self.student_vectors = None
# # # #         self.student_df = None
        
# # # #     def preprocess_text(self, text: str) -> str:
# # # #         """Basic text preprocessing"""
# # # #         if not text:
# # # #             return ""
# # # #         # Convert to lowercase
# # # #         text = text.lower()
# # # #         # Remove special characters and digits
# # # #         text = re.sub(r'[^a-zA-Z\s]', '', text)
# # # #         return text
    
# # # #     def build_kuppi_vectors(self):
# # # #         """Build TF-IDF vectors for all Kuppis"""
# # # #         # Get all approved kuppis
# # # #         kuppis = self.db.query(Kuppi).filter(Kuppi.status == 'APPROVED').all()
        
# # # #         if not kuppis:
# # # #             return
        
# # # #         # Create a DataFrame with kuppi data
# # # #         kuppi_data = []
# # # #         for kuppi in kuppis:
# # # #             # Get related information
# # # #             university = self.db.query(University).filter(University.id == kuppi.university_id).first()
# # # #             department = self.db.query(Department).filter(Department.id == kuppi.department_id).first()
# # # #             degree = self.db.query(Degree).filter(Degree.id == kuppi.degree_id).first()
# # # #             subject = self.db.query(Subject).filter(Subject.id == kuppi.subject_id).first()
# # # #             tutor = self.db.query(User).filter(User.id == kuppi.tutor_id).first()
            
# # # #             # Combine text fields for content similarity
# # # #             combined_text = f"{kuppi.title} {kuppi.description} {subject.name if subject else ''} {subject.description if subject else ''}"
            
# # # #             kuppi_data.append({
# # # #                 'id': kuppi.id,
# # # #                 'title': kuppi.title,
# # # #                 'description': kuppi.description,
# # # #                 'price': float(kuppi.price),
# # # #                 'university_id': kuppi.university_id,
# # # #                 'university_name': university.name if university else '',
# # # #                 'department_id': kuppi.department_id,
# # # #                 'department_name': department.name if department else '',
# # # #                 'degree_id': kuppi.degree_id,
# # # #                 'degree_name': degree.name if degree else '',
# # # #                 'subject_id': kuppi.subject_id,
# # # #                 'subject_name': subject.name if subject else '',
# # # #                 'tutor_id': kuppi.tutor_id,
# # # #                 'tutor_name': tutor.full_name if tutor else '',
# # # #                 'combined_text': self.preprocess_text(combined_text)
# # # #             })
        
# # # #         self.kuppi_df = pd.DataFrame(kuppi_data)
        
# # # #         # Create TF-IDF vectors
# # # #         self.kuppi_vectors = self.tfidf_vectorizer.fit_transform(self.kuppi_df['combined_text'])
    
# # # #     def build_student_vectors(self):
# # # #         """Build interaction vectors for all students"""
# # # #         # Get all students
# # # #         students = self.db.query(Student).all()
        
# # # #         if not students:
# # # #             return
        
# # # #         student_data = []
        
# # # #         for student in students:
# # # #             # Get student's enrollments
# # # #             enrollments = self.db.query(Enrollment).filter(Enrollment.student_id == student.id).all()
# # # #             enrolled_kuppi_ids = [e.kuppi_id for e in enrollments]
            
# # # #             # Get student's reviews
# # # #             reviews = self.db.query(Review).filter(Review.student_id == student.id).all()
# # # #             reviewed_kuppi_ids = [r.kuppi_id for r in reviews]
            
# # # #             # Get student's questions
# # # #             questions = self.db.query(Question).filter(Question.student_id == student.id).all()
# # # #             asked_kuppi_ids = [q.kuppi_id for q in questions]
            
# # # #             # Combine all interactions
# # # #             all_interacted_kuppi_ids = list(set(enrolled_kuppi_ids + reviewed_kuppi_ids + asked_kuppi_ids))
            
# # # #             # Get the kuppis the student interacted with
# # # #             interacted_kuppis = self.db.query(Kuppi).filter(Kuppi.id.in_(all_interacted_kuppi_ids)).all()
            
# # # #             # Create a profile based on the content of interacted kuppis
# # # #             profile_text = ""
# # # #             for kuppi in interacted_kuppis:
# # # #                 subject = self.db.query(Subject).filter(Subject.id == kuppi.subject_id).first()
# # # #                 profile_text += f"{kuppi.title} {kuppi.description} {subject.name if subject else ''} "
            
# # # #             student_data.append({
# # # #                 'id': student.id,
# # # #                 'university_id': student.university_id,
# # # #                 'department_id': student.department_id,
# # # #                 'degree_id': student.degree_id,
# # # #                 'academic_year': student.academic_year,
# # # #                 'enrolled_kuppi_ids': enrolled_kuppi_ids,
# # # #                 'reviewed_kuppi_ids': reviewed_kuppi_ids,
# # # #                 'asked_kuppi_ids': asked_kuppi_ids,
# # # #                 'profile_text': self.preprocess_text(profile_text)
# # # #             })
        
# # # #         self.student_df = pd.DataFrame(student_data)
        
# # # #         # Create TF-IDF vectors for student profiles
# # # #         if not self.student_df['profile_text'].str.strip().empty:
# # # #             self.student_vectors = self.tfidf_vectorizer.transform(self.student_df['profile_text'])
    
# # # #     def get_recommendations(self, student_id: int, top_n: int = 5) -> List[Dict]:
# # # #         """Get top-N recommendations for a student"""
# # # #         # Build vectors if not already built
# # # #         if self.kuppi_vectors is None:
# # # #             self.build_kuppi_vectors()
        
# # # #         if self.student_vectors is None:
# # # #             self.build_student_vectors()
        
# # # #         # Check if student exists
# # # #         student_row = self.student_df[self.student_df['id'] == student_id]
# # # #         if student_row.empty:
# # # #             return []
        
# # # #         student_idx = student_row.index[0]
# # # #         student_vector = self.student_vectors[student_idx]
        
# # # #         # Get student's enrolled kuppis to exclude them from recommendations
# # # #         enrolled_kuppi_ids = student_row.iloc[0]['enrolled_kuppi_ids']
        
# # # #         # Calculate cosine similarity between student and all kuppis
# # # #         similarity_scores = cosine_similarity(student_vector, self.kuppi_vectors).flatten()
        
# # # #         # Get indices of top similar kuppis
# # # #         top_indices = similarity_scores.argsort()[-top_n*2:][::-1]  # Get more to filter out enrolled ones
        
# # # #         # Filter out already enrolled kuppis and get top N
# # # #         recommendations = []
# # # #         for idx in top_indices:
# # # #             kuppi_id = self.kuppi_df.iloc[idx]['id']
# # # #             if kuppi_id not in enrolled_kuppi_ids:
# # # #                 kuppi_data = self.kuppi_df.iloc[idx].to_dict()
# # # #                 kuppi_data['similarity_score'] = float(similarity_scores[idx])
# # # #                 recommendations.append(kuppi_data)
                
# # # #                 if len(recommendations) >= top_n:
# # # #                     break
        
# # # #         return recommendations
    
# # # #     def get_fallback_recommendations(self, student_id: int, top_n: int = 5) -> List[Dict]:
# # # #         """Get fallback recommendations based on popular kuppis when student has no interaction history"""
# # # #         # Get student's university, department, and degree
# # # #         student = self.db.query(Student).filter(Student.id == student_id).first()
# # # #         if not student:
# # # #             return []
        
# # # #         # Get popular kuppis from the same university/department/degree
# # # #         kuppis = self.db.query(Kuppi).filter(
# # # #             Kuppi.status == 'APPROVED',
# # # #             Kuppi.university_id == student.university_id
# # # #         ).limit(top_n * 2).all()
        
# # # #         # If not enough kuppis from the same university, get from the same department
# # # #         if len(kuppis) < top_n:
# # # #             department_kuppis = self.db.query(Kuppi).filter(
# # # #                 Kuppi.status == 'APPROVED',
# # # #                 Kuppi.department_id == student.department_id,
# # # #                 Kuppi.id.notin_([k.id for k in kuppis])
# # # #             ).limit(top_n - len(kuppis)).all()
# # # #             kuppis.extend(department_kuppis)
        
# # # #         # If still not enough, get from the same degree
# # # #         if len(kuppis) < top_n:
# # # #             degree_kuppis = self.db.query(Kuppi).filter(
# # # #                 Kuppi.status == 'APPROVED',
# # # #                 Kuppi.degree_id == student.degree_id,
# # # #                 Kuppi.id.notin_([k.id for k in kuppis])
# # # #             ).limit(top_n - len(kuppis)).all()
# # # #             kuppis.extend(degree_kuppis)
        
# # # #         # If still not enough, get any approved kuppis
# # # #         if len(kuppis) < top_n:
# # # #             any_kuppis = self.db.query(Kuppi).filter(
# # # #                 Kuppi.status == 'APPROVED',
# # # #                 Kuppi.id.notin_([k.id for k in kuppis])
# # # #             ).limit(top_n - len(kuppis)).all()
# # # #             kuppis.extend(any_kuppis)
        
# # # #         # Convert to recommendation format
# # # #         recommendations = []
# # # #         for kuppi in kuppis[:top_n]:
# # # #             # Get related information
# # # #             university = self.db.query(University).filter(University.id == kuppi.university_id).first()
# # # #             department = self.db.query(Department).filter(Department.id == kuppi.department_id).first()
# # # #             degree = self.db.query(Degree).filter(Degree.id == kuppi.degree_id).first()
# # # #             subject = self.db.query(Subject).filter(Subject.id == kuppi.subject_id).first()
# # # #             tutor = self.db.query(User).filter(User.id == kuppi.tutor_id).first()
            
# # # #             recommendations.append({
# # # #                 'id': kuppi.id,
# # # #                 'title': kuppi.title,
# # # #                 'description': kuppi.description,
# # # #                 'price': float(kuppi.price),
# # # #                 'university_id': kuppi.university_id,
# # # #                 'university_name': university.name if university else '',
# # # #                 'department_id': kuppi.department_id,
# # # #                 'department_name': department.name if department else '',
# # # #                 'degree_id': kuppi.degree_id,
# # # #                 'degree_name': degree.name if degree else '',
# # # #                 'subject_id': kuppi.subject_id,
# # # #                 'subject_name': subject.name if subject else '',
# # # #                 'tutor_id': kuppi.tutor_id,
# # # #                 'tutor_name': tutor.full_name if tutor else '',
# # # #                 'similarity_score': 0.5  # Default similarity score for fallback recommendations
# # # #             })
        
# # # #         return recommendations
    
# # # #     def refresh_models(self):
# # # #         """Refresh the recommendation models"""
# # # #         self.build_kuppi_vectors()
# # # #         self.build_student_vectors()

# # # from sqlalchemy.orm import Session
# # # from sklearn.feature_extraction.text import TfidfVectorizer
# # # from sklearn.metrics.pairwise import cosine_similarity
# # # import pandas as pd
# # # import numpy as np
# # # from typing import List, Dict, Tuple
# # # import re
# # # from .database import Kuppi, User, Student, Enrollment, Review, University, Department, Degree, Subject, Tutor

# # # class RecommendationEngine:
# # #     def __init__(self, db: Session):
# # #         self.db = db
# # #         self.tfidf_vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
# # #         self.kuppi_vectors = None
# # #         self.kuppi_df = None
# # #         self.student_vectors = None
# # #         self.student_df = None
        
# # #     def preprocess_text(self, text: str) -> str:
# # #         """Basic text preprocessing"""
# # #         if not text:
# # #             return ""
# # #         # Convert to lowercase
# # #         text = text.lower()
# # #         # Remove special characters and digits
# # #         text = re.sub(r'[^a-zA-Z\s]', '', text)
# # #         return text
    
# # #     def build_kuppi_vectors(self):
# # #         """Build TF-IDF vectors for all Kuppis"""
# # #         # Get all approved kuppis
# # #         kuppis = self.db.query(Kuppi).filter(Kuppi.status == 'APPROVED').all()
        
# # #         if not kuppis:
# # #             return
        
# # #         # Create a DataFrame with kuppi data
# # #         kuppi_data = []
# # #         for kuppi in kuppis:
# # #             # Get related information
# # #             university = self.db.query(University).filter(University.id == kuppi.university_id).first()
# # #             department = self.db.query(Department).filter(Department.id == kuppi.department_id).first()
# # #             degree = self.db.query(Degree).filter(Degree.id == kuppi.degree_id).first()
# # #             subject = self.db.query(Subject).filter(Subject.id == kuppi.subject_id).first()
# # #             tutor = self.db.query(User).filter(User.id == kuppi.tutor_id).first()
            
# # #             # Combine text fields for content similarity
# # #             combined_text = f"{kuppi.title} {kuppi.description} {subject.name if subject else ''} {subject.description if subject else ''}"
            
# # #             kuppi_data.append({
# # #                 'id': kuppi.id,
# # #                 'title': kuppi.title,
# # #                 'description': kuppi.description,
# # #                 'price': float(kuppi.price),
# # #                 'university_id': kuppi.university_id,
# # #                 'university_name': university.name if university else '',
# # #                 'department_id': kuppi.department_id,
# # #                 'department_name': department.name if department else '',
# # #                 'degree_id': kuppi.degree_id,
# # #                 'degree_name': degree.name if degree else '',
# # #                 'subject_id': kuppi.subject_id,
# # #                 'subject_name': subject.name if subject else '',
# # #                 'tutor_id': kuppi.tutor_id,
# # #                 'tutor_name': tutor.full_name if tutor else '',
# # #                 'combined_text': self.preprocess_text(combined_text)
# # #             })
        
# # #         self.kuppi_df = pd.DataFrame(kuppi_data)
        
# # #         # Create TF-IDF vectors
# # #         self.kuppi_vectors = self.tfidf_vectorizer.fit_transform(self.kuppi_df['combined_text'])
    
# # #     def build_student_vectors(self):
# # #         """Build interaction vectors for all students"""
# # #         # Get all students
# # #         students = self.db.query(Student).all()
        
# # #         if not students:
# # #             return
        
# # #         student_data = []
        
# # #         for student in students:
# # #             # Get student's enrollments
# # #             enrollments = self.db.query(Enrollment).filter(Enrollment.student_id == student.id).all()
# # #             enrolled_kuppi_ids = [e.kuppi_id for e in enrollments]
            
# # #             # Get student's reviews
# # #             reviews = self.db.query(Review).filter(Review.student_id == student.id).all()
# # #             reviewed_kuppi_ids = [r.kuppi_id for r in reviews]
            
# # #             # Get student's questions
# # #             questions = self.db.query(Question).filter(Question.student_id == student.id).all()
# # #             asked_kuppi_ids = [q.kuppi_id for q in questions]
            
# # #             # Combine all interactions
# # #             all_interacted_kuppi_ids = list(set(enrolled_kuppi_ids + reviewed_kuppi_ids + asked_kuppi_ids))
            
# # #             # Get the kuppis the student interacted with
# # #             interacted_kuppis = self.db.query(Kuppi).filter(Kuppi.id.in_(all_interacted_kuppi_ids)).all()
            
# # #             # Create a profile based on the content of interacted kuppis
# # #             profile_text = ""
# # #             for kuppi in interacted_kuppis:
# # #                 subject = self.db.query(Subject).filter(Subject.id == kuppi.subject_id).first()
# # #                 profile_text += f"{kuppi.title} {kuppi.description} {subject.name if subject else ''} "
            
# # #             student_data.append({
# # #                 'id': student.id,
# # #                 'university_id': student.university_id,
# # #                 'department_id': student.department_id,
# # #                 'degree_id': student.degree_id,
# # #                 'academic_year': student.academic_year,
# # #                 'enrolled_kuppi_ids': enrolled_kuppi_ids,
# # #                 'reviewed_kuppi_ids': reviewed_kuppi_ids,
# # #                 'asked_kuppi_ids': asked_kuppi_ids,
# # #                 'profile_text': self.preprocess_text(profile_text)
# # #             })
        
# # #         self.student_df = pd.DataFrame(student_data)
        
# # #         # Create TF-IDF vectors for student profiles
# # #         if not self.student_df['profile_text'].str.strip().empty:
# # #             self.student_vectors = self.tfidf_vectorizer.transform(self.student_df['profile_text'])
    
# # #     def get_recommendations(self, student_id: int, top_n: int = 5) -> List[Dict]:
# # #         """Get top-N recommendations for a student"""
# # #         # Build vectors if not already built
# # #         if self.kuppi_vectors is None:
# # #             self.build_kuppi_vectors()
        
# # #         if self.student_vectors is None:
# # #             self.build_student_vectors()
        
# # #         # Check if student exists
# # #         student_row = self.student_df[self.student_df['id'] == student_id]
# # #         if student_row.empty:
# # #             return []
        
# # #         student_idx = student_row.index[0]
# # #         student_vector = self.student_vectors[student_idx]
        
# # #         # Get student's enrolled kuppis to exclude them from recommendations
# # #         enrolled_kuppi_ids = student_row.iloc[0]['enrolled_kuppi_ids']
        
# # #         # Calculate cosine similarity between student and all kuppis
# # #         similarity_scores = cosine_similarity(student_vector, self.kuppi_vectors).flatten()
        
# # #         # Get indices of top similar kuppis
# # #         top_indices = similarity_scores.argsort()[-top_n*2:][::-1]  # Get more to filter out enrolled ones
        
# # #         # Filter out already enrolled kuppis and get top N
# # #         recommendations = []
# # #         for idx in top_indices:
# # #             kuppi_id = self.kuppi_df.iloc[idx]['id']
# # #             if kuppi_id not in enrolled_kuppi_ids:
# # #                 kuppi_data = self.kuppi_df.iloc[idx].to_dict()
# # #                 kuppi_data['similarity_score'] = float(similarity_scores[idx])
# # #                 recommendations.append(kuppi_data)
                
# # #                 if len(recommendations) >= top_n:
# # #                     break
        
# # #         return recommendations
    
# # #     def get_fallback_recommendations(self, student_id: int, top_n: int = 5) -> List[Dict]:
# # #         """Get fallback recommendations based on popular kuppis when student has no interaction history"""
# # #         # Get student's university, department, and degree
# # #         student = self.db.query(Student).filter(Student.id == student_id).first()
# # #         if not student:
# # #             return []
        
# # #         # Get popular kuppis from the same university/department/degree
# # #         kuppis = self.db.query(Kuppi).filter(
# # #             Kuppi.status == 'APPROVED',
# # #             Kuppi.university_id == student.university_id
# # #         ).limit(top_n * 2).all()
        
# # #         # If not enough kuppis from the same university, get from the same department
# # #         if len(kuppis) < top_n:
# # #             department_kuppis = self.db.query(Kuppi).filter(
# # #                 Kuppi.status == 'APPROVED',
# # #                 Kuppi.department_id == student.department_id,
# # #                 Kuppi.id.notin_([k.id for k in kuppis])
# # #             ).limit(top_n - len(kuppis)).all()
# # #             kuppis.extend(department_kuppis)
        
# # #         # If still not enough, get from the same degree
# # #         if len(kuppis) < top_n:
# # #             degree_kuppis = self.db.query(Kuppi).filter(
# # #                 Kuppi.status == 'APPROVED',
# # #                 Kuppi.degree_id == student.degree_id,
# # #                 Kuppi.id.notin_([k.id for k in kuppis])
# # #             ).limit(top_n - len(kuppis)).all()
# # #             kuppis.extend(degree_kuppis)
        
# # #         # If still not enough, get any approved kuppis
# # #         if len(kuppis) < top_n:
# # #             any_kuppis = self.db.query(Kuppi).filter(
# # #                 Kuppi.status == 'APPROVED',
# # #                 Kuppi.id.notin_([k.id for k in kuppis])
# # #             ).limit(top_n - len(kuppis)).all()
# # #             kuppis.extend(any_kuppis)
        
# # #         # Convert to recommendation format
# # #         recommendations = []
# # #         for kuppi in kuppis[:top_n]:
# # #             # Get related information
# # #             university = self.db.query(University).filter(University.id == kuppi.university_id).first()
# # #             department = self.db.query(Department).filter(Department.id == kuppi.department_id).first()
# # #             degree = self.db.query(Degree).filter(Degree.id == kuppi.degree_id).first()
# # #             subject = self.db.query(Subject).filter(Subject.id == kuppi.subject_id).first()
# # #             tutor = self.db.query(User).filter(User.id == kuppi.tutor_id).first()
            
# # #             recommendations.append({
# # #                 'id': kuppi.id,
# # #                 'title': kuppi.title,
# # #                 'description': kuppi.description,
# # #                 'price': float(kuppi.price),
# # #                 'university_id': kuppi.university_id,
# # #                 'university_name': university.name if university else '',
# # #                 'department_id': kuppi.department_id,
# # #                 'department_name': department.name if department else '',
# # #                 'degree_id': kuppi.degree_id,
# # #                 'degree_name': degree.name if degree else '',
# # #                 'subject_id': kuppi.subject_id,
# # #                 'subject_name': subject.name if subject else '',
# # #                 'tutor_id': kuppi.tutor_id,
# # #                 'tutor_name': tutor.full_name if tutor else '',
# # #                 'similarity_score': 0.5  # Default similarity score for fallback recommendations
# # #             })
        
# # #         return recommendations
    
# # #     def refresh_models(self):
# # #         """Refresh the recommendation models"""
# # #         self.build_kuppi_vectors()
# # #         self.build_student_vectors()

# # from sqlalchemy.orm import Session
# # from sklearn.feature_extraction.text import TfidfVectorizer
# # from .database import Kuppi, User, Student, Enrollment, Review, University, Department, Degree, Subject, Tutor, Question

# # from sklearn.metrics.pairwise import cosine_similarity
# # import pandas as pd
# # import numpy as np
# # from typing import List, Dict, Tuple
# # import re
# # from decimal import Decimal
# # from .database import Kuppi, User, Student, Enrollment, Review, University, Department, Degree, Subject, Tutor

# # class RecommendationEngine:
# #     def __init__(self, db: Session):
# #         self.db = db
# #         self.tfidf_vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
# #         self.kuppi_vectors = None
# #         self.kuppi_df = None
# #         self.student_vectors = None
# #         self.student_df = None
        
# #     def preprocess_text(self, text: str) -> str:
# #         """Basic text preprocessing"""
# #         if not text:
# #             return ""
# #         # Convert to lowercase
# #         text = text.lower()
# #         # Remove special characters and digits
# #         text = re.sub(r'[^a-zA-Z\s]', '', text)
# #         return text
    
# #     def build_kuppi_vectors(self):
# #         """Build TF-IDF vectors for all Kuppis"""
# #         # Get all approved kuppis
# #         kuppis = self.db.query(Kuppi).filter(Kuppi.status == 'APPROVED').all()
        
# #         if not kuppis:
# #             return
        
# #         # Create a DataFrame with kuppi data
# #         kuppi_data = []
# #         for kuppi in kuppis:
# #             # Get related information
# #             university = self.db.query(University).filter(University.id == kuppi.university_id).first()
# #             department = self.db.query(Department).filter(Department.id == kuppi.department_id).first()
# #             degree = self.db.query(Degree).filter(Degree.id == kuppi.degree_id).first()
# #             subject = self.db.query(Subject).filter(Subject.id == kuppi.subject_id).first()
# #             tutor = self.db.query(User).filter(User.id == kuppi.tutor_id).first()
            
# #             # Combine text fields for content similarity
# #             combined_text = f"{kuppi.title} {kuppi.description} {subject.name if subject else ''} {subject.description if subject else ''}"
            
# #             kuppi_data.append({
# #                 'id': kuppi.id,
# #                 'title': kuppi.title,
# #                 'description': kuppi.description,
# #                 'price': float(kuppi.price) if kuppi.price else 0.0,  # Convert Decimal to float
# #                 'university_id': kuppi.university_id,
# #                 'university_name': university.name if university else '',
# #                 'department_id': kuppi.department_id,
# #                 'department_name': department.name if department else '',
# #                 'degree_id': kuppi.degree_id,
# #                 'degree_name': degree.name if degree else '',
# #                 'subject_id': kuppi.subject_id,
# #                 'subject_name': subject.name if subject else '',
# #                 'tutor_id': kuppi.tutor_id,
# #                 'tutor_name': tutor.full_name if tutor else '',
# #                 'combined_text': self.preprocess_text(combined_text)
# #             })
        
# #         self.kuppi_df = pd.DataFrame(kuppi_data)
        
# #         # Create TF-IDF vectors
# #         self.kuppi_vectors = self.tfidf_vectorizer.fit_transform(self.kuppi_df['combined_text'])
    
# #     def build_student_vectors(self):
# #         """Build interaction vectors for all students"""
# #         # Get all students
# #         students = self.db.query(Student).all()
        
# #         if not students:
# #             return
        
# #         student_data = []
        
# #         for student in students:
# #             # Get student's enrollments
# #             enrollments = self.db.query(Enrollment).filter(Enrollment.student_id == student.id).all()
# #             enrolled_kuppi_ids = [e.kuppi_id for e in enrollments]
            
# #             # Get student's reviews
# #             reviews = self.db.query(Review).filter(Review.student_id == student.id).all()
# #             reviewed_kuppi_ids = [r.kuppi_id for r in reviews]
            
# #             # Get student's questions
# #             questions = self.db.query(Question).filter(Question.student_id == student.id).all()
# #             asked_kuppi_ids = [q.kuppi_id for q in questions]
            
# #             # Combine all interactions
# #             all_interacted_kuppi_ids = list(set(enrolled_kuppi_ids + reviewed_kuppi_ids + asked_kuppi_ids))
            
# #             # Get the kuppis the student interacted with
# #             interacted_kuppis = self.db.query(Kuppi).filter(Kuppi.id.in_(all_interacted_kuppi_ids)).all()
            
# #             # Create a profile based on the content of interacted kuppis
# #             profile_text = ""
# #             for kuppi in interacted_kuppis:
# #                 subject = self.db.query(Subject).filter(Subject.id == kuppi.subject_id).first()
# #                 profile_text += f"{kuppi.title} {kuppi.description} {subject.name if subject else ''} "
            
# #             student_data.append({
# #                 'id': student.id,
# #                 'university_id': student.university_id,
# #                 'department_id': student.department_id,
# #                 'degree_id': student.degree_id,
# #                 'academic_year': student.academic_year,
# #                 'enrolled_kuppi_ids': enrolled_kuppi_ids,
# #                 'reviewed_kuppi_ids': reviewed_kuppi_ids,
# #                 'asked_kuppi_ids': asked_kuppi_ids,
# #                 'profile_text': self.preprocess_text(profile_text)
# #             })
        
# #         self.student_df = pd.DataFrame(student_data)
        
# #         # Create TF-IDF vectors for student profiles
# #         if not self.student_df['profile_text'].str.strip().empty:
# #             self.student_vectors = self.tfidf_vectorizer.transform(self.student_df['profile_text'])
    
# #     def get_recommendations(self, student_id: int, top_n: int = 5) -> List[Dict]:
# #         """Get top-N recommendations for a student"""
# #         # Build vectors if not already built
# #         if self.kuppi_vectors is None:
# #             self.build_kuppi_vectors()
        
# #         if self.student_vectors is None:
# #             self.build_student_vectors()
        
# #         # Check if student exists
# #         student_row = self.student_df[self.student_df['id'] == student_id]
# #         if student_row.empty:
# #             return []
        
# #         student_idx = student_row.index[0]
# #         student_vector = self.student_vectors[student_idx]
        
# #         # Get student's enrolled kuppis to exclude them from recommendations
# #         enrolled_kuppi_ids = student_row.iloc[0]['enrolled_kuppi_ids']
        
# #         # Calculate cosine similarity between student and all kuppis
# #         similarity_scores = cosine_similarity(student_vector, self.kuppi_vectors).flatten()
        
# #         # Get indices of top similar kuppis
# #         top_indices = similarity_scores.argsort()[-top_n*2:][::-1]  # Get more to filter out enrolled ones
        
# #         # Filter out already enrolled kuppis and get top N
# #         recommendations = []
# #         for idx in top_indices:
# #             kuppi_id = self.kuppi_df.iloc[idx]['id']
# #             if kuppi_id not in enrolled_kuppi_ids:
# #                 kuppi_data = self.kuppi_df.iloc[idx].to_dict()
# #                 kuppi_data['similarity_score'] = float(similarity_scores[idx])
# #                 recommendations.append(kuppi_data)
                
# #                 if len(recommendations) >= top_n:
# #                     break
        
# #         return recommendations
    
# #     def get_fallback_recommendations(self, student_id: int, top_n: int = 5) -> List[Dict]:
# #         """Get fallback recommendations based on popular kuppis when student has no interaction history"""
# #         # Get student's university, department, and degree
# #         student = self.db.query(Student).filter(Student.id == student_id).first()
# #         if not student:
# #             return []
        
# #         # Get popular kuppis from the same university/department/degree
# #         kuppis = self.db.query(Kuppi).filter(
# #             Kuppi.status == 'APPROVED',
# #             Kuppi.university_id == student.university_id
# #         ).limit(top_n * 2).all()
        
# #         # If not enough kuppis from the same university, get from the same department
# #         if len(kuppis) < top_n:
# #             department_kuppis = self.db.query(Kuppi).filter(
# #                 Kuppi.status == 'APPROVED',
# #                 Kuppi.department_id == student.department_id,
# #                 Kuppi.id.notin_([k.id for k in kuppis])
# #             ).limit(top_n - len(kuppis)).all()
# #             kuppis.extend(department_kuppis)
        
# #         # If still not enough, get from the same degree
# #         if len(kuppis) < top_n:
# #             degree_kuppis = self.db.query(Kuppi).filter(
# #                 Kuppi.status == 'APPROVED',
# #                 Kuppi.degree_id == student.degree_id,
# #                 Kuppi.id.notin_([k.id for k in kuppis])
# #             ).limit(top_n - len(kuppis)).all()
# #             kuppis.extend(degree_kuppis)
        
# #         # If still not enough, get any approved kuppis
# #         if len(kuppis) < top_n:
# #             any_kuppis = self.db.query(Kuppi).filter(
# #                 Kuppi.status == 'APPROVED',
# #                 Kuppi.id.notin_([k.id for k in kuppis])
# #             ).limit(top_n - len(kuppis)).all()
# #             kuppis.extend(any_kuppis)
        
# #         # Convert to recommendation format
# #         recommendations = []
# #         for kuppi in kuppis[:top_n]:
# #             # Get related information
# #             university = self.db.query(University).filter(University.id == kuppi.university_id).first()
# #             department = self.db.query(Department).filter(Department.id == kuppi.department_id).first()
# #             degree = self.db.query(Degree).filter(Degree.id == kuppi.degree_id).first()
# #             subject = self.db.query(Subject).filter(Subject.id == kuppi.subject_id).first()
# #             tutor = self.db.query(User).filter(User.id == kuppi.tutor_id).first()
            
# #             recommendations.append({
# #                 'id': kuppi.id,
# #                 'title': kuppi.title,
# #                 'description': kuppi.description,
# #                 'price': float(kuppi.price) if kuppi.price else 0.0,  # Convert Decimal to float
# #                 'university_id': kuppi.university_id,
# #                 'university_name': university.name if university else '',
# #                 'department_id': kuppi.department_id,
# #                 'department_name': department.name if department else '',
# #                 'degree_id': kuppi.degree_id,
# #                 'degree_name': degree.name if degree else '',
# #                 'subject_id': kuppi.subject_id,
# #                 'subject_name': subject.name if subject else '',
# #                 'tutor_id': kuppi.tutor_id,
# #                 'tutor_name': tutor.full_name if tutor else '',
# #                 'similarity_score': 0.5  # Default similarity score for fallback recommendations
# #             })
        
# #         return recommendations
    
# #     def refresh_models(self):
# #         """Refresh the recommendation models"""
# #         self.build_kuppi_vectors()
# #         self.build_student_vectors()

# from sqlalchemy.orm import Session
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
# import pandas as pd
# import re

# from .database import (
#     User, Student, Enrollment, Review, University,
#     Department, Degree, Subject, Tutor, Kuppi, Question
# )

# class RecommendationEngine:
#     def __init__(self, db: Session):
#         self.db = db
#         self.vectorizer = TfidfVectorizer(stop_words="english", max_features=5000)
#         self.kuppi_df = None
#         self.kuppi_vectors = None
#         self.student_df = None
#         self.student_vectors = None

#     def preprocess(self, text: str) -> str:
#         if not text:
#             return ""
#         text = text.lower()
#         return re.sub(r"[^a-z\s]", "", text)

#     def build_kuppi_vectors(self):
#         kuppis = self.db.query(Kuppi).filter(Kuppi.status == "APPROVED").all()
#         if not kuppis:
#             return

#         data = []
#         for k in kuppis:
#             subject = self.db.query(Subject).get(k.subject_id)
#             tutor = self.db.query(User).get(k.tutor_id)
#             university = self.db.query(University).get(k.university_id)
#             department = self.db.query(Department).get(k.department_id)
#             degree = self.db.query(Degree).get(k.degree_id)

#             text = f"{k.title} {k.description} {subject.name if subject else ''}"

#             data.append({
#                 "id": k.id,
#                 "title": k.title,
#                 "description": k.description,
#                 "price": float(k.price or 0),
#                 "university_name": university.name if university else "",
#                 "department_name": department.name if department else "",
#                 "degree_name": degree.name if degree else "",
#                 "subject_name": subject.name if subject else "",
#                 "tutor_name": tutor.full_name if tutor else "",
#                 "combined_text": self.preprocess(text)
#             })

#         self.kuppi_df = pd.DataFrame(data)
#         self.kuppi_vectors = self.vectorizer.fit_transform(self.kuppi_df["combined_text"])

#     def build_student_vectors(self):
#         students = self.db.query(Student).all()
#         profiles = []

#         for s in students:
#             enrollments = self.db.query(Enrollment).filter_by(student_id=s.id).all()
#             reviews = self.db.query(Review).filter_by(student_id=s.id).all()
#             questions = self.db.query(Question).filter_by(student_id=s.id).all()

#             kuppi_ids = list(set(
#                 [e.kuppi_id for e in enrollments] +
#                 [r.kuppi_id for r in reviews] +
#                 [q.kuppi_id for q in questions]
#             ))

#             text = ""
#             for kid in kuppi_ids:
#                 k = self.db.query(Kuppi).get(kid)
#                 if k:
#                     text += f"{k.title} {k.description} "

#             profiles.append({
#                 "id": s.id,
#                 "profile_text": self.preprocess(text),
#                 "enrolled_ids": [e.kuppi_id for e in enrollments]
#             })

#         self.student_df = pd.DataFrame(profiles)
#         self.student_vectors = self.vectorizer.transform(self.student_df["profile_text"])

#     def get_recommendations(self, student_id: int, top_n: int = 5):
#         if self.kuppi_vectors is None:
#             self.build_kuppi_vectors()
#         if self.student_vectors is None:
#             self.build_student_vectors()

#         student_row = self.student_df[self.student_df["id"] == student_id]
#         if student_row.empty:
#             return []

#         idx = student_row.index[0]
#         student_vector = self.student_vectors[idx]
#         enrolled_ids = student_row.iloc[0]["enrolled_ids"]

#         scores = cosine_similarity(student_vector, self.kuppi_vectors).flatten()
#         top_indices = scores.argsort()[::-1]

#         results = []
#         for i in top_indices:
#             if self.kuppi_df.iloc[i]["id"] in enrolled_ids:
#                 continue
#             item = self.kuppi_df.iloc[i].to_dict()
#             item["similarity_score"] = float(scores[i])
#             results.append(item)
#             if len(results) >= top_n:
#                 break

#         return results

#     def refresh_models(self):
#         self.build_kuppi_vectors()
#         self.build_student_vectors()


from sqlalchemy.orm import Session
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np
import re
from datetime import datetime

from .database import (
    User, Student, Enrollment, Review, University,
    Department, Degree, Subject, Tutor, Kuppi, Question
)

class RecommendationEngine:
    def __init__(self, db: Session):
        self.db = db
        self.vectorizer = TfidfVectorizer(
            stop_words="english",
            max_features=8000,
            ngram_range=(1, 2)  # bigrams for better text understanding
        )
        self.kuppi_df = None
        self.kuppi_vectors = None
        self.student_df = None
        self.student_vectors = None
        self.student_enrollments = {}  # student_id (user_id) → set of enrolled kuppi_ids

    def preprocess(self, text: str) -> str:
        if not text:
            return ""
        text = text.lower()
        text = re.sub(r"[^a-z\s]", "", text)
        return text

    def build_kuppi_vectors(self):
        kuppis = self.db.query(Kuppi).filter(Kuppi.status == "APPROVED").all()
        if not kuppis:
            return

        data = []
        for k in kuppis:
            subject = self.db.query(Subject).get(k.subject_id)
            tutor = self.db.query(User).get(k.tutor_id)
            university = self.db.query(University).get(k.university_id)
            department = self.db.query(Department).get(k.department_id)
            degree = self.db.query(Degree).get(k.degree_id)

            # Enhanced text representation
            text_parts = [
                k.title or "",
                k.description or "",
                subject.name if subject else "",
                subject.subject_code if subject else "",
                tutor.full_name if tutor else "",
                university.name if university else "",
                department.name if department else "",
                degree.name if degree else "",
            ]
            combined_text = " ".join(text_parts)
            processed_text = self.preprocess(combined_text)

            # Metadata for scoring
            avg_rating = self._get_average_rating(k)
            enrollment_count = self._get_enrollment_count(k)
            days_old = (datetime.utcnow() - k.created_at).days if k.created_at else 9999

            data.append({
                "id": k.id,
                "title": k.title,
                "description": k.description,
                "price": float(k.price or 0),
                "university_name": university.name if university else "",
                "department_name": department.name if department else "",
                "degree_name": degree.name if degree else "",
                "subject_name": subject.name if subject else "",
                "tutor_name": tutor.full_name if tutor else "",
                "tutor_id": tutor.id if tutor else None,
                "avg_rating": avg_rating,
                "enrollment_count": enrollment_count,
                "days_old": days_old,
                "combined_text": processed_text,
                "university_id": k.university_id,
                "department_id": k.department_id,
                "degree_id": k.degree_id,
                "academic_year": k.academic_year,
            })

        self.kuppi_df = pd.DataFrame(data)
        self.kuppi_vectors = self.vectorizer.fit_transform(self.kuppi_df["combined_text"])

    def _get_average_rating(self, kuppi: Kuppi) -> float:
        reviews = self.db.query(Review).filter(Review.kuppi_id == kuppi.id).all()
        if not reviews:
            return 3.0  # neutral default
        return sum(r.rating for r in reviews) / len(reviews)

    def _get_enrollment_count(self, kuppi: Kuppi) -> int:
        return self.db.query(Enrollment).filter(Enrollment.kuppi_id == kuppi.id).count()

    def build_student_vectors(self):
        students = self.db.query(Student).all()
        profiles = []
        self.student_enrollments = {}

        for s in students:
            # FIXED: Use s.id instead of s.user_id (Student.id == User.id)
            enrollments = self.db.query(Enrollment).filter_by(student_id=s.id).all()
            questions = self.db.query(Question).filter_by(student_id=s.id).all()
            reviews = self.db.query(Review).filter_by(student_id=s.id).all()

            kuppi_ids = set()
            text_parts = []

            for e in enrollments:
                k = self.db.query(Kuppi).get(e.kuppi_id)
                if k:
                    text_parts.append(f"{k.title} {k.description}")
                    kuppi_ids.add(k.id)

            for q in questions:
                k = self.db.query(Kuppi).get(q.kuppi_id)
                if k:
                    text_parts.append(f"{k.title} {k.description}")
                    kuppi_ids.add(k.id)

            for r in reviews:
                k = self.db.query(Kuppi).get(r.kuppi_id)
                if k:
                    text_parts.append(f"{k.title} {k.description}")
                    kuppi_ids.add(k.id)

            profile_text = " ".join(text_parts)
            processed_text = self.preprocess(profile_text)

            profiles.append({
                "id": s.id,  # FIXED: Use s.id (which is the user's ID)
                "profile_text": processed_text,
                "university_id": s.university_id,
                "department_id": s.department_id,
                "degree_id": s.degree_id,
                "academic_year": s.academic_year,
            })

            self.student_enrollments[s.id] = kuppi_ids  # FIXED: s.id

        self.student_df = pd.DataFrame(profiles)
        if not self.student_df.empty:
            self.student_vectors = self.vectorizer.transform(self.student_df["profile_text"])

    def get_recommendations(self, student_id: int, top_n: int = 8):
        if self.kuppi_df is None or self.kuppi_vectors is None:
            self.build_kuppi_vectors()
        if self.student_df is None or self.student_vectors is None:
            self.build_student_vectors()

        student_row = self.student_df[self.student_df["id"] == student_id]
        if student_row.empty:
            return self._get_cold_start_recommendations(student_id, top_n)

        idx = student_row.index[0]
        student_vector = self.student_vectors[idx]
        enrolled_ids = self.student_enrollments.get(student_id, set())

        # 1. Content similarity
        content_scores = cosine_similarity(student_vector, self.kuppi_vectors).flatten()

        # 2. Metadata boost
        metadata_boost = np.ones(len(self.kuppi_df)) * 0.3
        student = student_row.iloc[0]
        for i, row in self.kuppi_df.iterrows():
            score = 0.0
            if row["university_id"] == student["university_id"]:
                score += 0.6
            if row["department_id"] == student["department_id"]:
                score += 0.5
            if row["degree_id"] == student["degree_id"]:
                score += 0.4
            if row["academic_year"] == student["academic_year"]:
                score += 0.35
            metadata_boost[i] = score

        # 3. Quality & popularity boost
        quality_boost = np.array([
            (row["avg_rating"] / 5.0) * 0.4 + 
            min(row["enrollment_count"] / 50, 1.0) * 0.3
            for _, row in self.kuppi_df.iterrows()
        ])

        # 4. Recency penalty
        recency_penalty = np.array([
            max(0, 1 - (row["days_old"] / 365)) * 0.25
            for _, row in self.kuppi_df.iterrows()
        ])

        # Final combined score
        final_scores = (
            content_scores * 0.55 +
            metadata_boost * 0.25 +
            quality_boost * 0.15 +
            recency_penalty * 0.05
        )

        top_indices = final_scores.argsort()[::-1]

        results = []
        seen_subjects = set()

        for i in top_indices:
            kuppi_id = int(self.kuppi_df.iloc[i]["id"])
            if kuppi_id in enrolled_ids:
                continue

            subject = self.kuppi_df.iloc[i]["subject_name"]
            if subject in seen_subjects and len(results) > 3:
                continue
            seen_subjects.add(subject)

            item = self.kuppi_df.iloc[i].to_dict()
            item["similarity_score"] = float(final_scores[i])
            results.append(item)

            if len(results) >= top_n:
                break

        if len(results) < top_n:
            cold_results = self._get_cold_start_recommendations(student_id, top_n - len(results))
            results.extend(cold_results)

        return results[:top_n]

    def _get_cold_start_recommendations(self, student_id: int, top_n: int):
        # FIXED: Use Student.id instead of Student.user_id
        student = self.db.query(Student).filter(Student.id == student_id).first()
        if not student:
            popular = self.kuppi_df.sort_values("enrollment_count", ascending=False).head(top_n)
            return popular.to_dict(orient="records")

        same_uni = self.kuppi_df[self.kuppi_df["university_id"] == student.university_id]
        if len(same_uni) >= top_n:
            return same_uni.sort_values("enrollment_count", ascending=False).head(top_n).to_dict(orient="records")

        same_degree = self.kuppi_df[self.kuppi_df["degree_id"] == student.degree_id]
        candidates = pd.concat([same_uni, same_degree]).drop_duplicates()
        return candidates.sort_values("enrollment_count", ascending=False).head(top_n).to_dict(orient="records")

    def refresh_models(self):
        self.build_kuppi_vectors()
        self.build_student_vectors()