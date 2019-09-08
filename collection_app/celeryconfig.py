broker_url = 'pyamqp://guest@localhost//'
result_backend = 'rpc://'

task_serializer = 'json'
task_annotations = {
    'tasks.make_request': {'rate_limit': '1/m'}
}