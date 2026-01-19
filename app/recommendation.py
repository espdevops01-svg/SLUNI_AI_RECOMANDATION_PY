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
# # from sklearn.metrics.pairwise import cosine_similarity
# # import pandas as pd
# # import numpy as np
# # from typing import List, Dict, Tuple
# # import re
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
# #                 'price': float(kuppi.price),
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
# #                 'price': float(kuppi.price),
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
# import numpy as np
# from typing import List, Dict, Tuple
# import re
# from .database import Kuppi, User, Student, Enrollment, Review, University, Department, Degree, Subject, Tutor

# class RecommendationEngine:
#     def __init__(self, db: Session):
#         self.db = db
#         self.tfidf_vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
#         self.kuppi_vectors = None
#         self.kuppi_df = None
#         self.student_vectors = None
#         self.student_df = None
        
#     def preprocess_text(self, text: str) -> str:
#         """Basic text preprocessing"""
#         if not text:
#             return ""
#         # Convert to lowercase
#         text = text.lower()
#         # Remove special characters and digits
#         text = re.sub(r'[^a-zA-Z\s]', '', text)
#         return text
    
#     def build_kuppi_vectors(self):
#         """Build TF-IDF vectors for all Kuppis"""
#         # Get all approved kuppis
#         kuppis = self.db.query(Kuppi).filter(Kuppi.status == 'APPROVED').all()
        
#         if not kuppis:
#             return
        
#         # Create a DataFrame with kuppi data
#         kuppi_data = []
#         for kuppi in kuppis:
#             # Get related information
#             university = self.db.query(University).filter(University.id == kuppi.university_id).first()
#             department = self.db.query(Department).filter(Department.id == kuppi.department_id).first()
#             degree = self.db.query(Degree).filter(Degree.id == kuppi.degree_id).first()
#             subject = self.db.query(Subject).filter(Subject.id == kuppi.subject_id).first()
#             tutor = self.db.query(User).filter(User.id == kuppi.tutor_id).first()
            
#             # Combine text fields for content similarity
#             combined_text = f"{kuppi.title} {kuppi.description} {subject.name if subject else ''} {subject.description if subject else ''}"
            
#             kuppi_data.append({
#                 'id': kuppi.id,
#                 'title': kuppi.title,
#                 'description': kuppi.description,
#                 'price': float(kuppi.price),
#                 'university_id': kuppi.university_id,
#                 'university_name': university.name if university else '',
#                 'department_id': kuppi.department_id,
#                 'department_name': department.name if department else '',
#                 'degree_id': kuppi.degree_id,
#                 'degree_name': degree.name if degree else '',
#                 'subject_id': kuppi.subject_id,
#                 'subject_name': subject.name if subject else '',
#                 'tutor_id': kuppi.tutor_id,
#                 'tutor_name': tutor.full_name if tutor else '',
#                 'combined_text': self.preprocess_text(combined_text)
#             })
        
#         self.kuppi_df = pd.DataFrame(kuppi_data)
        
#         # Create TF-IDF vectors
#         self.kuppi_vectors = self.tfidf_vectorizer.fit_transform(self.kuppi_df['combined_text'])
    
#     def build_student_vectors(self):
#         """Build interaction vectors for all students"""
#         # Get all students
#         students = self.db.query(Student).all()
        
#         if not students:
#             return
        
#         student_data = []
        
#         for student in students:
#             # Get student's enrollments
#             enrollments = self.db.query(Enrollment).filter(Enrollment.student_id == student.id).all()
#             enrolled_kuppi_ids = [e.kuppi_id for e in enrollments]
            
#             # Get student's reviews
#             reviews = self.db.query(Review).filter(Review.student_id == student.id).all()
#             reviewed_kuppi_ids = [r.kuppi_id for r in reviews]
            
#             # Get student's questions
#             questions = self.db.query(Question).filter(Question.student_id == student.id).all()
#             asked_kuppi_ids = [q.kuppi_id for q in questions]
            
