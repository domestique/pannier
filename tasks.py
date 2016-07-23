import os
from invoke import task, util

LOCAL_ROOT = os.path.dirname(os.path.realpath(__file__))
DOCKER_DEV_COMMAND_ROOT = 'docker-compose -p pannier -f docker-compose.yml -f docker-compose.override.yml'
DOCKER_PROD_COMMAND_ROOT = 'docker-compose -p pannier -f docker-compose.yml -f docker-compose.prod.yml'


@task
def control_docker_dev(ctx, cmd='up -d'):
    ctx.run('cd {} && {} {}'.format(
        LOCAL_ROOT,
        DOCKER_DEV_COMMAND_ROOT,
        cmd
    ))


@task
def run_tests(ctx, test_module='pannier', opts='', pty=False):
    print("Cleaning out pycs")
    ctx.run('find . -type f -name \*.pyc -delete')
    with util.cd(os.path.join(LOCAL_ROOT, 'pannier_project')):
        ctx.run(
            'TESTS=true coverage run --source=pannier manage.py test {} {}'.format(
                test_module, opts
            ),
            pty=pty
        )
        ctx.run('coverage xml')


@task
def create_superuser(ctx):
    ctx.run(
        'docker exec -it pannier_pannier_1 /bin/bash -c "python3 manage.py createsuperuser"',
        pty=True
    )
