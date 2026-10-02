import { useEffect, useState } from 'react';

const API_URL = 'http://localhost:8000/api';

const emptyGroup = { name: '', academic_year: '', degree: '', description: '' };
const emptyStudent = { name: '', surname: '', carnet: '', email: '', group_id: '' };
const emptySubject = { name: '', code: '', credits: '', group_id: '', description: '' };
const emptyGrade = { student_id: '', subject_id: '', grade: '', status: 'pending', evaluation_type: 'final', academic_year: '2026' };

async function fetchJson(url, options = {}) {
  const response = await fetch(url, options);
  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || 'Error en la petición');
  }
  return response.json();
}

export default function App() {
  const [dashboard, setDashboard] = useState(null);
  const [groups, setGroups] = useState([]);
  const [students, setStudents] = useState([]);
  const [subjects, setSubjects] = useState([]);
  const [grades, setGrades] = useState([]);
  const [groupForm, setGroupForm] = useState(emptyGroup);
  const [studentForm, setStudentForm] = useState(emptyStudent);
  const [subjectForm, setSubjectForm] = useState(emptySubject);
  const [gradeForm, setGradeForm] = useState(emptyGrade);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState('');

  const loadData = async () => {
    try {
      setLoading(true);
      const [dashboardData, groupsData, studentsData, subjectsData, gradesData] = await Promise.all([
        fetchJson(`${API_URL}/dashboard`),
        fetchJson(`${API_URL}/groups`),
        fetchJson(`${API_URL}/students`),
        fetchJson(`${API_URL}/subjects`),
        fetchJson(`${API_URL}/grades`),
      ]);
      setDashboard(dashboardData);
      setGroups(groupsData);
      setStudents(studentsData);
      setSubjects(subjectsData);
      setGrades(gradesData);
      setMessage('Datos cargados correctamente');
    } catch (error) {
      setMessage(error.message || 'No se pudo cargar la información');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleGroupSubmit = async (event) => {
    event.preventDefault();
    try {
      await fetchJson(`${API_URL}/groups`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(groupForm),
      });
      setGroupForm(emptyGroup);
      await loadData();
    } catch (error) {
      setMessage(error.message);
    }
  };

  const handleStudentSubmit = async (event) => {
    event.preventDefault();
    try {
      await fetchJson(`${API_URL}/students`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ...studentForm, group_id: Number(studentForm.group_id) }),
      });
      setStudentForm(emptyStudent);
      await loadData();
    } catch (error) {
      setMessage(error.message);
    }
  };

  const handleSubjectSubmit = async (event) => {
    event.preventDefault();
    try {
      await fetchJson(`${API_URL}/subjects`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ...subjectForm, credits: Number(subjectForm.credits), group_id: Number(subjectForm.group_id) }),
      });
      setSubjectForm(emptySubject);
      await loadData();
    } catch (error) {
      setMessage(error.message);
    }
  };

  const handleGradeSubmit = async (event) => {
    event.preventDefault();
    try {
      await fetchJson(`${API_URL}/grades`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ...gradeForm,
          student_id: Number(gradeForm.student_id),
          subject_id: Number(gradeForm.subject_id),
          grade: Number(gradeForm.grade),
        }),
      });
      setGradeForm(emptyGrade);
      await loadData();
    } catch (error) {
      setMessage(error.message);
    }
  };

  const handleSeedDemo = async () => {
    try {
      await fetchJson(`${API_URL}/demo-data`, { method: 'POST' });
      await loadData();
    } catch (error) {
      setMessage(error.message);
    }
  };

  if (loading) return <div className="app-shell"><h1>Cargando Notas Stats v5...</h1></div>;

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">Notas Stats v5</div>
        <nav>
          <a href="#dashboard">Dashboard</a>
          <a href="#groups">Grupos</a>
          <a href="#students">Estudiantes</a>
          <a href="#subjects">Asignaturas</a>
          <a href="#grades">Calificaciones</a>
        </nav>
      </aside>

      <main className="main-content">
        <header className="topbar">
          <h1>Panel académico</h1>
          <button className="primary-button" onClick={handleSeedDemo}>Cargar datos demo</button>
        </header>

        {message && <div className="message-box">{message}</div>}

        <section id="dashboard" className="stats-grid">
          <div className="stat-card">
            <span>Total estudiantes</span>
            <strong>{dashboard?.total_students ?? 0}</strong>
          </div>
          <div className="stat-card">
            <span>Total grupos</span>
            <strong>{dashboard?.total_groups ?? 0}</strong>
          </div>
          <div className="stat-card">
            <span>Total asignaturas</span>
            <strong>{dashboard?.total_subjects ?? 0}</strong>
          </div>
          <div className="stat-card">
            <span>Nota media</span>
            <strong>{dashboard?.average_grade ?? 0}</strong>
          </div>
          <div className="stat-card">
            <span>Aprobadas</span>
            <strong>{dashboard?.approved ?? 0}</strong>
          </div>
          <div className="stat-card">
            <span>Suspendidas</span>
            <strong>{dashboard?.failed ?? 0}</strong>
          </div>
        </section>

        <section className="panel-grid">
          <div className="panel" id="groups">
            <h2>Crear grupo</h2>
            <form onSubmit={handleGroupSubmit} className="form-grid">
              <input value={groupForm.name} onChange={(e) => setGroupForm({ ...groupForm, name: e.target.value })} placeholder="Nombre del grupo" />
              <input value={groupForm.academic_year} onChange={(e) => setGroupForm({ ...groupForm, academic_year: e.target.value })} placeholder="Curso académico" />
              <input value={groupForm.degree} onChange={(e) => setGroupForm({ ...groupForm, degree: e.target.value })} placeholder="Carrera" />
              <textarea value={groupForm.description} onChange={(e) => setGroupForm({ ...groupForm, description: e.target.value })} placeholder="Descripción" />
              <button className="primary-button" type="submit">Guardar grupo</button>
            </form>
            <table>
              <thead>
                <tr><th>Nombre</th><th>Curso</th><th>Carrera</th></tr>
              </thead>
              <tbody>
                {groups.map((group) => (
                  <tr key={group.id}><td>{group.name}</td><td>{group.academic_year}</td><td>{group.degree}</td></tr>
                ))}
              </tbody>
            </table>
          </div>

          <div className="panel" id="students">
            <h2>Crear estudiante</h2>
            <form onSubmit={handleStudentSubmit} className="form-grid">
              <input value={studentForm.name} onChange={(e) => setStudentForm({ ...studentForm, name: e.target.value })} placeholder="Nombre" />
              <input value={studentForm.surname} onChange={(e) => setStudentForm({ ...studentForm, surname: e.target.value })} placeholder="Apellidos" />
              <input value={studentForm.carnet} onChange={(e) => setStudentForm({ ...studentForm, carnet: e.target.value })} placeholder="Carnet" />
              <input value={studentForm.email} onChange={(e) => setStudentForm({ ...studentForm, email: e.target.value })} placeholder="Correo" />
              <select value={studentForm.group_id} onChange={(e) => setStudentForm({ ...studentForm, group_id: e.target.value })}>
                <option value="">Selecciona grupo</option>
                {groups.map((group) => (
                  <option key={group.id} value={group.id}>{group.name}</option>
                ))}
              </select>
              <button className="primary-button" type="submit">Guardar estudiante</button>
            </form>
            <table>
              <thead>
                <tr><th>Nombre</th><th>Carnet</th><th>Grupo</th></tr>
              </thead>
              <tbody>
                {students.map((student) => (
                  <tr key={student.id}><td>{student.name} {student.surname}</td><td>{student.carnet}</td><td>{groups.find((group) => group.id === student.group_id)?.name ?? 'Sin grupo'}</td></tr>
                ))}
              </tbody>
            </table>
          </div>

          <div className="panel" id="subjects">
            <h2>Crear asignatura</h2>
            <form onSubmit={handleSubjectSubmit} className="form-grid">
              <input value={subjectForm.name} onChange={(e) => setSubjectForm({ ...subjectForm, name: e.target.value })} placeholder="Nombre" />
              <input value={subjectForm.code} onChange={(e) => setSubjectForm({ ...subjectForm, code: e.target.value })} placeholder="Código" />
              <input value={subjectForm.credits} onChange={(e) => setSubjectForm({ ...subjectForm, credits: e.target.value })} placeholder="Créditos" type="number" />
              <select value={subjectForm.group_id} onChange={(e) => setSubjectForm({ ...subjectForm, group_id: e.target.value })}>
                <option value="">Selecciona grupo</option>
                {groups.map((group) => (
                  <option key={group.id} value={group.id}>{group.name}</option>
                ))}
              </select>
              <textarea value={subjectForm.description} onChange={(e) => setSubjectForm({ ...subjectForm, description: e.target.value })} placeholder="Descripción" />
              <button className="primary-button" type="submit">Guardar asignatura</button>
            </form>
            <table>
              <thead>
                <tr><th>Nombre</th><th>Código</th><th>Créditos</th></tr>
              </thead>
              <tbody>
                {subjects.map((subject) => (
                  <tr key={subject.id}><td>{subject.name}</td><td>{subject.code}</td><td>{subject.credits ?? 0}</td></tr>
                ))}
              </tbody>
            </table>
          </div>

          <div className="panel" id="grades">
            <h2>Registrar nota</h2>
            <form onSubmit={handleGradeSubmit} className="form-grid">
              <select value={gradeForm.student_id} onChange={(e) => setGradeForm({ ...gradeForm, student_id: e.target.value })}>
                <option value="">Selecciona estudiante</option>
                {students.map((student) => (
                  <option key={student.id} value={student.id}>{student.name} {student.surname}</option>
                ))}
              </select>
              <select value={gradeForm.subject_id} onChange={(e) => setGradeForm({ ...gradeForm, subject_id: e.target.value })}>
                <option value="">Selecciona asignatura</option>
                {subjects.map((subject) => (
                  <option key={subject.id} value={subject.id}>{subject.name}</option>
                ))}
              </select>
              <input value={gradeForm.grade} onChange={(e) => setGradeForm({ ...gradeForm, grade: e.target.value })} placeholder="Nota" type="number" min="0" max="10" step="0.1" />
              <select value={gradeForm.status} onChange={(e) => setGradeForm({ ...gradeForm, status: e.target.value })}>
                <option value="pending">Pendiente</option>
                <option value="approved">Aprobado</option>
                <option value="failed">Suspendido</option>
              </select>
              <input value={gradeForm.academic_year} onChange={(e) => setGradeForm({ ...gradeForm, academic_year: e.target.value })} placeholder="Curso académico" />
              <button className="primary-button" type="submit">Guardar nota</button>
            </form>
            <table>
              <thead>
                <tr><th>Estudiante</th><th>Asignatura</th><th>Nota</th><th>Estado</th></tr>
              </thead>
              <tbody>
                {grades.map((grade) => {
                  const student = students.find((item) => item.id === grade.student_id);
                  const subject = subjects.find((item) => item.id === grade.subject_id);
                  return (
                    <tr key={grade.id}>
                      <td>{student ? `${student.name} ${student.surname}` : 'Desconocido'}</td>
                      <td>{subject ? subject.name : 'Desconocida'}</td>
                      <td>{grade.grade}</td>
                      <td>{grade.status}</td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </section>
      </main>
    </div>
  );
}
