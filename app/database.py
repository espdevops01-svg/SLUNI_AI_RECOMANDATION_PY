# # # # from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Text, DateTime, ForeignKey, Float
# # # # from sqlalchemy.ext.declarative import declarative_base
# # # # from sqlalchemy.orm import sessionmaker, relationship
# # # # from datetime import datetime
# # # # import os
# # # # from dotenv import load_dotenv

# # # # load_dotenv()

# # # # DATABASE_URL = os.getenv("DATABASE_URL")

# # # # engine = create_engine(DATABASE_URL)
# # # # SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# # # # Base = declarative_base()

# # # # def get_db():
# # # #     db = SessionLocal()
# # # #     try:
# # # #         yield db
# # # #     finally:
# # # #         db.close()

# # # # # Define database models based on your Spring Boot entities
# # # # class User(Base):
# # # #     __tablename__ = "users"
    
# # # #     id = Column(Integer, primary_key=True, index=True)
# # # #     email = Column(String(255), unique=True, index=True)
# # # #     full_name = Column(String(255))
# # # #     role = Column(String(50))
# # # #     active = Column(Integer, default=1)
# # # #     created_at = Column(DateTime, default=datetime.utcnow)
    
# # # #     # One-to-one relationships
# # # #     student = relationship("Student", back_populates="user", uselist=False)
# # # #     tutor = relationship("Tutor", back_populates="user", uselist=False)
    
# # # #     # One-to-many relationships
# # # #     enrollments = relationship("Enrollment", back_populates="student")
# # # #     reviews = relationship("Review", back_populates="student")
# # # #     questions = relationship("Question", back_populates="student")

# # # # class Student(Base):
# # # #     __tablename__ = "students"
    
# # # #     id = Column(Integer, ForeignKey("users.id"), primary_key=True)
# # # #     university_id = Column(Integer, ForeignKey("universities.id"))
# # # #     department_id = Column(Integer, ForeignKey("departments.id"))
# # # #     degree_id = Column(Integer, ForeignKey("degrees.id"))
# # # #     academic_year = Column(Integer)
    
# # # #     user = relationship("User", back_populates="student")
# # # #     university = relationship("University", back_populates="students")
# # # #     department = relationship("Department", back_populates="students")
# # # #     degree = relationship("Degree", back_populates="students")

# # # # class Tutor(Base):
# # # #     __tablename__ = "tutors"
    
# # # #     id = Column(Integer, ForeignKey("users.id"), primary_key=True)
# # # #     university_id = Column(Integer, ForeignKey("universities.id"))
# # # #     department_id = Column(Integer, ForeignKey("departments.id"))
# # # #     degree_id = Column(Integer, ForeignKey("degrees.id"))
# # # #     academic_year = Column(Integer)
# # # #     qualifications = Column(Text)
# # # #     expertise_subjects = Column(Text)
# # # #     is_verified = Column(Integer, default=0)
# # # #     wallet_balance = Column(Float, default=0.0)
    
# # # #     user = relationship("User", back_populates="tutor")
# # # #     university = relationship("University", back_populates="tutors")
# # # #     department = relationship("Department", back_populates="tutors")
# # # #     degree = relationship("Degree", back_populates="tutors")
# # # #     kuppis = relationship("Kuppi", back_populates="tutor")

# # # # class University(Base):
# # # #     __tablename__ = "universities"
    
# # # #     id = Column(Integer, primary_key=True, index=True)
# # # #     name = Column(String(255))
# # # #     description = Column(Text)
# # # #     location = Column(String(255))
    
# # # #     students = relationship("Student", back_populates="university")
# # # #     tutors = relationship("Tutor", back_populates="university")
# # # #     departments = relationship("Department", back_populates="university")
# # # #     kuppis = relationship("Kuppi", back_populates="university")

# # # # class Department(Base):
# # # #     __tablename__ = "departments"
    
# # # #     id = Column(Integer, primary_key=True, index=True)
# # # #     name = Column(String(255))
# # # #     description = Column(Text)
# # # #     university_id = Column(Integer, ForeignKey("universities.id"))
    
# # # #     university = relationship("University", back_populates="departments")
# # # #     students = relationship("Student", back_populates="department")
# # # #     tutors = relationship("Tutor", back_populates="department")
# # # #     degrees = relationship("Degree", back_populates="department")
# # # #     kuppis = relationship("Kuppi", back_populates="department")

# # # # class Degree(Base):
# # # #     __tablename__ = "degrees"
    
# # # #     id = Column(Integer, primary_key=True, index=True)
# # # #     name = Column(String(255))
# # # #     description = Column(Text)
# # # #     duration = Column(Integer)
# # # #     department_id = Column(Integer, ForeignKey("departments.id"))
    
# # # #     department = relationship("Department", back_populates="degrees")
# # # #     students = relationship("Student", back_populates="degree")
# # # #     tutors = relationship("Tutor", back_populates="degree")
# # # #     kuppis = relationship("Kuppi", back_populates="degree")

# # # # class Subject(Base):
# # # #     __tablename__ = "subjects"
    
# # # #     id = Column(Integer, primary_key=True, index=True)
# # # #     name = Column(String(255))
# # # #     subject_code = Column(String(50))
# # # #     description = Column(Text)
# # # #     academic_year = Column(Integer)
# # # #     degree_id = Column(Integer, ForeignKey("degrees.id"))
# # # #     department_id = Column(Integer, ForeignKey("departments.id"))
    
