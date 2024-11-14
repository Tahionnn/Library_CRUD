from fastapi import FastAPI
from app.book.router import book_router
from app.user.router import user_router
from app.auth.router import auth_router
from app.sheduler import *

app = FastAPI()


routers = (user_router, book_router, auth_router)

for router in routers:
    app.include_router(router)


@app.on_event("startup")
async def start_scheduler():
    scheduler.start()
    scheduler.add_job(forced_return, 'interval', hours=1)

@app.on_event("shutdown")
async def shutdown_scheduler():
    scheduler.shutdown()

@app.get("/jobs/")
async def get_jobs():
    jobs = scheduler.get_jobs()
    return {"jobs": [job.id for job in jobs]}


@app.get("/check_jobs/")
async def check_jobs():
    jobs = scheduler.get_jobs()
    return {"jobs": [{"id": job.id, "next_run_time": job.next_run_time} for job in jobs]}