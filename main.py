import threading
import time
import random


class MyTask:
    def __init__(self, project, priority=1):
        self.project = project
        self.priority = priority


class MyResource:
    def __init__(self, resource_id):
        self.id = resource_id
        self.busy = False
        self.task = None

    def task_assign(self, task):
        self.task = task
        self.busy = True

    def task_complete(self):
        self.task = None
        self.busy = False


class MyScheduler:
    def __init__(self, num_resources, num_projects):
        self.resources = [MyResource(i) for i in range(num_resources)]
        self.project_queues = {i: [] for i in range(1, num_projects + 1)}
        self.lock = threading.Lock()

    def add_task_to_queue(self, task):
        self.project_queues[task.project].append(task)

    def get_next_task(self):
        for priority in range(1, max_priority + 1):
            for project, queue in self.project_queues.items():
                for task in queue:
                    if task.priority == priority:
                        queue.remove(task)
                        return task
        return None

    def assign_task_to_resource(self, resource, task):
        resource.task_assign(task)
        print(f"resource {resource.id} started task for Project {task.project} with priority {task.priority}")

    def complete_task_on_resource(self, resource):
        completed_task = resource.task
        resource.task_complete()
        print(f"resource {resource.id} completed task for Project {completed_task.project}")

    def scheduler_loop(self):
        while True:
            time.sleep(random.uniform(0.1, 2))
            new_task = outside_interface.check_for_new_task()
            if new_task:
                with self.lock:
                    self.add_task_to_queue(new_task)

            for resource in self.resources:
                if not resource.busy:
                    task = self.get_next_task()
                    if task:
                        self.assign_task_to_resource(resource, task)
                        threading.Thread(target=self.execute_task, args=(resource,)).start()

    def execute_task(self, resource):
        time.sleep(random.uniform(1, 5))
        with self.lock:
            self.complete_task_on_resource(resource)


# Constants
N = 4  # Number of resources
P = 3  # Number of projects
max_priority = 4  # Maximum priority


class Interface:
    @staticmethod
    def check_for_new_task():
        if random.random() < 0.5:
            project = random.randint(1, P)
            priority = random.randint(1, max_priority)
            return MyTask(project, priority)
        return None


outside_interface = Interface()
scheduler = MyScheduler(N, P)
scheduler_thread = threading.Thread(target=scheduler.scheduler_loop)
scheduler_thread.start()
