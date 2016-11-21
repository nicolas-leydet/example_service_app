from locust import HttpLocust, TaskSet
import resource


resource.setrlimit(resource.RLIMIT_NOFILE, (2048, 65536))


def end_taskset(context):
    context.interrupt()


def create(context):
    context.client.post("/knoggets",
                        json={'content': 'oihf fiugh wughghs iugh sgih ghi'})


class UserBehavior(TaskSet):
    tasks = {
        create: 10,
        #end_taskset: 1,
    }

    def on_start(self):
        create(self)


class KnoggetClient(HttpLocust):
    task_set = UserBehavior
    min_wait = 3000
    max_wait = 5000