#             # Combine all interactions
#             all_interacted_kuppi_ids = list(set(enrolled_kuppi_ids + reviewed_kuppi_ids + asked_kuppi_ids))
            
#             # Get the kuppis the student interacted with
#             interacted_kuppis = self.db.query(Kuppi).filter(Kuppi.id.in_(all_interacted_kuppi_ids)).all()
            
#             # Create a profile based on the content of interacted kuppis
#             profile_text = ""
#             for kuppi in interacted_kuppis:
#                 subject = self.db.query(Subject).filter(Subject.id == kuppi.subject_id).first()
#                 profile_text += f"{kuppi.title} {kuppi.description} {subject.name if subject else ''} "
            
#             student_data.append({
#                 'id': student.id,
#                 'university_id': student.university_id,
#                 'department_id': student.department_id,
#                 'degree_id': student.degree_id,
#                 'academic_year': student.academic_year,
#                 'enrolled_kuppi_ids': enrolled_kuppi_ids,
#                 'reviewed_kuppi_ids': reviewed_kuppi_ids,
#                 'asked_kuppi_ids': asked_kuppi_ids,
#                 'profile_text': self.preprocess_text(profile_text)
#             })
        
#         self.student_df = pd.DataFrame(student_data)
        
#         # Create TF-IDF vectors for student profiles
#         if not self.student_df['profile_text'].str.strip().empty:
#             self.student_vectors = self.tfidf_vectorizer.transform(self.student_df['profile_text'])
    
#     def get_recommendations(self, student_id: int, top_n: int = 5) -> List[Dict]:
#         """Get top-N recommendations for a student"""
#         # Build vectors if not already built
#         if self.kuppi_vectors is None:
#             self.build_kuppi_vectors()
        
#         if self.student_vectors is None:
#             self.build_student_vectors()
        
#         # Check if student exists
#         student_row = self.student_df[self.student_df['id'] == student_id]
#         if student_row.empty:
#             return []
        
#         student_idx = student_row.index[0]
#         student_vector = self.student_vectors[student_idx]
        
#         # Get student's enrolled kuppis to exclude them from recommendations
#         enrolled_kuppi_ids = student_row.iloc[0]['enrolled_kuppi_ids']
        
#         # Calculate cosine similarity between student and all kuppis
#         similarity_scores = cosine_similarity(student_vector, self.kuppi_vectors).flatten()
        
#         # Get indices of top similar kuppis
#         top_indices = similarity_scores.argsort()[-top_n*2:][::-1]  # Get more to filter out enrolled ones
        
#         # Filter out already enrolled kuppis and get top N
#         recommendations = []
#         for idx in top_indices:
#             kuppi_id = self.kuppi_df.iloc[idx]['id']
#             if kuppi_id not in enrolled_kuppi_ids:
#                 kuppi_data = self.kuppi_df.iloc[idx].to_dict()
#                 kuppi_data['similarity_score'] = float(similarity_scores[idx])
#                 recommendations.append(kuppi_data)
                
#                 if len(recommendations) >= top_n:
#                     break
        
#         return recommendations
    
#     def get_fallback_recommendations(self, student_id: int, top_n: int = 5) -> List[Dict]:
#         """Get fallback recommendations based on popular kuppis when student has no interaction history"""
#         # Get student's university, department, and degree
#         student = self.db.query(Student).filter(Student.id == student_id).first()
#         if not student:
#             return []
        
#         # Get popular kuppis from the same university/department/degree
#         kuppis = self.db.query(Kuppi).filter(
#             Kuppi.status == 'APPROVED',
#             Kuppi.university_id == student.university_id
#         ).limit(top_n * 2).all()
        
#         # If not enough kuppis from the same university, get from the same department
#         if len(kuppis) < top_n:
#             department_kuppis = self.db.query(Kuppi).filter(
#                 Kuppi.status == 'APPROVED',
#                 Kuppi.department_id == student.department_id,
#                 Kuppi.id.notin_([k.id for k in kuppis])
#             ).limit(top_n - len(kuppis)).all()
#             kuppis.extend(department_kuppis)
        
