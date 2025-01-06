import numpy as np

def calculate_ndvi_stats(ndvi_array):
    stats = {
        "min": np.min(ndvi_array),
        "max": np.max(ndvi_array),
        "mean": np.mean(ndvi_array),
        "std": np.std(ndvi_array)
    }
    return stats

def calculate_ndvi_change(base_array, comparison_array):
    change = comparison_array - base_array
    return {
        "new_vegetation": np.sum(change > 0.5),
        "lost_vegetation": np.sum(change < 0.3),
        "change_array": change.tolist()
    }