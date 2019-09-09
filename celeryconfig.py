broker_url = 'pyamqp://guest@localhost//'
result_backend = 'rpc://'

task_serializer = 'json'
task_annotations = {
    'collection_app.tasks.make_request': {'rate_limit': '10/s'}
}