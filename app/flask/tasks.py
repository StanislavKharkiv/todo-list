import threading

from invoke import task


@task
def devcron(ctx, crontab_name='crontab'):
    ctx.run(f'python devcron.py {crontab_name}')


@task
def run(ctx):
    thread_cron = threading.Thread(target=devcron, args=(ctx,))
    thread_cron.start()

    ctx.run('python -u server.py')