# # # #     degree = relationship("Degree")
# # # #     department = relationship("Department")
# # # #     kuppis = relationship("Kuppi", back_populates="subject")

# # # # class Kuppi(Base):
# # # #     __tablename__ = "kuppis"
    
# # # #     id = Column(Integer, primary_key=True, index=True)
# # # #     title = Column(String(255))
# # # #     description = Column(Text)
# # # #     price = Column(Float)
# # # #     academic_year = Column(Integer)
# # # #     status = Column(String(50))  # PENDING, APPROVED, REJECTED
    
# # # #     tutor_id = Column(Integer, ForeignKey("tutors.id"))
# # # #     university_id = Column(Integer, ForeignKey("universities.id"))
# # # #     department_id = Column(Integer, ForeignKey("departments.id"))
# # # #     degree_id = Column(Integer, ForeignKey("degrees.id"))
# # # #     subject_id = Column(Integer, ForeignKey("subjects.id"))
    
# # # #     tutor = relationship("Tutor", back_populates="kuppis")
# # # #     university = relationship("University", back_populates="kuppis")
# # # #     department = relationship("Department", back_populates="kuppis")
# # # #     degree = relationship("Degree", back_populates="kuppis")
# # # #     subject = relationship("Subject", back_populates="kuppis")
    
# # # #     enrollments = relationship("Enrollment", back_populates="kuppi")
# # # #     reviews = relationship("Review", back_populates="kuppi")
# # # #     questions = relationship("Question", back_populates="kuppi")
# # # #     contents = relationship("KuppiContent", back_populates="kuppi")

# # # # class KuppiContent(Base):
# # # #     __tablename__ = "kuppi_contents"
    
# # # #     id = Column(Integer, primary_key=True, index=True)
# # # #     title = Column(String(255))
# # # #     type = Column(String(50))  # VIDEO, DOCUMENT, TEXT, LINK
# # # #     text_description = Column(Text)
# # # #     url = Column(String(500))
# # # #     kuppi_id = Column(Integer, ForeignKey("kuppis.id"))
    
# # # #     kuppi = relationship("Kuppi", back_populates="contents")

# # # # class Enrollment(Base):
# # # #     __tablename__ = "enrollments"
    
# # # #     id = Column(Integer, primary_key=True, index=True)
# # # #     enrollment_date = Column(DateTime, default=datetime.utcnow)
# # # #     expiry_date = Column(DateTime)
# # # #     payment_amount = Column(Float)
# # # #     payment_id = Column(String(255))
    
# # # #     student_id = Column(Integer, ForeignKey("users.id"))
# # # #     kuppi_id = Column(Integer, ForeignKey("kuppis.id"))
    
# # # #     student = relationship("User", back_populates="enrollments")
# # # #     kuppi = relationship("Kuppi", back_populates="enrollments")

# # # # class Review(Base):
# # # #     __tablename__ = "reviews"
    
# # # #     id = Column(Integer, primary_key=True, index=True)
# # # #     rating = Column(Integer)
# # # #     comment = Column(Text)
    
# # # #     student_id = Column(Integer, ForeignKey("users.id"))
# # # #     kuppi_id = Column(Integer, ForeignKey("kuppis.id"))
    
# # # #     student = relationship("User", back_populates="reviews")
# # # #     kuppi = relationship("Kuppi", back_populates="reviews")

# # # # class Question(Base):
# # # #     __tablename__ = "questions"
    
# # # #     id = Column(Integer, primary_key=True, index=True)
# # # #     question = Column(Text)
# # # #     answer = Column(Text)
# # # #     answered_at = Column(DateTime)
    
# # # #     student_id = Column(Integer, ForeignKey("users.id"))
# # # #     kuppi_id = Column(Integer, ForeignKey("kuppis.id"))
# # # #     answered_by = Column(Integer, ForeignKey("users.id"))
    
# # # #     student = relationship("User", foreign_keys=[student_id], back_populates="questions")
# # # #     kuppi = relationship("Kuppi", back_populates="questions")
# # # #     answerer = relationship("User", foreign_keys=[answered_by])

# # # from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Text, DateTime, ForeignKey, Float
# # # from sqlalchemy.ext.declarative import declarative_base
# # # from sqlalchemy.orm import sessionmaker, relationship
# # # from datetime import datetime
# # # import os
# # # from dotenv import load_dotenv

# # # load_dotenv()

# # # DATABASE_URL = os.getenv("DATABASE_URL")

# # # engine = create_engine(DATABASE_URL)
# # # SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# # # Base = declarative_base()

# # # def get_db():
# # #     db = SessionLocal()
# # #     try:
# # #         yield db
# # #     finally:
# # #         db.close()

# # # # Define database models based on your Spring Boot entities
# # # class User(Base):
# # #     __tablename__ = "users"
    
# # #     id = Column(Integer, primary_key=True, index=True)
# # #     email = Column(String(255), unique=True, index=True)
# # #     full_name = Column(String(255))
# # #     role = Column(String(50))
# # #     active = Column(Integer, default=1)
# # #     created_at = Column(DateTime, default=datetime.utcnow)
    
# # #     # One-to-one relationships
# # #     student = relationship("Student", back_populates="user", uselist=False)
# # #     tutor = relationship("Tutor", back_populates="user", uselist=False)
    
# # #     # One-to-many relationships
# # #     enrollments = relationship("Enrollment", back_populates="student")
# # #     reviews = relationship("Review", back_populates="student")
# # #     # We'll define the questions relationship in the Question model to avoid ambiguity

