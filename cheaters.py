from datetime import datetime
import shuffle

## Question 1 

def organize_teams_by_match(teams):
    """
    Organizes player account IDs into teams, where teams are uniquely identified by a combination of match_id and team_id.

    Takes:
        - teams: A list of tuples, where each tuple is in the format (match_id, player_acc_id, team_id).

    Returns:
        - match_teams: A dictionary where the keys are tuples (match_id, team_id) and the values are lists of player account IDs.
    """
    match_teams = {}

    for match_id, player_acc_id, team_id in teams:
        team_key = (match_id, team_id)
        if team_key not in match_teams:
            match_teams[team_key] = []
        match_teams[team_key].append(player_acc_id)

    return match_teams

def count_cheaters_per_team(teams, cheaters):
    """
    Counts the number of cheaters on each team.

    Takes:
    - teams: A dictionary where keys are team IDs, and values are lists of players (match_id, player_acc_id).
    - cheaters: A set of player account IDs that represent cheaters.

    Returns:
    - A dictionary with team IDs as keys and the number of cheaters on that team as values.
    """
    cheaters_per_team = {}
    
    # Iterate through each team
    for team_key, players in teams.items():
        # Count how many players in this team are cheaters
        cheater_count = sum(1 for player_acc_id in players if player_acc_id in cheaters)
        
        # Store the count of cheaters for this team
        cheaters_per_team[team_key] = cheater_count
    
    return cheaters_per_team

def summarize_cheaters_per_team(cheaters_per_team):
    """
    Summarizes the number of teams with specific counts of cheaters.

    Takes:
    - cheaters_per_team: A dictionary where keys are (match_id, team_id) tuples
                          and values are counts of cheaters on that team.

    Returns:
    - Statements of the form: "Number of teams with X cheater(s): Y".
    """
    # Count the occurrences of each cheater count
    cheater_counts = {}
    
    for count in cheaters_per_team.values():
        if count not in cheater_counts:
            cheater_counts[count] = 0
        cheater_counts[count] += 1

    # Print the summary
    for count, num_teams in sorted(cheater_counts.items()):
        print(f"Number of teams with {count} cheater(s): {num_teams}")

## Question 2 

def filter_kills_by_cheaters(kills, cheaters):
    """
    Filters kills data to include only rows where the killer is in the cheaters set.

    Takes:
    - data (list of lists): The kills data, where each row is a list containing:
        [match_id, killer_acc_id, killed_acc_id, kill_time].
    - cheaters_set (set): A set of account IDs that are cheaters.

    Returns:
    - list of lists: A filtered list of rows where the killer is in the cheaters set.
    """
    return [row for row in kills if row[1] in cheaters]

def cheaters_after_killed(killers, cheaters):
    """
    Counts how many players got killed by an active cheater on at least one occasion 
    and then started cheating after their death, ensuring the killer and killed 
    are in the same match.

    Takes:
    - killers (list of lists): The filtered kills data where each row is:
        [match_id, killer_acc_id, killed_acc_id, kill_time].
    - cheaters (list of tuples): The cheaters data where each tuple is:
        (player_acc_id, cheating_start_time, banned_date).

    Returns:
    - int: The count of players who got killed by an active cheater and started cheating afterwards.
    """
    # Create a dictionary of cheaters with their start times
    cheater_start_times = {
        player_acc_id: cheating_start_time if isinstance(cheating_start_time, datetime) 
        else datetime.strptime(cheating_start_time, "%Y-%m-%d %H:%M:%S.%f")
        for player_acc_id, cheating_start_time, _ in cheaters
    }

    # Initialize count and a set to track players who have already been counted
    count = 0
    counted_players = set()

     # Iterate over the kills
    for match_id, killer_acc_id, killed_acc_id, kill_time in killers:
        
        # Convert kill_time to datetime if it's a string
        kill_time = datetime.strptime(kill_time, "%Y-%m-%d %H:%M:%S.%f") if isinstance(kill_time, str) else kill_time

        # Check if the killer is an active cheater at the time of the kill
        if killer_acc_id in cheater_start_times:
            killer_cheating_start_time = cheater_start_times[killer_acc_id]
            
            # Check the killer is actively cheating
            if killer_cheating_start_time <= kill_time: 

                # Check if the killed player is not cheating at the time of the kill
                if killed_acc_id not in cheater_start_times or cheater_start_times[killed_acc_id] >= kill_time:
                   
                    # If the killed player starts cheating later
                    if killed_acc_id in cheater_start_times and cheater_start_times[killed_acc_id] >= kill_time:

                        # Only count the player once
                        if killed_acc_id not in counted_players:
                            count += 1
                            counted_players.add(killed_acc_id)
    return count

## Question 3

def get_kill_time(kill):
    """
    Helper function to extract the kill_time from a kill event tuple.

    Takes:
    - kill (tuple): A kill event tuple.

    Returns:
    - datetime: The kill_time from the tuple.
    """
    return kill[2]

