from collections import namedtuple
import time
import numpy as np
from niaarm.niaarm import NiaARM
from niapy.task import OptimizationType, Task


class Result(namedtuple('Result', ('rules', 'run_time'))):
    """Result of an algorithm run as a ``namedtuple``.

    Attributes:
        rules (RuleList): A list of mined association rules.
        run_time (float): The run time of the algorithm in seconds.

    """

    __slots__ = ()


def get_rules(dataset, algorithm, metrics, max_evals=np.inf, max_iters=np.inf, logging=False, **kwargs):
    """Mine association rules on a dataset.

    Args:
        dataset (Dataset): Dataset to mine rules on.
        algorithm (niapy.algorithms.Algorithm): Algorithm to use. Algorithm parameters can be passed in as keyword
         arguments.
        metrics (Union[Dict[str, float], Sequence[str]]): Metrics to take into account when computing the fitness.
         Metrics can either be passed as a Dict of pairs {'metric_name': <weight of metric>} or
         a sequence of metrics as strings, in which case, the weights of the metrics will be set to 1.
        max_evals (Optional[int]): Maximum number of iterations. Default: ``inf``
        max_iters (Optional[int]): Maximum number of fitness evaluations. Default: ``inf``
        logging (bool): Enable logging of fitness improvements. Default: ``False``.

    Returns:
        Result: a named tuple with fields (rules, run_time), where ``rules`` is a RuleList of mined rules and run_tine
        is the execution time of the algorithm in seconds.

    """
    problem = NiaARM(dataset.dimension, dataset.features, dataset.transactions, metrics, logging)
    task = Task(problem, max_evals=max_evals, max_iters=max_iters, optimization_type=OptimizationType.MAXIMIZATION)
    params = algorithm.get_parameters()
    params.update(kwargs)
    algorithm.set_parameters(**params)

    start_time = time.perf_counter()
    algorithm.run(task)
    stop_time = time.perf_counter()

    problem.rules.sort()

    return Result(problem.rules, stop_time - start_time)
