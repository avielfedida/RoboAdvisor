from subprocess import Popen

redis_init = ["redis-server.exe", "redis.windows.conf"]
celery_init = ["celery", "worker", "-A", "celery_tasks.worker.celery", "--loglevel=info", "--pool=eventlet"]
# -P solo --without-gossip --without-mingle --without-heartbeat
# celery_init = ["celery", "worker", "-A", "celery_tasks.worker.celery", "--loglevel=info", "-P", "solo",
#                "--without-gossip", "--without-mingle", "--without-heartbeat"]

pc_user = "user"

to_run = [
    (redis_init, '/redis-celery/',),
    (celery_init, f'/Users/{pc_user}/Desktop/RoboAdvisor/server/'),
]
# https://stackoverflow.com/questions/30686295/how-do-i-run-multiple-subprocesses-in-parallel-and-wait-for-them-to-finish-in-py
procs = [Popen(args=params[0], cwd=params[1], shell=True) for params in to_run]
for p in procs:
    p.wait()