# # # class Student(Base):
# # #     __tablename__ = "students"
    
# # #     id = Column(Integer, ForeignKey("users.id"), primary_key=True)
# # #     university_id = Column(Integer, ForeignKey("universities.id"))
# # #     department_id = Column(Integer, ForeignKey("departments.id"))
# # #     degree_id = Column(Integer, ForeignKey("degrees.id"))
# # #     academic_year = Column(Integer)
    
# # #     user = relationship("User", back_populates="student")
# # #     university = relationship("University", back_populates="students")
# # #     department = relationship("Department", back_populates="students")
# # #     degree = relationship("Degree", back_populates="students")

# # # class Tutor(Base):
# # #     __tablename__ = "tutors"
    
# # #     id = Column(Integer, ForeignKey("users.id"), primary_key=True)
# # #     university_id = Column(Integer, ForeignKey("universities.id"))
# # #     department_id = Column(Integer, ForeignKey("departments.id"))
# # #     degree_id = Column(Integer, ForeignKey("degrees.id"))
# # #     academic_year = Column(Integer)
# # #     qualifications = Column(Text)
# # #     expertise_subjects = Column(Text)
# # #     is_verified = Column(Integer, default=0)
# # #     wallet_balance = Column(Float, default=0.0)
    
# # #     user = relationship("User", back_populates="tutor")
# # #     university = relationship("University", back_populates="tutors")
# # #     department = relationship("Department", back_populates="tutors")
# # #     degree = relationship("Degree", back_populates="tutors")
# # #     kuppis = relationship("Kuppi", back_populates="tutor")

# # # class University(Base):
# # #     __tablename__ = "universities"
    
# # #     id = Column(Integer, primary_key=True, index=True)
# # #     name = Column(String(255))
# # #     description = Column(Text)
# # #     location = Column(String(255))
    
# # #     students = relationship("Student", back_populates="university")
# # #     tutors = relationship("Tutor", back_populates="university")
# # #     departments = relationship("Department", back_populates="university")
# # #     kuppis = relationship("Kuppi", back_populates="university")

# # # class Department(Base):
# # #     __tablename__ = "departments"
    
# # #     id = Column(Integer, primary_key=True, index=True)
# # #     name = Column(String(255))
# # #     description = Column(Text)
# # #     university_id = Column(Integer, ForeignKey("universities.id"))
    
# # #     university = relationship("University", back_populates="departments")
# # #     students = relationship("Student", back_populates="department")
# # #     tutors = relationship("Tutor", back_populates="department")
# # #     degrees = relationship("Degree", back_populates="department")
# # #     kuppis = relationship("Kuppi", back_populates="department")

# # # class Degree(Base):
# # #     __tablename__ = "degrees"
    
# # #     id = Column(Integer, primary_key=True, index=True)
# # #     name = Column(String(255))
# # #     description = Column(Text)
# # #     duration = Column(Integer)
# # #     department_id = Column(Integer, ForeignKey("departments.id"))
    
# # #     department = relationship("Department", back_populates="degrees")
# # #     students = relationship("Student", back_populates="degree")
# # #     tutors = relationship("Tutor", back_populates="degree")
# # #     kuppis = relationship("Kuppi", back_populates="degree")

# # # class Subject(Base):
# # #     __tablename__ = "subjects"
    
# # #     id = Column(Integer, primary_key=True, index=True)
# # #     name = Column(String(255))
# # #     subject_code = Column(String(50))
# # #     description = Column(Text)
# # #     academic_year = Column(Integer)
# # #     degree_id = Column(Integer, ForeignKey("degrees.id"))
# # #     department_id = Column(Integer, ForeignKey("departments.id"))
    
# # #     degree = relationship("Degree")
# # #     department = relationship("Department")
# # #     kuppis = relationship("Kuppi", back_populates="subject")

# # # class Kuppi(Base):
# # #     __tablename__ = "kuppis"
    
# # #     id = Column(Integer, primary_key=True, index=True)
# # #     title = Column(String(255))
# # #     description = Column(Text)
# # #     price = Column(Float)
# # #     academic_year = Column(Integer)
# # #     status = Column(String(50))  # PENDING, APPROVED, REJECTED
    
# # #     tutor_id = Column(Integer, ForeignKey("tutors.id"))
# # #     university_id = Column(Integer, ForeignKey("universities.id"))
# # #     department_id = Column(Integer, ForeignKey("departments.id"))
# # #     degree_id = Column(Integer, ForeignKey("degrees.id"))
# # #     subject_id = Column(Integer, ForeignKey("subjects.id"))
    
# # #     tutor = relationship("Tutor", back_populates="kuppis")
# # #     university = relationship("University", back_populates="kuppis")
# # #     department = relationship("Department", back_populates="kuppis")
# # #     degree = relationship("Degree", back_populates="kuppis")
# # #     subject = relationship("Subject", back_populates="subject")
    
# # #     enrollments = relationship("Enrollment", back_populates="kuppi")
# # #     reviews = relationship("Review", back_populates="kuppi")
# # #     questions = relationship("Question", back_populates="kuppi")
# # #     contents = relationship("KuppiContent", back_populates="kuppi")

# # # class KuppiContent(Base):
# # #     __tablename__ = "kuppi_contents"
    
# # #     id = Column(Integer, primary_key=True, index=True)
# # #     title = Column(String(255))
# # #     type = Column(String(50))  # VIDEO, DOCUMENT, TEXT, LINK
# # #     text_description = Column(Text)
# # #     url = Column(String(500))
# # #     kuppi_id = Column(Integer, ForeignKey("kuppis.id"))
    
