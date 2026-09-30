CREATE TABLE grupos(
 id INTEGER PRIMARY KEY,
 nombre TEXT NOT NULL,
 curso TEXT
);

CREATE TABLE estudiantes(
 id INTEGER PRIMARY KEY,
 grupo_id INTEGER,
 nombre TEXT NOT NULL,
 carnet TEXT
);

CREATE TABLE asignaturas(
 id INTEGER PRIMARY KEY,
 nombre TEXT NOT NULL
);

CREATE TABLE notas(
 id INTEGER PRIMARY KEY,
 estudiante_id INTEGER,
 asignatura_id INTEGER,
 nota TEXT,
 estado TEXT
);