def sort_kills_by_time(kills):
    """
    Sorts the kills list by kill_time.

    Takes:
    - kills (list of tuples): Each entry contains [killer_id, killed_id, kill_time].

    Returns:
    - list: Sorted kills based on kill_time.
    """
    return sorted(kills, key=get_kill_time)

def find_first_cheater(kills, cheater_ids):
    """
    Finds the first cheater who kills three different players in a match.

    Takes:
    - kills (list of tuples): Each entry contains [killer_id, killed_id, kill_time].
    - cheater_ids (set): A set of cheater IDs for quick lookup.

    Returns:
    - tuple: The observed_time and the killer_id of the first cheater, or None if no cheater found.
    """
    kills_by_killer = {}

    for killer_id, killed_id, kill_time in kills:
        if killer_id not in kills_by_killer:
            kills_by_killer[killer_id] = set()

        kills_by_killer[killer_id].add(killed_id)

        if len(kills_by_killer[killer_id]) >= 3:
            if killer_id in cheater_ids:
                return kill_time, killer_id
            break
    return None

def filter_kills_after_observed_time(kills, observed_time):
    """
    Filters kills that occur after the observed_time.

    Takes:
    - kills (list of tuples): Each entry contains [killer_id, killed_id, kill_time].
    - observed_time (datetime): The time after which kills are included.

    Returns:
    - list: The kills that occurred after the observed_time.
    """
    return [
        (killer_id, killed_id, kill_time, observed_time)
        for killer_id, killed_id, kill_time in kills
        if kill_time > observed_time
    ]

def filter_kills_by_cheating_time(kills, cheaters_data):
    """
    Filters kills to only include data after the first time a player kills three different players
    and is a cheater. Returns a dictionary of filtered kills for each match.
    
    Takes:
    - kills (list of tuples): Each entry contains [match_id, killer_id, killed_id, kill_time].
    - cheaters_data (list): List of cheaters, where each entry contains [player_acc_id, cheating_start_time, banned_date].
    
    Returns:
    - dict: A dictionary where key is match_id and value is a list of filtered kills.
    """
    # Organize kills by match_id
    kills_by_match = {}
    for match_id, killer_id, killed_id, kill_time in kills:
        if match_id not in kills_by_match:
            kills_by_match[match_id] = []
        kills_by_match[match_id].append((killer_id, killed_id, kill_time))

    # Create a set of cheater ids for quick lookup
    cheater_ids = {cheater[0] for cheater in cheaters_data}

    # Create a dictionary to store the observed time for each match
    result = {}

    # Iterate through each match's kills
    for match_id, match_kills in kills_by_match.items():
        # Sort kills by time
        sorted_kills = sort_kills_by_time(match_kills)

        # Find the first cheater and observed time for this match
        observed_data = find_first_cheater(sorted_kills, cheater_ids)
        if observed_data:
            observed_time, _ = observed_data
            # Store the observed time in result
            result[match_id] = observed_time

    # Filter kills after the observed time for each match
    filtered_kills_by_match = {}
    for match_id, match_kills in kills_by_match.items():
        if match_id in result:
            observed_time = result[match_id]
            if isinstance(observed_time, str):
                observed_time = datetime.strptime(observed_time, "%Y-%m-%d %H:%M")
            filtered_kills_by_match[match_id] = filter_kills_after_observed_time(match_kills, observed_time)

    return filtered_kills_by_match

def update_observers(match_observers, killer_id, killed_id, kill_time, observed_time, cheater_info):
    """
    Update the observers set by adding the killer and killed IDs based on certain conditions,
    checking if they are cheaters at the time of the kill.

    Takes:
    - match_observers (set): The set of observer IDs for the current match.
    - killer_id (int): The ID of the killer.
    - killed_id (int): The ID of the killed player.
    - kill_time (datetime): The time of the kill.
    - observed_time (datetime): The time when the kill is observed.
    - cheater_info (dict): A dictionary of player IDs and their cheating start times.

    Returns:
    - None: The observers set is modified in place.
    """
    # Check if the killer or the killed player is a cheater at the time of the kill
    is_killer_cheater = killer_id in cheater_info and cheater_info[killer_id] <= kill_time
    is_killed_cheater = killed_id in cheater_info and cheater_info[killed_id] <= kill_time

    # Add the IDs to the observers set if the kill_time is greater than observed_time
    if not is_killer_cheater and not is_killed_cheater and kill_time > observed_time:
        match_observers.add(killer_id)
        match_observers.add(killed_id)

