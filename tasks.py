

from celery import Celery
app = Celery('tasks', broker='redis://localhost:6379/0', backend='redis://localhost')


app.conf.timezone = 'UTC'
@app.task
def add(x, y):
    z = x + y
    print(z)
    return 3

app.conf.beat_schedule = {
    'add-every-1-seconds': {  
        'task': 'tasks.add',  
        'schedule': 1.0,      
        'args': (16, 16)       
    },
}