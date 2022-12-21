from flask import Flask, render_template, jsonify, request
import pyodbc
app = Flask(__name__, template_folder="html")
#Connect to Database
def connection():
    s = 'DESKTOP-D3J0VVB' #Your server name
    d = 'journal'
    cstr = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+s+';DATABASE='+d+';Trusted_connection=yes'
    conn = pyodbc.connect(cstr)
    return conn

#students
def getstudents():
    students = []
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM dbo.student")
    for row in cursor.fetchall():
        students.append({"id_student": row[0], "student_fio": row[1], "student_phone": row[2], "student_sex": row[3], "group_id_group": row[4]})
    conn.close()
    return students

def getstudent(id_student):
    assert isinstance(id_student, int)

    students = []
    conn = connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM dbo.student where id_student = {id_student}")
    for row in cursor.fetchall():
        students.append({"id_student": row[0], "student_fio": row[1], "student_phone": row[2], "student_sex": row[3], "group_id_group": row[4],
                        })
    conn.close()
    return students[0]

def updatestudent(id_student, student_fio, student_phone, student_sex, group_id_group):
    assert isinstance(id_student, int)
    conn = connection()
    cursor = conn.cursor()
    cursor.execute(f"UPDATE dbo.student SET student_fio='{student_fio}',student_phone='{student_phone}',student_sex='{student_sex}',group_id_group='{group_id_group}'  WHERE id_student = {id_student}")
    conn.commit()
    conn.close()
    return True
def insertstudent(student_fio, student_phone, student_sex, group_id_group):
    conn = connection()
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO dbo.student (student_fio, student_phone, student_sex, group_id_group) OUTPUT Inserted.id_student VALUES" +
        f"('{student_fio}','{student_phone}','{student_sex}','{group_id_group}')")
    id_student = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return id_student
def deletestudent(id_student):
    assert isinstance(id_student, int)
    conn = connection()
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM dbo.student WHERE id_student={id_student};")
    conn.commit()
    conn.close()
    return True
@app.route("/admin/students")
def students_view():
    students = getstudents()
    return render_template("student_admin.html", students= students)

@app.route("/students")
def students_list():

    students = getstudents()
    return render_template("student_list.html", students= students)
@app.route("/get_students", methods=["GET"])
def students():
    students = getstudents()
    return jsonify(students)


@app.route("/admin/student/<int:id_student>", methods=["POST", "GET", "DELETE", "UPDATE"])
def student(id_student):
    if request.method == 'GET':
        return jsonify(getstudent(id_student))
    elif request.method == 'POST':
        form = request.get_json()
        id_student = insertstudent(form["student_fio"], form["student_phone"], form["student_sex"], form["group_id_group"])
        return jsonify({"id_student":id_student})
    elif request.method == 'UPDATE':
        form = request.get_json()
        id_student = updatestudent(id_student, form["student_fio"], form["student_phone"], form["student_sex"], form["group_id_group"])
        return jsonify({"id_student":id_student})
    else:
        return jsonify({"status": deletestudent(id_student)})


#group

def getgroups():
    groups = []
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM dbo.[group]")
    for row in cursor.fetchall():
        groups.append({"id_group": row[0], "group_name": row[1], "group_student_count": row[2], "cafedra_id_cafedra": row[3]})
    conn.close()
    return groups

def getgroup(id_group):
    assert isinstance(id_group, int)

    groups = []
    conn = connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM dbo.[group] where id_group = {id_group}")
    for row in cursor.fetchall():
        groups.append({"id_group": row[0], "group_name": row[1], "group_student_count": row[2], "cafedra_id_cafedra": row[3]})
    conn.close()
    return groups[0]

def updategroup(id_group, group_name, group_student_count, cafedra_id_cafedra):
    assert isinstance(id_group, int)
    conn = connection()
    cursor = conn.cursor()
    cursor.execute(f"UPDATE dbo.[group] SET group_name='{group_name}',group_student_count='{group_student_count}',cafedra_id_cafedra='{cafedra_id_cafedra}'  WHERE id_group = {id_group}")
    conn.commit()
    conn.close()
    return True
