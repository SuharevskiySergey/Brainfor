from app import create_app, db
from app.models.info import Info
from app.models.user import User
from app.models.info import Lesson
from app.models.info import Teacher_To_Student
from app.models.info import Cource, Part_Course
app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Info': Info, 'Lesson': Lesson, 'Teacher_To_Student': Teacher_To_Student,
            'Cource': Cource}
