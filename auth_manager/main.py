from fastapi import FastAPI

from .routers import account, access_right, project

app = FastAPI()

app.include_router(account.router,
                   tags=['account'],
                   prefix='account')
app.include_router(access_right.router,
                   tags=['access_right'],
                   prefix='access_right')
app.include_router(project.router,
                   tags=['project'],
                   prefix='project')