def process_match_kills(kills, cheater_info):
    """
    Process the kills in a match and return a set of observers (unique player IDs).
    
    Takes:
    - kills (list): A list of tuples (killer_id, killed_id, kill_time, observed_time).
    - cheater_info (dict): A dictionary of player IDs and their cheating start times.
    
    Returns:
    - set: A set of unique player IDs (killers and killed players) who are observers.
    """
    match_observers = set()

    # Iterate through the kills and check the conditions for each
    for killer_id, killed_id, kill_time, observed_time in kills:
        update_observers(match_observers, killer_id, killed_id, kill_time, observed_time, cheater_info)

    return match_observers

def find_observers(filtered_kills_by_cheating_time, cheaters_data):
    """
    Find unique killer_ids and killed_ids for each match where kill_time >= observed_time 
    and the kill was not made by a cheater.

    Takes:
    - filtered_kills_by_cheating_time (dict): A dictionary where key is match_id and value is a list of tuples
            (killer_id, killed_id, kill_time, observed_time) for kills after the first
            player kills three different players.
    - cheaters_data (list): A list of cheaters, where each entry contains:
                            [player_acc_id, cheating_start_time (datetime), banned_date (datetime)].

    Returns:
    - observers (dict): A dictionary where the key is match_id and the value is a set of unique player_ids 
                         (killer_ids and killed_ids) who are involved in kills after the observed time.
    """
    # Create a dictionary to store cheater info for quick lookup
    cheater_info = {cheater[0]: cheater[1] for cheater in cheaters_data}

    # Initialize the observers dictionary
    observers = {}

    # Iterate over the filtered kills by match
    for match_id, kills in filtered_kills_by_cheating_time.items():
        # Process the kills for each match and get the unique observers
        match_observers = process_match_kills(kills, cheater_info)

        # Store the set of unique ids for this match in the observers dictionary
        observers[match_id] = match_observers

    return observers

def get_match_end_times(filtered_kills_by_cheating_time):
    """
    Calculate the end times of each match based on the maximum kill time.

    Takes:
    - filtered_kills_by_cheating_time (dict): A dictionary of kills per match.

    Returns:
    - dict: A dictionary where each match_id maps to the end time of the match.
    """
    return {
        match_id: max(kill_time for _, _, kill_time, _ in kills)
        for match_id, kills in filtered_kills_by_cheating_time.items()
    }

def get_observed_times(filtered_kills_by_cheating_time):
    """
    Get the first observed time for each match based on the first kill's observed time.

    Takes:
    - filtered_kills_by_cheating_time (dict): A dictionary of kills per match.

    Returns:
    - dict: A dictionary where each match_id maps to the first observed time.
    """
    return {
        match_id: kills[0][2]  # Get the first observed_time from the first kill in the match
        for match_id, kills in filtered_kills_by_cheating_time.items()
    }

def check_if_cheater_started_after_observed_time(observer_id, observed_time, match_end, cheater_start_times):
    """
    Check if a cheater started cheating after observing a cheater.

    Takes:
    - observer_id (int): The ID of the observer.
    - observed_time (datetime): The time when the observer observed a kill.
    - match_end (datetime): The time when the match ended.
    - cheater_start_times (dict): A dictionary of cheater player IDs and their start times.

    Returns:
    - bool: True if the observer started cheating after observing a cheater, otherwise False.
    """
    if observer_id in cheater_start_times:
        cheater_start_time = cheater_start_times[observer_id]
        return cheater_start_time >= match_end and cheater_start_time > observed_time
    return False

def filter_cheaters(observers, filtered_kills_by_cheating_time, cheaters_data):
    """
    Filters observers who started cheating after observing a cheater.

    Takes:
    - observers (dict): A dictionary where the key is match_id and the value is a set of observer_ids.
    - filtered_kills_by_cheating_time (dict): A dictionary where key is match_id and value is a list of tuples
            (killer_id, killed_id, kill_time, observed_time) for kills after the first
            player kills three different players.
    - cheaters_data (list): A list of cheaters, where each entry contains:
                            [player_acc_id, cheating_start_time (datetime), banned_date (datetime)].

    Returns:
    - filtered_cheaters (set): The set of observer_ids who started cheating after observing a cheater.
    """
    # Map cheater player IDs to their cheating start times
    cheater_start_times = {cheater[0]: cheater[1] for cheater in cheaters_data}

    # Precompute match end times and observed times
    match_end_dict = get_match_end_times(filtered_kills_by_cheating_time)
    observed_time_by_match = get_observed_times(filtered_kills_by_cheating_time)

    # Track the filtered cheaters
    filtered_cheaters = set()

    # Iterate over the observers and check if they started cheating after observing
    for match_id, observer_ids in observers.items():
        if match_id not in observed_time_by_match or match_id not in match_end_dict:
            continue

        observed_time = observed_time_by_match[match_id]
        match_end = match_end_dict[match_id]

        # Check each observer's cheating start time
        for observer_id in observer_ids:
            if check_if_cheater_started_after_observed_time(observer_id, observed_time, match_end, cheater_start_times):
                filtered_cheaters.add(observer_id)

    return len(filtered_cheaters)