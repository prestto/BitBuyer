# specify k8s config
k8s_yaml('./k8s/api.yml')

# run app
k8s_resource('bitbuyer-api', port_forwards=8000)

print('Setting up seed script')
local_resource(
    'seed',
    cmd='./run.sh seed',
    deps=['./scripts'],
    trigger_mode=TRIGGER_MODE_MANUAL
)

print('Setting up reset script')
local_resource(
    'reset',
    cmd='./run.sh reset',
    deps=['./scripts'],
    trigger_mode=TRIGGER_MODE_MANUAL
)