def insertgroup(group_name, group_student_count, cafedra_id_cafedra):
    conn = connection()
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO dbo.[group] (group_name, group_student_count, cafedra_id_cafedra) OUTPUT Inserted.id_group VALUES" +
        f"('{group_name}','{group_student_count}','{cafedra_id_cafedra}')")
    id_group = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return id_group
def deletegroup(id_group):
    assert isinstance(id_group, int)
    conn = connection()
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM dbo.[group] WHERE id_group={id_group};")
    conn.commit()
    conn.close()
    return True
@app.route("/admin/groups")
def groups_view():
    groups = getgroups()
    return render_template("group_admin.html", groups= groups)

@app.route("/groups")
def groups_list():

    groups = getgroups()
    return render_template("group_list.html", groups= groups)
@app.route("/get_groups", methods=["GET"])
def groups():
    groups = getgroups()
    return jsonify(groups)


@app.route("/admin/group/<int:id_group>", methods=["POST", "GET", "DELETE", "UPDATE"])
def group(id_group):
    if request.method == 'GET':
        return jsonify(getgroup(id_group))
    elif request.method == 'POST':
        form = request.get_json()
        id_group = insertgroup(form["group_name"], form["group_student_count"], form["cafedra_id_cafedra"])
        return jsonify({"id_group":id_group})
    elif request.method == 'UPDATE':
        form = request.get_json()
        id_group = updategroup(id_group, form["group_name"], form["group_student_count"], form["cafedra_id_cafedra"])
        return jsonify({"id_group":id_group})
    else:
        return jsonify({"status": deletegroup(id_group)})

#teacher
def getteachers():
    teachers = []
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM dbo.teacher")
    for row in cursor.fetchall():
        teachers.append({"id_teacher": row[0], "teacher_fio": row[1],  "teacher_age": row[2],"teacher_phone": row[3],"teacher_sex": row[4],"cafedra_id_cafedra": row[5]})
    conn.close()
    return teachers

def getteacher(id_teacher):
    assert isinstance(id_teacher, int)
    teachers = []
    conn = connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM dbo.teacher where id_teacher = {id_teacher}")
    for row in cursor.fetchall():
        teachers.append({"id_teacher": row[0], "teacher_fio": row[1], "teacher_age": row[2], "teacher_phone": row[3], "teacher_sex": row[4], "cafedra_id_cafedra": row[5]})
    conn.close()
    return teachers[0]

def updateteacher(id_teacher, teacher_fio,teacher_age, teacher_phone, teacher_sex, cafedra_id_cafedra):
    assert isinstance(id_teacher, int)
    conn = connection()
    cursor = conn.cursor()
    cursor.execute(f"UPDATE dbo.teacher SET teacher_fio='{teacher_fio}',teacher_age='{teacher_age}',teacher_phone='{teacher_phone}',teacher_sex='{teacher_sex}',cafedra_id_cafedra='{cafedra_id_cafedra}' WHERE id_teacher = {id_teacher}")
    conn.commit()
    conn.close()
    return True
def insertteacher(teacher_fio, teacher_age,teacher_phone,teacher_sex,cafedra_id_cafedra):
    conn = connection()
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO dbo.teacher (teacher_fio,  teacher_age, teacher_phone, teacher_sex, cafedra_id_cafedra) OUTPUT Inserted.id_teacher VALUES " +
        f"('{teacher_fio}','{teacher_age}','{teacher_phone}','{teacher_sex}','{cafedra_id_cafedra}')")
    id_teacher = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return id_teacher
def deleteteacher(id_teacher):
    assert isinstance(id_teacher, int)
    conn = connection()
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM dbo.teacher WHERE id_teacher={id_teacher};")
    conn.commit()
    conn.close()
    return True
@app.route("/admin/teachers")
def teachers_view():
    teachers = getteachers()
    return render_template("teacher_admin.html", teachers= teachers)

@app.route("/teachers")
def teachers_list():

    teachers = getteachers()
    return render_template("teacher_list.html", teachers = teachers)

@app.route("/get_teachers", methods=["GET"])
def teachers():
    teachers = getteachers()
    return jsonify(teachers)