# # #     kuppi = relationship("Kuppi", back_populates="contents")

# # # class Enrollment(Base):
# # #     __tablename__ = "enrollments"
    
# # #     id = Column(Integer, primary_key=True, index=True)
# # #     enrollment_date = Column(DateTime, default=datetime.utcnow)
# # #     expiry_date = Column(DateTime)
# # #     payment_amount = Column(Float)
# # #     payment_id = Column(String(255))
    
# # #     student_id = Column(Integer, ForeignKey("users.id"))
# # #     kuppi_id = Column(Integer, ForeignKey("kuppis.id"))
    
# # #     student = relationship("User", back_populates="enrollments")
# # #     kuppi = relationship("Kuppi", back_populates="enrollments")

# # # class Review(Base):
# # #     __tablename__ = "reviews"
    
# # #     id = Column(Integer, primary_key=True, index=True)
# # #     rating = Column(Integer)
# # #     comment = Column(Text)
    
# # #     student_id = Column(Integer, ForeignKey("users.id"))
# # #     kuppi_id = Column(Integer, ForeignKey("kuppis.id"))
    
# # #     student = relationship("User", back_populates="reviews")
# # #     kuppi = relationship("Kuppi", back_populates="reviews")

# # # class Question(Base):
# # #     __tablename__ = "questions"
    
# # #     id = Column(Integer, primary_key=True, index=True)
# # #     question = Column(Text)
# # #     answer = Column(Text)
# # #     answered_at = Column(DateTime)
    
# # #     student_id = Column(Integer, ForeignKey("users.id"))
# # #     kuppi_id = Column(Integer, ForeignKey("kuppis.id"))
# # #     answered_by = Column(Integer, ForeignKey("users.id"))
    
# # #     # Define relationships with explicit foreign_keys to avoid ambiguity
# # #     student = relationship("User", foreign_keys=[student_id], backref="student_questions")
# # #     answerer = relationship("User", foreign_keys=[answered_by], backref="answered_questions")
# # #     kuppi = relationship("Kuppi", back_populates="questions")

# # from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Text, DateTime, ForeignKey, Float
# # from sqlalchemy.ext.declarative import declarative_base
# # from sqlalchemy.orm import sessionmaker, relationship
# # from datetime import datetime
# # import os
# # from dotenv import load_dotenv

# # load_dotenv()

# # DATABASE_URL = os.getenv("DATABASE_URL")

# # engine = create_engine(DATABASE_URL)
# # SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# # Base = declarative_base()

# # def get_db():
# #     db = SessionLocal()
# #     try:
# #         yield db
# #     finally:
# #         db.close()

# # # Define database models based on your Spring Boot entities
# # class User(Base):
# #     __tablename__ = "users"
    
# #     id = Column(Integer, primary_key=True, index=True)
# #     email = Column(String(255), unique=True, index=True)
# #     full_name = Column(String(255))
# #     role = Column(String(50))
# #     active = Column(Integer, default=1)
# #     created_at = Column(DateTime, default=datetime.utcnow)
    
# #     # One-to-one relationships
# #     student = relationship("Student", back_populates="user", uselist=False)
# #     tutor = relationship("Tutor", back_populates="user", uselist=False)
    
# #     # One-to-many relationships
# #     enrollments = relationship("Enrollment", back_populates="student")
# #     reviews = relationship("Review", back_populates="student")
# #     # We'll define the questions relationship in the Question model to avoid ambiguity

# # class Student(Base):
# #     __tablename__ = "students"
    
# #     id = Column(Integer, ForeignKey("users.id"), primary_key=True)
# #     university_id = Column(Integer, ForeignKey("universities.id"))
# #     department_id = Column(Integer, ForeignKey("departments.id"))
# #     degree_id = Column(Integer, ForeignKey("degrees.id"))
# #     academic_year = Column(Integer)
    
# #     user = relationship("User", back_populates="student")
# #     university = relationship("University", back_populates="students")
# #     department = relationship("Department", back_populates="students")
# #     degree = relationship("Degree", back_populates="students")

# # class Tutor(Base):
# #     __tablename__ = "tutors"
    
# #     id = Column(Integer, ForeignKey("users.id"), primary_key=True)
# #     university_id = Column(Integer, ForeignKey("universities.id"))
# #     department_id = Column(Integer, ForeignKey("departments.id"))
# #     degree_id = Column(Integer, ForeignKey("degrees.id"))
# #     academic_year = Column(Integer)
# #     qualifications = Column(Text)
# #     expertise_subjects = Column(Text)
# #     is_verified = Column(Integer, default=0)
# #     wallet_balance = Column(Float, default=0.0)
    
# #     user = relationship("User", back_populates="tutor")
# #     university = relationship("University", back_populates="tutors")
# #     department = relationship("Department", back_populates="tutors")
# #     degree = relationship("Degree", back_populates="tutors")
# #     kuppis = relationship("Kuppi", back_populates="tutor")

# # class University(Base):
# #     __tablename__ = "universities"
    
# #     id = Column(Integer, primary_key=True, index=True)
# #     name = Column(String(255))
# #     description = Column(Text)
# #     location = Column(String(255))
    
# #     students = relationship("Student", back_populates="university")
# #     tutors = relationship("Tutor", back_populates="university")
# #     departments = relationship("Department", back_populates="university")
# #     kuppis = relationship("Kuppi", back_populates="university")

# # class Department(Base):
# #     __tablename__ = "departments"
    
