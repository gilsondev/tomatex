# Tomatex

Pomodoro timer web feito em Python e Django

# Simple API Doc

## Tasks

### Lista as tarefas cadastradas
**GET** /api/tasks

```json
[
    {
        "uid": "c02d91a9-7071-4927-a05d-c9d0deb357c2",
        "description": "Task #1",
        "created_at": "2020-01-01T11:00:00",
    },
    {
        "uid": "c02d91a9-7071-4927-a05d-c9d0deb357c2",
        "description": "Task #2",
        "created_at": "2020-01-01T12:00:00",
    }
]
```

### Cria uma nova tarefa
**POST** /api/tasks

```json
{ "description": "Task Test" }
```

### Recupera uma tarefa pelo UID
**GET** /api/tasks/{uid}

```json
{
    "uid": "c02d91a9-7071-4927-a05d-c9d0deb357c2",
    "description": "Task #2",
    "created_at": "2020-01-01T12:00:00",
}
```

### Atualiza uma tarefa pelo UID
**PUT** /api/tasks/{uid}

```json
{ "description": "Task Updated" }
```

### Remove a tarefa
**DELETE** /api/tasks/{uid}

---

# Pomodoros

### Listar os pomodoros de uma tarefa
**GET** /api/tasks/{uid}/pomodoros

```json
[
    "uid": "baa9f00a-873a-4239-8294-8f3c8b0943d1",
    "description": "Task name",
    "total_pomodoros": 1,
    "total_interruptions": 0,
    "pomodoros": [
        {
            "started_at": "2021-01-01T15:35:00",
            "end_at": "2021-01-01T15:25:00",
            "completed": true,
            "interrupted": false
        }
    ]
]
```

### Adicionar um pomodoro
**POST** /api/tasks/{uid}/pomodoros
Body:

```json
{
    "started_at": "",
    "end_at": "",
    "completed": true,
    "interrupted": false
}
```

## TODO

- [x] Preparar settings.py para 12 Factors (python-decouple)
- [x] Preparar para o PostgreSQL
- [ ] Incluir o flake8, black e isort
- [ ] Incluir o pre-commit para verificar codigo (flake8, black e isort), e outras coisas
- [ ] Criar Github Actions workflow para:
    - [ ] Verificar lint
    - [ ] Rodar os testes
    - [ ] Verificar cobertura (Codecov)
    - [ ] Efetuar o deploy no heroku