@app.route("/admin/teacher/<int:id_teacher>", methods=["POST", "GET", "DELETE", "UPDATE"])
def teacher(id_teacher):
    if request.method == 'GET':
        return jsonify(getteacher(id_teacher))
    elif request.method == 'POST':
        form = request.get_json()
        id_teacher = insertteacher(form["teacher_fio"], form["teacher_age"], form["teacher_phone"], form["teacher_sex"], form["cafedra_id_cafedra"] )
        return jsonify({"id_teacher":id_teacher})
    elif request.method == 'UPDATE':
        form = request.get_json()
        id_teacher = updateteacher(id_teacher, form["teacher_fio"], form["teacher_age"], form["teacher_phone"], form["teacher_sex"], form["cafedra_id_cafedra"])
        return jsonify({"id_teacher":id_teacher})
    else:
        return jsonify({"status": deleteteacher(id_teacher)})


#lesson
def getlessons():
    lessons = []
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM dbo.lesson")
    for row in cursor.fetchall():
        lessons.append({"id_lesson": row[0], "lesson_name": row[1]})
    conn.close()
    return lessons

def getlesson(id_lesson):
    assert isinstance(id_lesson, int)
    lessons = []
    conn = connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM dbo.lesson where id_lesson = {id_lesson}")
    for row in cursor.fetchall():
        lessons.append({"id_lesson": row[0], "lesson_name": row[1]})
    conn.close()
    return lessons[0]

def updatelesson(id_lesson, lesson_name):
    assert isinstance(id_lesson, int)
    conn = connection()
    cursor = conn.cursor()
    cursor.execute(f"UPDATE dbo.lesson SET lesson_name='{lesson_name}' WHERE id_lesson = {id_lesson}")
    conn.commit()
    conn.close()
    return True
def insertlesson(lesson_name):
    conn = connection()
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO dbo.lesson (lesson_name) OUTPUT Inserted.id_lesson VALUES " +
        f"('{lesson_name}')")
    id_lesson = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return id_lesson
def deletelesson(id_lesson):
    assert isinstance(id_lesson, int)
    conn = connection()
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM dbo.lesson WHERE id_lesson={id_lesson};")
    conn.commit()
    conn.close()
    return True
@app.route("/admin/lessons")
def lessons_view():
    lessons = getlessons()
    return render_template("lesson_admin.html", lessons= lessons)

@app.route("/lessons")
def lessons_list():
    lessons = getlessons()
    return render_template("lesson_list.html", lessons = lessons)

@app.route("/get_lessons", methods=["GET"])
def lessons():
    lessons = getlessons()
    return jsonify(lessons)


@app.route("/admin/lesson/<int:id_lesson>", methods=["POST", "GET", "DELETE", "UPDATE"])
def lesson(id_lesson):
    if request.method == 'GET':
        return jsonify(getlesson(id_lesson))
    elif request.method == 'POST':
        form = request.get_json()
        id_lesson = insertPost(form["lesson_name"])
        return jsonify({"id_lesson":id_lesson})
    elif request.method == 'UPDATE':
        form = request.get_json()
        id_lesson = updatelesson(id_lesson, form["lesson_name"])
        return jsonify({"id_lesson":id_lesson})
    else:
        return jsonify({"status": deletelesson(id_lesson)})

#cafedra
def getcafedras():
    cafedras = []
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM dbo.cafedra")
    for row in cursor.fetchall():
        cafedras.append({"id_cafedra": row[0], "cafedra_name": row[1], "cafedra_student_count": row[2]})
    conn.close()
    return cafedras

def getcafedra(id_cafedra):
    assert isinstance(id_cafedra, int)

    cafedras = []
    conn = connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM dbo.cafedra where id_cafedra = {id_cafedra}")
    for row in cursor.fetchall():
        cafedras.append({"id_cafedra": row[0], "cafedra_name": row[1], "cafedra_student_count": row[2]})
    conn.close()
    return cafedras[0]

def updatecafedra(id_cafedra, cafedra_name, cafedra_student_count):
    assert isinstance(id_cafedra, int)
    conn = connection()
    cursor = conn.cursor()
    cursor.execute(f"UPDATE dbo.cafedra SET cafedra_name='{cafedra_name}',cafedra_student_count='{cafedra_student_count}' WHERE id_cafedra = {id_cafedra}")
    conn.commit()
    conn.close()
    return True