#         # If still not enough, get from the same degree
#         if len(kuppis) < top_n:
#             degree_kuppis = self.db.query(Kuppi).filter(
#                 Kuppi.status == 'APPROVED',
#                 Kuppi.degree_id == student.degree_id,
#                 Kuppi.id.notin_([k.id for k in kuppis])
#             ).limit(top_n - len(kuppis)).all()
#             kuppis.extend(degree_kuppis)
        
#         # If still not enough, get any approved kuppis
#         if len(kuppis) < top_n:
#             any_kuppis = self.db.query(Kuppi).filter(
#                 Kuppi.status == 'APPROVED',
#                 Kuppi.id.notin_([k.id for k in kuppis])
#             ).limit(top_n - len(kuppis)).all()
#             kuppis.extend(any_kuppis)
        
#         # Convert to recommendation format
#         recommendations = []
#         for kuppi in kuppis[:top_n]:
#             # Get related information
#             university = self.db.query(University).filter(University.id == kuppi.university_id).first()
#             department = self.db.query(Department).filter(Department.id == kuppi.department_id).first()
#             degree = self.db.query(Degree).filter(Degree.id == kuppi.degree_id).first()
#             subject = self.db.query(Subject).filter(Subject.id == kuppi.subject_id).first()
#             tutor = self.db.query(User).filter(User.id == kuppi.tutor_id).first()
            
#             recommendations.append({
#                 'id': kuppi.id,
#                 'title': kuppi.title,
#                 'description': kuppi.description,
#                 'price': float(kuppi.price),
#                 'university_id': kuppi.university_id,
#                 'university_name': university.name if university else '',
#                 'department_id': kuppi.department_id,
#                 'department_name': department.name if department else '',
#                 'degree_id': kuppi.degree_id,
#                 'degree_name': degree.name if degree else '',
#                 'subject_id': kuppi.subject_id,
#                 'subject_name': subject.name if subject else '',
#                 'tutor_id': kuppi.tutor_id,
#                 'tutor_name': tutor.full_name if tutor else '',
#                 'similarity_score': 0.5  # Default similarity score for fallback recommendations
#             })
        
#         return recommendations
    
#     def refresh_models(self):
#         """Refresh the recommendation models"""
#         self.build_kuppi_vectors()
#         self.build_student_vectors()

from sqlalchemy.orm import Session
from sklearn.feature_extraction.text import TfidfVectorizer
from .database import Kuppi, User, Student, Enrollment, Review, University, Department, Degree, Subject, Tutor, Question

from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np
from typing import List, Dict, Tuple
import re
from decimal import Decimal
from .database import Kuppi, User, Student, Enrollment, Review, University, Department, Degree, Subject, Tutor

