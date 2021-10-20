# specify k8s config
k8s_yaml(kustomize('./k8s/overlays/dev'))

# run app
k8s_resource('bitbuyer-api', port_forwards=8000)
k8s_resource('postgresql-db')

docker_build('user632716/bitbuyer:latest', '.', dockerfile='./docker/Dockerfile-bitbuyer', live_update=[
    sync('.', '/app'),
    run('cd /app && pip install -r requirements.txt', trigger='./requirements.txt'),

    # if all that changed was start-time.txt, make sure the server
    # reloads so that it will reflect the new startup time
    run('touch /app/app.py', trigger='./start-time.txt'),
])

print('Setting up seed script')
local_resource(
    'seed',
    cmd='./run.sh seed',
    deps=['./scripts'],
    trigger_mode=TRIGGER_MODE_MANUAL
)

print('Setting up makemigrations command')
local_resource(
    'make_migrations',
    cmd='./run.sh makemigrations',
    deps=['./common/', './test', './scripts'],
    trigger_mode=TRIGGER_MODE_MANUAL
)

print('Setting up migrate command')
local_resource(
    'migrate',
    cmd='./run.sh migrate',
    deps=['./common/', './scripts'],
    trigger_mode=TRIGGER_MODE_MANUAL
)