def insertcafedra(cafedra_name, cafedra_student_count):
    conn = connection()
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO dbo.cafedra (cafedra_name, cafedra_student_count) OUTPUT Inserted.id_cafedra VALUES " +
        f"('{cafedra_name}','{cafedra_student_count}')")
    id_cafedra = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return id_cafedra
def deletecafedra(id_cafedra):
    assert isinstance(id_cafedra, int)
    conn = connection()
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM dbo.cafedra WHERE id_cafedra={id_cafedra};")
    conn.commit()
    conn.close()
    return True
@app.route("/admin/cafedras")
def cafedras_view():
    cafedras = getcafedras()
    return render_template("cafedra_admin.html", cafedras= cafedras)

@app.route("/cafedras")
def cafedras_list():

    cafedras = getcafedras()
    return render_template("cafedra_list.html", cafedras = cafedras)

@app.route("/get_cafedras", methods=["GET"])
def cafedras():
    cafedras = getcafedras()
    return jsonify(cafedras)


@app.route("/admin/cafedra/<int:id_cafedra>", methods=["POST", "GET", "DELETE", "UPDATE"])
def cafedra(id_cafedra):
    if request.method == 'GET':
        return jsonify(getcafedra(id_cafedra))
    elif request.method == 'POST':
        form = request.get_json()
        id_cafedra = insertcafedra(form["cafedra_name"], form["cafedra_student_count"])
        return jsonify({"id_cafedra":id_cafedra})
    elif request.method == 'UPDATE':
        form = request.get_json()
        id_cafedra = updatecafedra(id_cafedra, form["cafedra_name"], form["cafedra_student_count"])
        return jsonify({"id_cafedra":id_cafedra})
    else:
        return jsonify({"status": deletecafedra(id_cafedra)})


#student_has_lessons
def getteacher_has_lessons():
    teacher_has_lessons = []
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM dbo.teacher_has_lesson")
    for row in cursor.fetchall():
        teacher_has_lessons.append({"teacher_id_teacher": row[0], "lesson_id_lesson": row[1], "count": row[2]})
    conn.close()
    return teacher_has_lessons

def getteacher_has_lesson(teacher_id_teacher):
    assert isinstance(teacher_id_teacher, int)

    teacher_has_lessons = []
    conn = connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM dbo.teacher_has_lesson where teacher_id_teacher = {teacher_id_teacher}")
    for row in cursor.fetchall():
        teacher_has_lessons.append({"teacher_id_teacher": row[0], "lesson_id_lesson": row[1], "count": row[2]})
    conn.close()
    return teacher_has_lessons[0]

def updateteacher_has_lesson(teacher_id_teacher, lesson_id_lesson, count):
    assert isinstance(teacher_id_teacher, int)
    conn = connection()
    cursor = conn.cursor()
    cursor.execute(f"UPDATE dbo.teacher_has_lesson SET lesson_id_lesson='{lesson_id_lesson}',count='{count}' WHERE teacher_id_teacher = {teacher_id_teacher}")
    conn.commit()
    conn.close()
    return True
def insertteacher_has_lesson(lesson_id_lesson, count):
    conn = connection()
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO dbo.teacher_has_lesson (lesson_id_lesson, count) OUTPUT Inserted.teacher_id_teacher VALUES " +
        f"('{lesson_id_lesson}','{count}')")
    teacher_id_teacher = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return teacher_id_teacher
def deleteteacher_has_lesson(teacher_id_teacher):
    assert isinstance(teacher_id_teacher, int)
    conn = connection()
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM dbo.teacher_has_lesson WHERE teacher_id_teacher={teacher_id_teacher};")
    conn.commit()
    conn.close()
    return True
@app.route("/admin/teacher_has_lessons")
def teacher_has_lessons_view():
    teacher_has_lessons = getteacher_has_lessons()
    return render_template("teacher_has_lesson_admin.html", teacher_has_lessons= teacher_has_lessons)

@app.route("/teacher_has_lessons")
def teacher_has_lessons_list():

    teacher_has_lessons = getteacher_has_lessons()
    return render_template("teacher_has_lesson_list.html", teacher_has_lessons = teacher_has_lessons)

@app.route("/get_teacher_has_lessons", methods=["GET"])
def teacher_has_lessons():
    teacher_has_lessons = getteacher_has_lessons()
    return jsonify(teacher_has_lessons)