# #     id = Column(Integer, primary_key=True, index=True)
# #     name = Column(String(255))
# #     description = Column(Text)
# #     university_id = Column(Integer, ForeignKey("universities.id"))
    
# #     university = relationship("University", back_populates="departments")
# #     students = relationship("Student", back_populates="department")
# #     tutors = relationship("Tutor", back_populates="department")
# #     degrees = relationship("Degree", back_populates="department")
# #     kuppis = relationship("Kuppi", back_populates="department")

# # class Degree(Base):
# #     __tablename__ = "degrees"
    
# #     id = Column(Integer, primary_key=True, index=True)
# #     name = Column(String(255))
# #     description = Column(Text)
# #     duration = Column(Integer)
# #     department_id = Column(Integer, ForeignKey("departments.id"))
    
# #     department = relationship("Department", back_populates="degrees")
# #     students = relationship("Student", back_populates="degree")
# #     tutors = relationship("Tutor", back_populates="degree")
# #     kuppis = relationship("Kuppi", back_populates="degree")

# # class Subject(Base):
# #     __tablename__ = "subjects"
    
# #     id = Column(Integer, primary_key=True, index=True)
# #     name = Column(String(255))
# #     subject_code = Column(String(50))
# #     description = Column(Text)
# #     academic_year = Column(Integer)
# #     degree_id = Column(Integer, ForeignKey("degrees.id"))
# #     department_id = Column(Integer, ForeignKey("departments.id"))
    
# #     degree = relationship("Degree")
# #     department = relationship("Department")
# #     kuppis = relationship("Kuppi", back_populates="subject")

# # class Kuppi(Base):
# #     __tablename__ = "kuppis"
    
# #     id = Column(Integer, primary_key=True, index=True)
# #     title = Column(String(255))
# #     description = Column(Text)
# #     price = Column(Float)
# #     academic_year = Column(Integer)
# #     status = Column(String(50))  # PENDING, APPROVED, REJECTED
    
# #     tutor_id = Column(Integer, ForeignKey("tutors.id"))
# #     university_id = Column(Integer, ForeignKey("universities.id"))
# #     department_id = Column(Integer, ForeignKey("departments.id"))
# #     degree_id = Column(Integer, ForeignKey("degrees.id"))
# #     subject_id = Column(Integer, ForeignKey("subjects.id"))
    
# #     tutor = relationship("Tutor", back_populates="kuppis")
# #     university = relationship("University", back_populates="kuppis")
# #     department = relationship("Department", back_populates="kuppis")
# #     degree = relationship("Degree", back_populates="kuppis")
# #     subject = relationship("Subject", back_populates="kuppis")
    
# #     enrollments = relationship("Enrollment", back_populates="kuppi")
# #     reviews = relationship("Review", back_populates="kuppi")
# #     questions = relationship("Question", back_populates="kuppi")
# #     contents = relationship("KuppiContent", back_populates="kuppi")

# # class KuppiContent(Base):
# #     __tablename__ = "kuppi_contents"
    
# #     id = Column(Integer, primary_key=True, index=True)
# #     title = Column(String(255))
# #     type = Column(String(50))  # VIDEO, DOCUMENT, TEXT, LINK
# #     text_description = Column(Text)
# #     url = Column(String(500))
# #     kuppi_id = Column(Integer, ForeignKey("kuppis.id"))
    
# #     kuppi = relationship("Kuppi", back_populates="contents")

# # class Enrollment(Base):
# #     __tablename__ = "enrollments"
    
# #     id = Column(Integer, primary_key=True, index=True)
# #     enrollment_date = Column(DateTime, default=datetime.utcnow)
# #     expiry_date = Column(DateTime)
# #     payment_amount = Column(Float)
# #     payment_id = Column(String(255))
    
# #     student_id = Column(Integer, ForeignKey("users.id"))
# #     kuppi_id = Column(Integer, ForeignKey("kuppis.id"))
    
# #     student = relationship("User", back_populates="enrollments")
# #     kuppi = relationship("Kuppi", back_populates="enrollments")

# # class Review(Base):
# #     __tablename__ = "reviews"
    
# #     id = Column(Integer, primary_key=True, index=True)
# #     rating = Column(Integer)
# #     comment = Column(Text)
    
# #     student_id = Column(Integer, ForeignKey("users.id"))
# #     kuppi_id = Column(Integer, ForeignKey("kuppis.id"))
    
# #     student = relationship("User", back_populates="reviews")
# #     kuppi = relationship("Kuppi", back_populates="reviews")

# # class Question(Base):
# #     __tablename__ = "questions"
    
# #     id = Column(Integer, primary_key=True, index=True)
# #     question = Column(Text)
# #     answer = Column(Text)
# #     answered_at = Column(DateTime)
    
# #     student_id = Column(Integer, ForeignKey("users.id"))
# #     kuppi_id = Column(Integer, ForeignKey("kuppis.id"))
# #     answered_by = Column(Integer, ForeignKey("users.id"))
    
# #     # Define relationships with explicit foreign_keys to avoid ambiguity
# #     student = relationship("User", foreign_keys=[student_id], backref="student_questions")
# #     answerer = relationship("User", foreign_keys=[answered_by], backref="answered_questions")
# #     kuppi = relationship("Kuppi", back_populates="questions")

# from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Text, DateTime, ForeignKey, Float, Boolean
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker, relationship
# from datetime import datetime
# import os
# from dotenv import load_dotenv

# load_dotenv()

