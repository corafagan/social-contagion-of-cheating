
def calculate_mean_cheaters(randomized_results):
    
    """ 
    Function to calculate the mean number of teams with specific cheater counts (0 to 4)

    Takes: 
    - randomized_results: 
    
    """

    # Initialize a dictionary to store the total count of teams with specific cheater counts (0 to 4)
    cheaters_count_sum = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}
    num_iterations = len(randomized_results)
    
    # Loop through each iteration's result
    for result in randomized_results:

        # Loop through the cheater counts in the current result and update the total count for valid cheater counts (0 to 4)
        for cheater_count in result.values():
            
            if cheater_count in cheaters_count_sum:
                cheaters_count_sum[cheater_count] += 1
    
    # Calculate the mean for each cheater count
    mean_cheaters = {cheater_count: cheaters_count_sum[cheater_count] / num_iterations 
                     for cheater_count in cheaters_count_sum}
    
    return mean_cheaters

def calculate_confidence_intervals(randomized_results, confidence_level=0.95):
    
    """
    Calculate the confidence intervals for cheater counts across multiple simulations.

    This function computes the confidence intervals for the mean cheater count for each
    possible cheater count (0, 1, 2, 3, 4) across all simulations in the provided
    `randomized_results`. The confidence intervals are calculated based on a z-score for the
    specified confidence level (default is 95%).

    Takes:
    - randomized_results (list of dict): A list of dictionaries where each dictionary contains
      cheater count data for one simulation iteration.
    - confidence_level (float, optional): The desired confidence level for the intervals. Default is 0.95.

    Returns:
    - dict: A dictionary where keys are cheater counts (0, 1, 2, 3, 4) and values are tuples
      representing the lower and upper bounds of the confidence intervals for each cheater count.
    """
    
    # Calculate the mean cheater count for each cheater count (0, 1, 2, 3, 4)
    mean_cheaters = calculate_mean_cheaters(randomized_results)
    
    # Initialize a dictionary to store confidence intervals
    confidence_intervals = {}
    
    # Calculate standard deviation for each cheater count across iterations
    for cheater_count in mean_cheaters:
        
        # Collect all values for this cheater_count from each iteration
        values = [result.get(cheater_count, 0) for result in randomized_results]  # Default to 0 if not present
        
        # Calculate mean of values
        mean_value = mean_cheaters[cheater_count]
        
        # Calculate standard deviation
        squared_diffs = [(value - mean_value) ** 2 for value in values]
        variance = sum(squared_diffs) / len(values)
        standard_deviation = variance ** 0.5
        
        # Calculate margin of error using z-score for 95% confidence
        z_score = 1.96  # For 95% confidence
        margin_of_error = z_score * (standard_deviation / len(values) ** 0.5)
        
        # Calculate confidence interval
        confidence_intervals[cheater_count] = (mean_value - margin_of_error, mean_value + margin_of_error)
    
    return confidence_intervals

def calculate_mean_observers(randomized_results):
    """
    Calculates the mean number of players who start cheating after observing a cheater 
    across multiple simulation iterations.

    Takes:
    - randomized_results (list of int): A list where each element represents the number of 
      players who started cheating after observing a cheater in a single simulation iteration.

    Returns:
    - float: The mean number of players who started cheating after observing a cheater 
      across all simulation iterations.
    """
    
    # Calculate the mean for the number of observers who start cheating
    num_iterations = len(randomized_results)
    total_count = sum(randomized_results)

    return total_count / num_iterations


def calculate_observer_confidence_intervals(randomized_results, confidence_level=0.95):
    """
    Calculates the confidence interval for the mean number of players who start cheating after observing 
    a cheater, based on multiple simulation iterations.

    Takes:
    - randomized_results (list of int): A list where each element represents the number of players 
      who started cheating after observing a cheater in a single simulation iteration.
    - confidence_level (float, optional): The desired confidence level for the interval (default is 0.95).

    Returns:
    - tuple: A tuple containing the lower and upper bounds of the confidence interval for the mean number 
      of players who started cheating after observing a cheater.
    """
    
    # Calculate the mean observer count
    mean_observers = calculate_mean_observers(randomized_results)
    
    # Calculate the standard deviation for the observers' counts
    squared_diffs = [(count - mean_observers) ** 2 for count in randomized_results]
    variance = sum(squared_diffs) / len(randomized_results)
    standard_deviation = variance ** 0.5
    
    # Calculate margin of error using z-score for 95% confidence
    z_score = 1.96  # For 95% confidence
    margin_of_error = z_score * (standard_deviation / len(randomized_results) ** 0.5)
    
    # Calculate confidence interval
    confidence_interval = (mean_observers - margin_of_error, mean_observers + margin_of_error)
    
    return confidence_interval
