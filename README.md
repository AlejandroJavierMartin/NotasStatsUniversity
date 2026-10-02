# Notas Stats v5

Aplicación académica para gestionar grupos, estudiantes, asignaturas y calificaciones.

## Inicio rápido

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Luego abre la interfaz en http://localhost:5173.

## Funcionalidades MVP

- Dashboard con indicadores principales
- CRUD de grupos
- CRUD de estudiantes
- CRUD de asignaturas
- CRUD de calificaciones
- Datos demo para pruebas rápidas
- API REST con SQLite

## Estructura

```text
backend/
  app/
    database.py
    models.py
    schemas.py
    main.py
  requirements.txt
  notas_stats.db
frontend/
  src/
  package.json
```