# DATABASE_URL = os.getenv("DATABASE_URL")

# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# # Define database models based on your Spring Boot entities
# class User(Base):
#     __tablename__ = "users"
    
#     id = Column(Integer, primary_key=True, index=True)
#     email = Column(String(255), unique=True, index=True, nullable=False)
#     password = Column(String(255), nullable=False)
#     full_name = Column(String(255), nullable=False)
#     role = Column(String(50), nullable=False)
#     is_active = Column(Boolean, default=True)
#     created_at = Column(DateTime, default=datetime.utcnow)
#     updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
#     # One-to-one relationships
#     student = relationship("Student", back_populates="user", uselist=False)
#     tutor = relationship("Tutor", back_populates="user", uselist=False)
#     admin = relationship("Admin", back_populates="user", uselist=False)
    
#     # One-to-many relationships
#     enrollments = relationship("Enrollment", back_populates="student")
#     reviews = relationship("Review", back_populates="student")
#     # We'll define the questions relationship in the Question model to avoid ambiguity

# class Student(Base):
#     __tablename__ = "students"
    
#     id = Column(Integer, ForeignKey("users.id"), primary_key=True)
#     university_id = Column(Integer, ForeignKey("universities.id"))
#     department_id = Column(Integer, ForeignKey("departments.id"))
#     degree_id = Column(Integer, ForeignKey("degrees.id"))
#     academic_year = Column(Integer)
    
#     user = relationship("User", back_populates="student")
#     university = relationship("University", back_populates="students")
#     department = relationship("Department", back_populates="students")
#     degree = relationship("Degree", back_populates="students")

# class Tutor(Base):
#     __tablename__ = "tutors"
    
#     id = Column(Integer, ForeignKey("users.id"), primary_key=True)
#     university_id = Column(Integer, ForeignKey("universities.id"))
#     department_id = Column(Integer, ForeignKey("departments.id"))
#     degree_id = Column(Integer, ForeignKey("degrees.id"))
#     academic_year = Column(Integer)
#     qualifications = Column(Text)
#     expertise_subjects = Column(String(255))
#     is_verified = Column(Boolean, default=False)
#     wallet_balance = Column(Float(precision=12, scale=2), default=0.0)
    
#     user = relationship("User", back_populates="tutor")
#     university = relationship("University", back_populates="tutors")
#     department = relationship("Department", back_populates="tutors")
#     degree = relationship("Degree", back_populates="tutors")
#     kuppis = relationship("Kuppi", back_populates="tutor")

# class Admin(Base):
#     __tablename__ = "admins"
    
#     id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    
#     user = relationship("User", back_populates="admin")

# class University(Base):
#     __tablename__ = "universities"
    
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String(255))
#     description = Column(Text)
#     location = Column(String(255))
    
#     students = relationship("Student", back_populates="university")
#     tutors = relationship("Tutor", back_populates="university")
#     departments = relationship("Department", back_populates="university")
#     kuppis = relationship("Kuppi", back_populates="university")

# class Department(Base):
#     __tablename__ = "departments"
    
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String(255))
#     description = Column(Text)
#     university_id = Column(Integer, ForeignKey("universities.id"))
    
#     university = relationship("University", back_populates="departments")
#     students = relationship("Student", back_populates="department")
#     tutors = relationship("Tutor", back_populates="department")
#     degrees = relationship("Degree", back_populates="department")
#     kuppis = relationship("Kuppi", back_populates="department")

# class Degree(Base):
#     __tablename__ = "degrees"
    
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String(255))
#     description = Column(Text)
#     duration = Column(Integer)
#     department_id = Column(Integer, ForeignKey("departments.id"))
    
#     department = relationship("Department", back_populates="degrees")
#     students = relationship("Student", back_populates="degree")
#     tutors = relationship("Tutor", back_populates="degree")
#     kuppis = relationship("Kuppi", back_populates="degree")
#     subjects = relationship("Subject", back_populates="degree")

# class Subject(Base):
#     __tablename__ = "subjects"
    
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String(255))
#     subject_code = Column(String(50))
#     description = Column(Text)
#     academic_year = Column(Integer)
#     degree_id = Column(Integer, ForeignKey("degrees.id"))
#     department_id = Column(Integer, ForeignKey("departments.id"))
    
#     degree = relationship("Degree", back_populates="subjects")
#     department = relationship("Department")
#     kuppis = relationship("Kuppi", back_populates="subject")

# class Kuppi(Base):
#     __tablename__ = "kuppis"
    
#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String(255))
#     description = Column(Text)
#     price = Column(Float(precision=10, scale=2))
#     academic_year = Column(Integer)
#     status = Column(String(50))  # PENDING, APPROVED, REJECTED
#     created_at = Column(DateTime, default=datetime.utcnow)
#     updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
#     tutor_id = Column(Integer, ForeignKey("tutors.id"))
#     university_id = Column(Integer, ForeignKey("universities.id"))
#     department_id = Column(Integer, ForeignKey("departments.id"))
#     degree_id = Column(Integer, ForeignKey("degrees.id"))
#     subject_id = Column(Integer, ForeignKey("subjects.id"))
    
#     tutor = relationship("Tutor", back_populates="kuppis")
#     university = relationship("University", back_populates="kuppis")
#     department = relationship("Department", back_populates="kuppis")
#     degree = relationship("Degree", back_populates="kuppis")
#     subject = relationship("Subject", back_populates="subject")
    
