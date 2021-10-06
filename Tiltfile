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