class RecommendationEngine:
    def __init__(self, db: Session):
        self.db = db
        self.tfidf_vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
        self.kuppi_vectors = None
        self.kuppi_df = None
        self.student_vectors = None
        self.student_df = None
        
    def preprocess_text(self, text: str) -> str:
        """Basic text preprocessing"""
        if not text:
            return ""
        # Convert to lowercase
        text = text.lower()
        # Remove special characters and digits
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        return text
    
    def build_kuppi_vectors(self):
        """Build TF-IDF vectors for all Kuppis"""
        # Get all approved kuppis
        kuppis = self.db.query(Kuppi).filter(Kuppi.status == 'APPROVED').all()
        
        if not kuppis:
            return
        
        # Create a DataFrame with kuppi data
        kuppi_data = []
        for kuppi in kuppis:
            # Get related information
            university = self.db.query(University).filter(University.id == kuppi.university_id).first()
            department = self.db.query(Department).filter(Department.id == kuppi.department_id).first()
            degree = self.db.query(Degree).filter(Degree.id == kuppi.degree_id).first()
            subject = self.db.query(Subject).filter(Subject.id == kuppi.subject_id).first()
            tutor = self.db.query(User).filter(User.id == kuppi.tutor_id).first()
            
            # Combine text fields for content similarity
            combined_text = f"{kuppi.title} {kuppi.description} {subject.name if subject else ''} {subject.description if subject else ''}"
            
            kuppi_data.append({
                'id': kuppi.id,
                'title': kuppi.title,
                'description': kuppi.description,
                'price': float(kuppi.price) if kuppi.price else 0.0,  # Convert Decimal to float
                'university_id': kuppi.university_id,
                'university_name': university.name if university else '',
                'department_id': kuppi.department_id,
                'department_name': department.name if department else '',
                'degree_id': kuppi.degree_id,
                'degree_name': degree.name if degree else '',
                'subject_id': kuppi.subject_id,
                'subject_name': subject.name if subject else '',
                'tutor_id': kuppi.tutor_id,
                'tutor_name': tutor.full_name if tutor else '',
                'combined_text': self.preprocess_text(combined_text)
            })
        
        self.kuppi_df = pd.DataFrame(kuppi_data)
        
        # Create TF-IDF vectors
        self.kuppi_vectors = self.tfidf_vectorizer.fit_transform(self.kuppi_df['combined_text'])
    
    def build_student_vectors(self):
        """Build interaction vectors for all students"""
        # Get all students
        students = self.db.query(Student).all()
        
        if not students:
            return
        
        student_data = []
        
        for student in students:
            # Get student's enrollments
            enrollments = self.db.query(Enrollment).filter(Enrollment.student_id == student.id).all()
            enrolled_kuppi_ids = [e.kuppi_id for e in enrollments]
            
            # Get student's reviews
            reviews = self.db.query(Review).filter(Review.student_id == student.id).all()
            reviewed_kuppi_ids = [r.kuppi_id for r in reviews]
            
            # Get student's questions
            questions = self.db.query(Question).filter(Question.student_id == student.id).all()
            asked_kuppi_ids = [q.kuppi_id for q in questions]
            
            # Combine all interactions
            all_interacted_kuppi_ids = list(set(enrolled_kuppi_ids + reviewed_kuppi_ids + asked_kuppi_ids))
            
            # Get the kuppis the student interacted with
            interacted_kuppis = self.db.query(Kuppi).filter(Kuppi.id.in_(all_interacted_kuppi_ids)).all()
            
            # Create a profile based on the content of interacted kuppis
            profile_text = ""
            for kuppi in interacted_kuppis:
                subject = self.db.query(Subject).filter(Subject.id == kuppi.subject_id).first()
                profile_text += f"{kuppi.title} {kuppi.description} {subject.name if subject else ''} "
            
            student_data.append({
                'id': student.id,
                'university_id': student.university_id,
                'department_id': student.department_id,
                'degree_id': student.degree_id,
                'academic_year': student.academic_year,
                'enrolled_kuppi_ids': enrolled_kuppi_ids,
                'reviewed_kuppi_ids': reviewed_kuppi_ids,
                'asked_kuppi_ids': asked_kuppi_ids,
                'profile_text': self.preprocess_text(profile_text)
            })
        
        self.student_df = pd.DataFrame(student_data)
        
        # Create TF-IDF vectors for student profiles
        if not self.student_df['profile_text'].str.strip().empty:
            self.student_vectors = self.tfidf_vectorizer.transform(self.student_df['profile_text'])
    
    def get_recommendations(self, student_id: int, top_n: int = 5) -> List[Dict]:
        """Get top-N recommendations for a student"""
        # Build vectors if not already built
        if self.kuppi_vectors is None:
            self.build_kuppi_vectors()
        
        if self.student_vectors is None:
            self.build_student_vectors()
        
        # Check if student exists
        student_row = self.student_df[self.student_df['id'] == student_id]
        if student_row.empty:
            return []
        
        student_idx = student_row.index[0]
        student_vector = self.student_vectors[student_idx]
        
        # Get student's enrolled kuppis to exclude them from recommendations
        enrolled_kuppi_ids = student_row.iloc[0]['enrolled_kuppi_ids']
        
        # Calculate cosine similarity between student and all kuppis
        similarity_scores = cosine_similarity(student_vector, self.kuppi_vectors).flatten()
        
        # Get indices of top similar kuppis
        top_indices = similarity_scores.argsort()[-top_n*2:][::-1]  # Get more to filter out enrolled ones
        
        # Filter out already enrolled kuppis and get top N
        recommendations = []
        for idx in top_indices:
            kuppi_id = self.kuppi_df.iloc[idx]['id']
            if kuppi_id not in enrolled_kuppi_ids:
                kuppi_data = self.kuppi_df.iloc[idx].to_dict()
                kuppi_data['similarity_score'] = float(similarity_scores[idx])
                recommendations.append(kuppi_data)
                
                if len(recommendations) >= top_n:
                    break
        
        return recommendations
    
    def get_fallback_recommendations(self, student_id: int, top_n: int = 5) -> List[Dict]:
        """Get fallback recommendations based on popular kuppis when student has no interaction history"""
        # Get student's university, department, and degree
        student = self.db.query(Student).filter(Student.id == student_id).first()
        if not student:
            return []
        
        # Get popular kuppis from the same university/department/degree
        kuppis = self.db.query(Kuppi).filter(
            Kuppi.status == 'APPROVED',
            Kuppi.university_id == student.university_id
        ).limit(top_n * 2).all()
        
        # If not enough kuppis from the same university, get from the same department
        if len(kuppis) < top_n:
            department_kuppis = self.db.query(Kuppi).filter(
                Kuppi.status == 'APPROVED',
                Kuppi.department_id == student.department_id,
                Kuppi.id.notin_([k.id for k in kuppis])
            ).limit(top_n - len(kuppis)).all()
            kuppis.extend(department_kuppis)
        
        # If still not enough, get from the same degree
        if len(kuppis) < top_n:
            degree_kuppis = self.db.query(Kuppi).filter(
                Kuppi.status == 'APPROVED',
                Kuppi.degree_id == student.degree_id,
                Kuppi.id.notin_([k.id for k in kuppis])
            ).limit(top_n - len(kuppis)).all()
            kuppis.extend(degree_kuppis)
        
        # If still not enough, get any approved kuppis
        if len(kuppis) < top_n:
            any_kuppis = self.db.query(Kuppi).filter(
                Kuppi.status == 'APPROVED',
                Kuppi.id.notin_([k.id for k in kuppis])
            ).limit(top_n - len(kuppis)).all()
            kuppis.extend(any_kuppis)
        
        # Convert to recommendation format
        recommendations = []
        for kuppi in kuppis[:top_n]:
            # Get related information
            university = self.db.query(University).filter(University.id == kuppi.university_id).first()
            department = self.db.query(Department).filter(Department.id == kuppi.department_id).first()
            degree = self.db.query(Degree).filter(Degree.id == kuppi.degree_id).first()
            subject = self.db.query(Subject).filter(Subject.id == kuppi.subject_id).first()
            tutor = self.db.query(User).filter(User.id == kuppi.tutor_id).first()
            
            recommendations.append({
                'id': kuppi.id,
                'title': kuppi.title,
                'description': kuppi.description,
                'price': float(kuppi.price) if kuppi.price else 0.0,  # Convert Decimal to float
                'university_id': kuppi.university_id,
                'university_name': university.name if university else '',
                'department_id': kuppi.department_id,
                'department_name': department.name if department else '',
                'degree_id': kuppi.degree_id,
                'degree_name': degree.name if degree else '',
                'subject_id': kuppi.subject_id,
                'subject_name': subject.name if subject else '',
                'tutor_id': kuppi.tutor_id,
                'tutor_name': tutor.full_name if tutor else '',
                'similarity_score': 0.5  # Default similarity score for fallback recommendations
            })
        
        return recommendations
    
    def refresh_models(self):
        """Refresh the recommendation models"""
        self.build_kuppi_vectors()
        self.build_student_vectors()