#     enrollments = relationship("Enrollment", back_populates="kuppi")
#     reviews = relationship("Review", back_populates="kuppi")
#     questions = relationship("Question", back_populates="kuppi")
#     contents = relationship("KuppiContent", back_populates="kuppi")

# class KuppiContent(Base):
#     __tablename__ = "kuppi_contents"
    
#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String(255))
#     type = Column(String(50))  # VIDEO, DOCUMENT
#     text_description = Column(Text)
#     url = Column(String(500))
#     created_at = Column(DateTime, default=datetime.utcnow)
#     kuppi_id = Column(Integer, ForeignKey("kuppis.id"))
    
#     kuppi = relationship("Kuppi", back_populates="contents")

# class Enrollment(Base):
#     __tablename__ = "enrollments"
    
#     id = Column(Integer, primary_key=True, index=True)
#     enrollment_date = Column(DateTime, default=datetime.utcnow)
#     expiry_date = Column(DateTime)
#     payment_amount = Column(Float(precision=10, scale=2))
#     payment_id = Column(String(255))
#     created_at = Column(DateTime, default=datetime.utcnow)
    
#     student_id = Column(Integer, ForeignKey("users.id"))
#     kuppi_id = Column(Integer, ForeignKey("kuppis.id"))
    
#     student = relationship("User", back_populates="enrollments")
#     kuppi = relationship("Kuppi", back_populates="enrollments")

# class Review(Base):
#     __tablename__ = "reviews"
    
#     id = Column(Integer, primary_key=True, index=True)
#     rating = Column(Integer)
#     comment = Column(Text)
#     created_at = Column(DateTime, default=datetime.utcnow)
#     updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
#     student_id = Column(Integer, ForeignKey("users.id"))
#     kuppi_id = Column(Integer, ForeignKey("kuppis.id"))
    
#     student = relationship("User", back_populates="reviews")
#     kuppi = relationship("Kuppi", back_populates="reviews")

# class Question(Base):
#     __tablename__ = "questions"
    
#     id = Column(Integer, primary_key=True, index=True)
#     question = Column(Text)
#     answer = Column(Text)
#     answered_at = Column(DateTime)
#     created_at = Column(DateTime, default=datetime.utcnow)
#     updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
#     student_id = Column(Integer, ForeignKey("users.id"))
#     kuppi_id = Column(Integer, ForeignKey("kuppis.id"))
#     answered_by = Column(Integer, ForeignKey("users.id"))
    
#     # Define relationships with explicit foreign_keys to avoid ambiguity
#     student = relationship("User", foreign_keys=[student_id], backref="student_questions")
#     answerer = relationship("User", foreign_keys=[answered_by], backref="answered_questions")
#     kuppi = relationship("Kuppi", back_populates="questions")

# class WithdrawalRequest(Base):
#     __tablename__ = "withdrawal_requests"
    
#     id = Column(Integer, primary_key=True, index=True)
#     amount = Column(Float(precision=12, scale=2))
#     bank_details = Column(Text)
#     status = Column(String(50))  # PENDING, APPROVED, REJECTED
#     rejection_reason = Column(Text)
#     processed_at = Column(DateTime)
#     created_at = Column(DateTime, default=datetime.utcnow)
#     updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
#     tutor_id = Column(Integer, ForeignKey("users.id"))
#     processed_by = Column(Integer, ForeignKey("users.id"))
    
#     tutor = relationship("User", foreign_keys=[tutor_id])
#     processed_by_user = relationship("User", foreign_keys=[processed_by])

# class AcademicYear(Base):
#     __tablename__ = "academic_years"
    
#     id = Column(Integer, primary_key=True, index=True)
#     year = Column(Integer)
    
#     degree_id = Column(Integer, ForeignKey("degrees.id"))
    
#     degree = relationship("Degree")

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Text, DateTime, ForeignKey, Float, Boolean, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Define database models based on your Spring Boot entities
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # One-to-one relationships
    student = relationship("Student", back_populates="user", uselist=False)
    tutor = relationship("Tutor", back_populates="user", uselist=False)
    admin = relationship("Admin", back_populates="user", uselist=False)
    
    # One-to-many relationships
    enrollments = relationship("Enrollment", back_populates="student")
    reviews = relationship("Review", back_populates="student")
    # We'll define the questions relationship in the Question model to avoid ambiguity

class Student(Base):
    __tablename__ = "students"
    
    id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    university_id = Column(Integer, ForeignKey("universities.id"))
    department_id = Column(Integer, ForeignKey("departments.id"))
    degree_id = Column(Integer, ForeignKey("degrees.id"))
    academic_year = Column(Integer)
    
    user = relationship("User", back_populates="student")
    university = relationship("University", back_populates="students")
    department = relationship("Department", back_populates="students")
    degree = relationship("Degree", back_populates="students")

class Tutor(Base):
    __tablename__ = "tutors"
    
    id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    university_id = Column(Integer, ForeignKey("universities.id"))
    department_id = Column(Integer, ForeignKey("departments.id"))
    degree_id = Column(Integer, ForeignKey("degrees.id"))
    academic_year = Column(Integer)
    qualifications = Column(Text)
    expertise_subjects = Column(String(255))
    is_verified = Column(Boolean, default=False)
    wallet_balance = Column(Numeric(precision=12, scale=2), default=0.0)
    
    user = relationship("User", back_populates="tutor")
    university = relationship("University", back_populates="tutors")
    department = relationship("Department", back_populates="tutors")
    degree = relationship("Degree", back_populates="tutors")
    kuppis = relationship("Kuppi", back_populates="tutor")

