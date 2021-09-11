import unittest

from core.rnd.rndgen import MarcianiMultiStream
from core.simulation.model.scope import TaskScope
from core.simulation.model.taskgen import ExponentialTaskgen


class TaskgenTest(unittest.TestCase):
    def setUp(self):
        self.config = {
            TaskScope.TASK_1: {
                "distribution": "EXPONENTIAL",
                "parameters": {"m": 1.0 / 6.00},  # the inter-arrival mean time for tasks of type 1 (tasks/s)
            },
            TaskScope.TASK_2: {
                "distribution": "EXPONENTIAL",
                "parameters": {"m": 1.0 / 6.25},  # the inter-arrival mean time for tasks of type 2 (tasks/s)
            },
        }

        self.rndgen = MarcianiMultiStream()
        self.taskgen = ExponentialTaskgen(self.rndgen, self.config)
        self.t_stop = 100000
        self.error = 0.00169

    def test_task_generation(self):
        t_clock = 0

        while t_clock < self.t_stop:
            event = self.taskgen.generate(t_clock)
            t_clock = event.time

        rate_task_1 = self.taskgen.rates[TaskScope.TASK_1]
        rate_task_2 = self.taskgen.rates[TaskScope.TASK_2]
        rate_total = rate_task_1 + rate_task_2

        probability_task_1 = rate_task_1 / rate_total
        probability_task_2 = rate_task_2 / rate_total

        generated_task_1 = self.taskgen.generated[TaskScope.TASK_1]
        generated_task_2 = self.taskgen.generated[TaskScope.TASK_2]
        generated_total = generated_task_1 + generated_task_2

        ratio_generated_tsk_1 = generated_task_1 / generated_total
        ratio_generated_tsk_2 = generated_task_2 / generated_total

        generation_rate_tsk_1 = generated_task_1 / self.t_stop
        generation_rate_tsk_2 = generated_task_2 / self.t_stop

        self.assertLessEqual(abs(generation_rate_tsk_1 - rate_task_1) / rate_task_1, self.error)
        self.assertLessEqual(abs(generation_rate_tsk_2 - rate_task_2) / rate_task_2, self.error)

        self.assertLessEqual(abs(ratio_generated_tsk_1 - probability_task_1) / probability_task_1, self.error)
        self.assertLessEqual(abs(ratio_generated_tsk_2 - probability_task_2) / probability_task_2, self.error)


if __name__ == "__main__":
    unittest.main()
