from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import Base, engine, get_db
from app.models import Group, Student, Subject, Grade
from app.schemas import (
    GroupCreate,
    GroupUpdate,
    GroupRead,
    StudentCreate,
    StudentUpdate,
    StudentRead,
    SubjectCreate,
    SubjectUpdate,
    SubjectRead,
    GradeCreate,
    GradeUpdate,
    GradeRead,
    DashboardStats,
)

app = FastAPI(title="Notas Stats v5", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


Base.metadata.create_all(bind=engine)


def calculate_average(grades):
    return round(sum(item.grade for item in grades) / len(grades), 2) if grades else 0


@app.get("/api/health")
def health_check():
    return {"status": "ok", "app": "Notas Stats v5"}


@app.post("/api/demo-data")
def seed_demo_data(db: Session = Depends(get_db)):
    existing_groups = db.query(Group).count()
    if existing_groups > 0:
        return {"message": "Demo data already initialized"}

    group_1 = Group(name="3TEL", academic_year="2026", degree="Ingeniería en Telecomunicaciones")
    group_2 = Group(name="2INFO", academic_year="2025", degree="Ingeniería Informática")
    db.add_all([group_1, group_2])
    db.commit()
    db.refresh(group_1)
    db.refresh(group_2)

    student_1 = Student(name="Ana", surname="Pérez", carnet="A001", email="ana@demo.com", group_id=group_1.id)
    student_2 = Student(name="Luis", surname="García", carnet="A002", email="luis@demo.com", group_id=group_1.id)
    student_3 = Student(name="Marta", surname="López", carnet="A003", email="marta@demo.com", group_id=group_2.id)
    db.add_all([student_1, student_2, student_3])
    db.commit()
    db.refresh(student_1)
    db.refresh(student_2)
    db.refresh(student_3)

    subject_1 = Subject(name="Cálculo", code="CAL-101", credits=6, group_id=group_1.id)
    subject_2 = Subject(name="Programación", code="PRO-202", credits=6, group_id=group_1.id)
    subject_3 = Subject(name="Redes", code="RED-303", credits=5, group_id=group_2.id)
    db.add_all([subject_1, subject_2, subject_3])
    db.commit()
    db.refresh(subject_1)
    db.refresh(subject_2)
    db.refresh(subject_3)

    grade_1 = Grade(student_id=student_1.id, subject_id=subject_1.id, grade=8.7, status="approved", evaluation_type="final", academic_year="2026")
    grade_2 = Grade(student_id=student_1.id, subject_id=subject_2.id, grade=7.5, status="approved", evaluation_type="final", academic_year="2026")
    grade_3 = Grade(student_id=student_2.id, subject_id=subject_1.id, grade=6.0, status="failed", evaluation_type="final", academic_year="2026")
    grade_4 = Grade(student_id=student_2.id, subject_id=subject_2.id, grade=7.2, status="approved", evaluation_type="final", academic_year="2026")
    grade_5 = Grade(student_id=student_3.id, subject_id=subject_3.id, grade=9.1, status="approved", evaluation_type="final", academic_year="2025")
    db.add_all([grade_1, grade_2, grade_3, grade_4, grade_5])
    db.commit()

    return {"message": "Demo data loaded successfully"}


@app.get("/api/dashboard", response_model=DashboardStats)
def get_dashboard(db: Session = Depends(get_db)):
    total_students = db.query(Student).count()
    total_groups = db.query(Group).count()
    total_subjects = db.query(Subject).count()
    total_grades = db.query(Grade).count()
    grades = db.query(Grade).all()
    average_grade = calculate_average(grades)
    approved = db.query(Grade).filter(Grade.status == "approved").count()
    failed = db.query(Grade).filter(Grade.status == "failed").count()
    pending = db.query(Grade).filter(Grade.status == "pending").count()

    return DashboardStats(
        total_students=total_students,
        total_groups=total_groups,
        total_subjects=total_subjects,
        total_grades=total_grades,
        average_grade=average_grade,
        approved=approved,
        failed=failed,
        pending=pending,
    )


@app.get("/api/groups", response_model=list[GroupRead])
def get_groups(db: Session = Depends(get_db)):
    return db.query(Group).order_by(Group.id).all()


@app.post("/api/groups", response_model=GroupRead)
def create_group(data: GroupCreate, db: Session = Depends(get_db)):
    item = Group(**data.dict())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@app.get("/api/groups/{group_id}", response_model=GroupRead)
def get_group(group_id: int, db: Session = Depends(get_db)):
    item = db.query(Group).filter(Group.id == group_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Group not found")
    return item


@app.put("/api/groups/{group_id}", response_model=GroupRead)
def update_group(group_id: int, data: GroupUpdate, db: Session = Depends(get_db)):
    item = db.query(Group).filter(Group.id == group_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Group not found")
    for field, value in data.dict(exclude_unset=True).items():
        setattr(item, field, value)
    db.commit()
    db.refresh(item)
    return item


@app.delete("/api/groups/{group_id}")
def delete_group(group_id: int, db: Session = Depends(get_db)):
    item = db.query(Group).filter(Group.id == group_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Group not found")
    db.delete(item)
    db.commit()
    return {"message": "Group deleted"}


@app.get("/api/students", response_model=list[StudentRead])
def get_students(db: Session = Depends(get_db)):
    return db.query(Student).order_by(Student.id).all()


@app.post("/api/students", response_model=StudentRead)
def create_student(data: StudentCreate, db: Session = Depends(get_db)):
    if db.query(Student).filter(Student.carnet == data.carnet).first():
        raise HTTPException(status_code=400, detail="Carnet already exists")
    item = Student(**data.dict())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@app.get("/api/students/{student_id}", response_model=StudentRead)
def get_student(student_id: int, db: Session = Depends(get_db)):
    item = db.query(Student).filter(Student.id == student_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Student not found")
    return item


@app.put("/api/students/{student_id}", response_model=StudentRead)
def update_student(student_id: int, data: StudentUpdate, db: Session = Depends(get_db)):
    item = db.query(Student).filter(Student.id == student_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Student not found")
    for field, value in data.dict(exclude_unset=True).items():
        setattr(item, field, value)
    db.commit()
    db.refresh(item)
    return item


@app.delete("/api/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    item = db.query(Student).filter(Student.id == student_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Student not found")
    db.delete(item)
    db.commit()
    return {"message": "Student deleted"}


@app.get("/api/subjects", response_model=list[SubjectRead])
def get_subjects(db: Session = Depends(get_db)):
    return db.query(Subject).order_by(Subject.id).all()


@app.post("/api/subjects", response_model=SubjectRead)
def create_subject(data: SubjectCreate, db: Session = Depends(get_db)):
    if db.query(Subject).filter(Subject.code == data.code).first():
        raise HTTPException(status_code=400, detail="Subject code already exists")
    item = Subject(**data.dict())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@app.get("/api/subjects/{subject_id}", response_model=SubjectRead)
def get_subject(subject_id: int, db: Session = Depends(get_db)):
    item = db.query(Subject).filter(Subject.id == subject_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Subject not found")
    return item


@app.put("/api/subjects/{subject_id}", response_model=SubjectRead)
def update_subject(subject_id: int, data: SubjectUpdate, db: Session = Depends(get_db)):
    item = db.query(Subject).filter(Subject.id == subject_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Subject not found")
    for field, value in data.dict(exclude_unset=True).items():
        setattr(item, field, value)
    db.commit()
    db.refresh(item)
    return item


@app.delete("/api/subjects/{subject_id}")
def delete_subject(subject_id: int, db: Session = Depends(get_db)):
    item = db.query(Subject).filter(Subject.id == subject_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Subject not found")
    db.delete(item)
    db.commit()
    return {"message": "Subject deleted"}


@app.get("/api/grades", response_model=list[GradeRead])
def get_grades(db: Session = Depends(get_db)):
    return db.query(Grade).order_by(Grade.id).all()


@app.post("/api/grades", response_model=GradeRead)
def create_grade(data: GradeCreate, db: Session = Depends(get_db)):
    student_exists = db.query(Student).filter(Student.id == data.student_id).first()
    subject_exists = db.query(Subject).filter(Subject.id == data.subject_id).first()
    if not student_exists:
        raise HTTPException(status_code=404, detail="Student not found")
    if not subject_exists:
        raise HTTPException(status_code=404, detail="Subject not found")
    item = Grade(**data.dict())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@app.put("/api/grades/{grade_id}", response_model=GradeRead)
def update_grade(grade_id: int, data: GradeUpdate, db: Session = Depends(get_db)):
    item = db.query(Grade).filter(Grade.id == grade_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Grade not found")
    for field, value in data.dict(exclude_unset=True).items():
        setattr(item, field, value)
    db.commit()
    db.refresh(item)
    return item


@app.delete("/api/grades/{grade_id}")
def delete_grade(grade_id: int, db: Session = Depends(get_db)):
    item = db.query(Grade).filter(Grade.id == grade_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Grade not found")
    db.delete(item)
    db.commit()
    return {"message": "Grade deleted"}
