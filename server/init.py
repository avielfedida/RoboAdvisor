from subprocess import Popen

redis_init = ["redis-server.exe", "redis.windows.conf"]
# More about beat: https://stackoverflow.com/questions/28587030/celery-schedule-not-working
celery_beat = ["celery", "-A", "celery_tasks.worker.celery", "beat"]
celery_init = ["celery", "-A", "celery_tasks.worker.celery", "worker", "--loglevel=info", "--pool=eventlet"]

pc_user = "aviel"

to_run = [
    (redis_init, '/redis-celery/',),
    # The order is important: https://stackoverflow.com/questions/9769496/celery-received-unregistered-task-of-type-run-example
    (celery_init, f'/Users/{pc_user}/Desktop/RoboAdvisor/server/'),
    (celery_beat, f'/Users/{pc_user}/Desktop/RoboAdvisor/server/'),
]

# https://stackoverflow.com/questions/30686295/how-do-i-run-multiple-subprocesses-in-parallel-and-wait-for-them-to-finish-in-py
procs = [Popen(args=params[0], cwd=params[1], shell=True) for params in to_run]
for p in procs:
    p.wait()