@app.route("/admin/teacher_has_lesson/<int:teacher_id_teacher>", methods=["POST", "GET", "DELETE", "UPDATE"])
def teacher_has_lesson(teacher_id_teacher):
    if request.method == 'GET':
        return jsonify(getteacher_has_lesson(teacher_id_teacher))
    elif request.method == 'POST':
        form = request.get_json()
        teacher_id_teacher = insertteacher_has_lesson(form["lesson_id_lesson"], form["count"])
        return jsonify({"teacher_id_teacher":teacher_id_teacher})
    elif request.method == 'UPDATE':
        form = request.get_json()
        teacher_id_teacher = updateteacher_has_lesson(teacher_id_teacher, form["lesson_id_lesson"], form["count"])
        return jsonify({"teacher_id_teacher":teacher_id_teacher})
    else:
        return jsonify({"status": deleteteacher_has_lesson(teacher_id_teacher)})


#student_has_lessons
def getstudent_has_lessons():
    student_has_lessons = []
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM dbo.student_has_lesson")
    for row in cursor.fetchall():
        student_has_lessons.append({"student_id_student": row[0], "lesson_id_lesson": row[1], "mark": row[2]})
    conn.close()
    return student_has_lessons

def getstudent_has_lesson(student_id_student):
    assert isinstance(student_id_student, int)

    student_has_lessons = []
    conn = connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM dbo.student_has_lesson where student_id_student = {student_id_student}")
    for row in cursor.fetchall():
        student_has_lessons.append({"student_id_student": row[0], "lesson_id_lesson": row[1], "mark": row[2]})
    conn.close()
    return student_has_lessons[0]

def updatestudent_has_lesson(student_id_student, lesson_id_lesson, mark):
    assert isinstance(student_id_student, int)
    conn = connection()
    cursor = conn.cursor()
    cursor.execute(f"UPDATE dbo.student_has_lesson SET lesson_id_lesson='{lesson_id_lesson}',mark='{mark}' WHERE student_id_student = {student_id_student}")
    conn.commit()
    conn.close()
    return True
def insertstudent_has_lesson(lesson_id_lesson, mark):
    conn = connection()
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO dbo.student_has_lesson (lesson_id_lesson, mark) OUTPUT Inserted.student_id_student VALUES " +
        f"('{lesson_id_lesson}','{mark}')")
    student_id_student = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return student_id_student
def deletestudent_has_lesson(student_id_student):
    assert isinstance(student_id_student, int)
    conn = connection()
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM dbo.student_has_lesson WHERE student_id_student={student_id_student};")
    conn.commit()
    conn.close()
    return True
@app.route("/admin/student_has_lessons")
def student_has_lessons_view():
    student_has_lessons = getstudent_has_lessons()
    return render_template("student_has_lesson_admin.html", student_has_lessons= student_has_lessons)

@app.route("/student_has_lessons")
def student_has_lessons_list():

    student_has_lessons = getstudent_has_lessons()
    return render_template("student_has_lesson_list.html", student_has_lessons = student_has_lessons)

@app.route("/get_student_has_lessons", methods=["GET"])
def student_has_lessons():
    student_has_lessons = getstudent_has_lessons()
    return jsonify(student_has_lessons)


@app.route("/admin/student_has_lesson/<int:student_id_student>", methods=["POST", "GET", "DELETE", "UPDATE"])
def student_has_lesson(student_id_student):
    if request.method == 'GET':
        return jsonify(getstudent_has_lesson(student_id_student))
    elif request.method == 'POST':
        form = request.get_json()
        student_id_student = insertstudent_has_lesson(form["lesson_id_lesson"], form["mark"])
        return jsonify({"student_id_student":student_id_student})
    elif request.method == 'UPDATE':
        form = request.get_json()
        student_id_student = updatestudent_has_lesson(student_id_student, form["lesson_id_lesson"], form["mark"])
        return jsonify({"student_id_student":student_id_student})
    else:
        return jsonify({"status": deletestudent_has_lesson(student_id_student)})

#All
@app.route("/")
def main():
    return render_template("index.html")


if(__name__ == "__main__"):
    app.run()
