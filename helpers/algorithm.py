import numpy as np
from helpers.delay import compute_delays

# optimize range exploration, binary search, save intermediate results


def increasing_function_check(correlations):
    N = len(correlations)
    max_idx = np.argmax(correlations)
    return not (max_idx > 0.1*N and max_idx < 0.9*N)


def find_best_delay(n1, n2):
    n_iteration = 15
    center = 0
    step_size = 1000  # ms
    last_best_delay = None
    for it in range(n_iteration):
        delays, correlations, los, his = compute_delays(
            n1, n2, center=center, step_size=step_size)
        best_delay = delays[np.argmax(correlations)]
        if (last_best_delay is not None and last_best_delay == best_delay) or not step_size > 1:
            return best_delay, delays, correlations, los, his

        last_best_delay = best_delay
        center = best_delay

        print(
            f"idx:{np.argmax(correlations)}, step_size:{step_size}, center:{center}")
        if increasing_function_check(correlations):
            step_size = int(step_size*1.5)
        else:
            step_size = step_size//2

    return best_delay, delays, correlations, los, his
