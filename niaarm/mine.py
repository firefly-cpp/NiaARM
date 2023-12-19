from collections import namedtuple
import time
import numpy as np
from niaarm.niaarm import NiaARM
from niapy.task import OptimizationType, Task
from niapy.util.factory import get_algorithm
from niaarm.text import NiaARTM


class Result(namedtuple("Result", ("rules", "run_time"))):
    """Result of an algorithm run as a ``namedtuple``.

    Attributes:
        rules (RuleList): A list of mined association rules.
        run_time (float): The run time of the algorithm in seconds.

    """

    __slots__ = ()


def get_rules(
    dataset,
    algorithm,
    metrics,
    max_evals=np.inf,
    max_iters=np.inf,
    logging=False,
    **kwargs,
):
    """Mine association rules on a dataset.

    Args:
        dataset (Dataset): Dataset to mine rules on.
        algorithm (Union[niapy.algorithms.Algorithm, str]): Algorithm to use.
         Can be either an Algorithm object or the class name as a string.
         In that case, algorithm parameters can be passed in as keyword arguments.
        metrics (Union[Dict[str, float], Sequence[str]]): Metrics to take into account when computing the fitness.
         Metrics can either be passed as a Dict of pairs {'metric_name': <weight of metric>} or
         a sequence of metrics as strings, in which case, the weights of the metrics will be set to 1.
        max_evals (Optional[int]): Maximum number of iterations. Default: ``inf``. At least one of ``max_evals`` or
         ``max_iters`` must be provided.
        max_iters (Optional[int]): Maximum number of fitness evaluations. Default: ``inf``.
        logging (bool): Enable logging of fitness improvements. Default: ``False``.

    Returns:
        Result: A named tuple containing the list of mined rules and the algorithm's run time in seconds.

    """
    problem = NiaARM(
        dataset.dimension, dataset.features, dataset.transactions, metrics, logging
    )
    task = Task(
        problem,
        max_evals=max_evals,
        max_iters=max_iters,
        optimization_type=OptimizationType.MAXIMIZATION,
    )

    if isinstance(algorithm, str):
        algorithm = get_algorithm(algorithm, **kwargs)

    start_time = time.perf_counter()
    algorithm.run(task)
    stop_time = time.perf_counter()

    problem.rules.sort()

    return Result(problem.rules, stop_time - start_time)


def get_text_rules(
    corpus,
    max_terms,
    algorithm,
    metrics,
    smooth=True,
    norm=2,
    threshold=0,
    max_evals=np.inf,
    max_iters=np.inf,
    logging=False,
    **kwargs,
):
    """Mine association rules in a text corpus.

    Args:
        corpus (Corpus): Dataset to mine rules on.
        max_terms (int): Maximum number of terms in association rule.
        algorithm (Union[niapy.algorithms.Algorithm, str]): Algorithm to use.
         Can be either an Algorithm object or the class name as a string.
         In that case, algorithm parameters can be passed in as keyword arguments.
        metrics (Union[Dict[str, float], Sequence[str]]): Metrics to take into account when computing the fitness.
         Metrics can either be passed as a Dict of pairs {'metric_name': <weight of metric>} or
         a sequence of metrics as strings, in which case, the weights of the metrics will be set to 1.
        smooth (bool): Smooth idf to prevent division by 0 error. Default: ``True``.
        norm (int): Order of norm for normalizing the tf-idf matrix. Default: 2.
        threshold (Optional[float]): Threshold of tf-idf weights. If a weight is less than or equal to the
         threshold, the term is not included in the transaction. Default: 0.
        max_evals (Optional[int]): Maximum number of iterations. Default: ``inf``. At least one of ``max_evals`` or
         ``max_iters`` must be provided.
        max_iters (Optional[int]): Maximum number of fitness evaluations. Default: ``inf``.
        logging (bool): Enable logging of fitness improvements. Default: ``False``.

    Returns:
        Result: A named tuple containing the list of mined rules and the algorithm's run time in seconds.

    """
    problem = NiaARTM(
        max_terms,
        corpus.terms(),
        corpus.tf_idf_matrix(smooth=smooth, norm=norm),
        metrics,
        threshold,
        logging,
    )
    task = Task(
        problem,
        max_evals=max_evals,
        max_iters=max_iters,
        optimization_type=OptimizationType.MAXIMIZATION,
    )

    if isinstance(algorithm, str):
        algorithm = get_algorithm(algorithm, **kwargs)

    start_time = time.perf_counter()
    algorithm.run(task)
    stop_time = time.perf_counter()

    problem.rules.sort()

    return Result(problem.rules, stop_time - start_time)