class Admin(Base):
    __tablename__ = "admins"
    
    id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    
    user = relationship("User", back_populates="admin")

class University(Base):
    __tablename__ = "universities"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    description = Column(Text)
    location = Column(String(255))
    
    students = relationship("Student", back_populates="university")
    tutors = relationship("Tutor", back_populates="university")
    departments = relationship("Department", back_populates="university")
    kuppis = relationship("Kuppi", back_populates="university")

class Department(Base):
    __tablename__ = "departments"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    description = Column(Text)
    university_id = Column(Integer, ForeignKey("universities.id"))
    
    university = relationship("University", back_populates="departments")
    students = relationship("Student", back_populates="department")
    tutors = relationship("Tutor", back_populates="department")
    degrees = relationship("Degree", back_populates="department")
    kuppis = relationship("Kuppi", back_populates="department")

class Degree(Base):
    __tablename__ = "degrees"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    description = Column(Text)
    duration = Column(Integer)
    department_id = Column(Integer, ForeignKey("departments.id"))
    
    department = relationship("Department", back_populates="degrees")
    students = relationship("Student", back_populates="degree")
    tutors = relationship("Tutor", back_populates="degree")
    kuppis = relationship("Kuppi", back_populates="degree")
    subjects = relationship("Subject", back_populates="degree")

class Subject(Base):
    __tablename__ = "subjects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    subject_code = Column(String(50))
    description = Column(Text)
    academic_year = Column(Integer)
    degree_id = Column(Integer, ForeignKey("degrees.id"))
    department_id = Column(Integer, ForeignKey("departments.id"))
    
    degree = relationship("Degree", back_populates="subjects")
    department = relationship("Department")
    kuppis = relationship("Kuppi", back_populates="subject")

class Kuppi(Base):
    __tablename__ = "kuppis"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    description = Column(Text)
    price = Column(Numeric(precision=10, scale=2))
    academic_year = Column(Integer)
    status = Column(String(50))  # PENDING, APPROVED, REJECTED
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    tutor_id = Column(Integer, ForeignKey("tutors.id"))
    university_id = Column(Integer, ForeignKey("universities.id"))
    department_id = Column(Integer, ForeignKey("departments.id"))
    degree_id = Column(Integer, ForeignKey("degrees.id"))
    subject_id = Column(Integer, ForeignKey("subjects.id"))
    
    tutor = relationship("Tutor", back_populates="kuppis")
    university = relationship("University", back_populates="kuppis")
    department = relationship("Department", back_populates="kuppis")
    degree = relationship("Degree", back_populates="kuppis")
    subject = relationship("Subject", back_populates="kuppis")  # ✅ fixed
    
    enrollments = relationship("Enrollment", back_populates="kuppi")
    reviews = relationship("Review", back_populates="kuppi")
    questions = relationship("Question", back_populates="kuppi")
    contents = relationship("KuppiContent", back_populates="kuppi")


class KuppiContent(Base):
    __tablename__ = "kuppi_contents"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    type = Column(String(50))  # VIDEO, DOCUMENT
    text_description = Column(Text)
    url = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
    kuppi_id = Column(Integer, ForeignKey("kuppis.id"))
    
    kuppi = relationship("Kuppi", back_populates="contents")

class Enrollment(Base):
    __tablename__ = "enrollments"
    
    id = Column(Integer, primary_key=True, index=True)
    enrollment_date = Column(DateTime, default=datetime.utcnow)
    expiry_date = Column(DateTime)
    payment_amount = Column(Numeric(precision=10, scale=2))
    payment_id = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    student_id = Column(Integer, ForeignKey("users.id"))
    kuppi_id = Column(Integer, ForeignKey("kuppis.id"))
    
    student = relationship("User", back_populates="enrollments")
    kuppi = relationship("Kuppi", back_populates="enrollments")

class Review(Base):
    __tablename__ = "reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    rating = Column(Integer)
    comment = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    student_id = Column(Integer, ForeignKey("users.id"))
    kuppi_id = Column(Integer, ForeignKey("kuppis.id"))
    
    student = relationship("User", back_populates="reviews")
    kuppi = relationship("Kuppi", back_populates="reviews")

class Question(Base):
    __tablename__ = "questions"
    
    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text)
    answer = Column(Text)
    answered_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    student_id = Column(Integer, ForeignKey("users.id"))
    kuppi_id = Column(Integer, ForeignKey("kuppis.id"))
    answered_by = Column(Integer, ForeignKey("users.id"))
    
    # Define relationships with explicit foreign_keys to avoid ambiguity
    student = relationship("User", foreign_keys=[student_id], backref="student_questions")
    answerer = relationship("User", foreign_keys=[answered_by], backref="answered_questions")
    kuppi = relationship("Kuppi", back_populates="questions")

class WithdrawalRequest(Base):
    __tablename__ = "withdrawal_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Numeric(precision=12, scale=2))
    bank_details = Column(Text)
    status = Column(String(50))  # PENDING, APPROVED, REJECTED
    rejection_reason = Column(Text)
    processed_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    tutor_id = Column(Integer, ForeignKey("users.id"))
    processed_by = Column(Integer, ForeignKey("users.id"))
    
    tutor = relationship("User", foreign_keys=[tutor_id])
    processed_by_user = relationship("User", foreign_keys=[processed_by])

class AcademicYear(Base):
    __tablename__ = "academic_years"
    
    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer)
    
    degree_id = Column(Integer, ForeignKey("degrees.id"))
    
    degree = relationship("Degree")