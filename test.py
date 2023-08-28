import unittest
import threading
import time
import random
from main import MyScheduler, MyResource, MyTask, Interface


class TestScheduler(unittest.TestCase):
    def setUp(self):
        self.N = 4  # Number of resources
        self.P = 3  # Number of projects
        self.max_priority = 4  # Maximum priority level
        self.outside_interface = Interface()
        self.scheduler = MyScheduler(self.N, self.P)

    def test_scheduler(self):
        self.assertEqual(len(self.scheduler.resources), self.N)
        self.assertEqual(len(self.scheduler.project_queues), self.P)

        # Add tasks to project queues
        tasks = [
            MyTask(1, 2),
            MyTask(2, 4),
            MyTask(1, 1),
            MyTask(3, 2),
            MyTask(2, 1)
        ]
        for task in tasks:
            self.scheduler.add_task_to_queue(task)

        for i in range(self.N):
            self.scheduler.assign_task_to_resource(self.scheduler.resources[i], tasks[i])
        for i in range(self.N):
            self.assertEqual(self.scheduler.resources[i].task, tasks[i])
            self.assertTrue(self.scheduler.resources[i].busy)

        for i in range(self.N):
            self.scheduler.complete_task_on_resource(self.scheduler.resources[i])
            self.assertIsNone(self.scheduler.resources[i].task)
            self.assertFalse(self.scheduler.resources[i].busy)

    def test_scheduler_loop(self):
        scheduler_thread = threading.Thread(target=self.scheduler.scheduler_loop)
        scheduler_thread.start()

        tasks = [
            MyTask(1, 2),
            MyTask(2, 3),
            MyTask(1, 1),
            MyTask(3, 2),
            MyTask(2, 1)
        ]
        for task in tasks:
            self.scheduler.add_task_to_queue(task)

        scheduler_thread.join()

        for resource in self.scheduler.resources:
            self.assertFalse(resource.busy)


if __name__ == '__main__':
    unittest.main()
