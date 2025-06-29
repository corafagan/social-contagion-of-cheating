import random
import cheaters

def randomize_teams(match_teams_dict):

    """
    Function to randomize players' teams for each match. 
    
    Takes: 
    - Dictionary of match teams where keys are (match_id, team_id) tuples and values are lists of player account IDs.

    Returns: 
    - Dictionary of randomized teams where keys are (match_id, team_id) tuples and values are lists of player account IDs.
    
    """

    randomized_teams_by_match = {}

    # Group players by match
    matches = {}
    for (match_id, team_id), players in match_teams_dict.items():
        if match_id not in matches:
            matches[match_id] = {"players": [], "teams": []}
        matches[match_id]["players"].extend(players)
        matches[match_id]["teams"].append((match_id, team_id))
    
    # Perform the randomization
    for match_id, match_data in matches.items():
        players = match_data["players"]
        team_keys = match_data["teams"]
        num_teams = len(team_keys)

        # Shuffle players
        random.shuffle(players)

        # Split shuffled players into teams
        team_players = [players[i::num_teams] for i in range(num_teams)]

        # Reassign shuffled players to teams
        for team_key, players in zip(team_keys, team_players):
            randomized_teams_by_match[team_key] = players

    return randomized_teams_by_match

def count_cheaters_after_randomization(teams_by_match, cheaters_ids, num_iterations=20):
    """
    Randomizes teams and counts the number of teams with specific cheater counts.

    Takes:
    - teams_by_match: A dictionary where keys are (match_id, team_id) tuples and values are lists of player account IDs.
    - cheaters: A set of player account IDs that represent cheaters.
    - num_iterations: Number of randomizations to perform.

    Returns:
    - A list of dictionaries where each dictionary contains the counts of teams with
      0, 1, 2, 3, or 4 cheaters for each iteration.
    """
    randomized_results = []

    for _ in range(num_iterations):
        # Randomize the teams
        randomized_teams = randomize_teams(teams_by_match)

        # Count cheaters in the randomized teams
        cheaters_per_team = cheaters.count_cheaters_per_team(randomized_teams, cheaters_ids)

        # Append the result to the list
        randomized_results.append(cheaters_per_team)

    return randomized_results

def flatten_kills(simulation):
    """
    Flattens a simulation of game kill events into a list of tuples.

    Each simulation is a dictionary where the keys are game IDs and the values 
    are lists of kill events. This function transforms the nested structure 
    into a flat list of tuples, where each tuple contains a game ID, the killer's 
    ID, the victim's ID, and the time of the kill.

    Takes:
    - simulation (dict): A dictionary mapping game IDs to lists of kill events, 
                          where each kill event is a tuple (killer, victim, time).

    Returns:
    - list of tuples: A flat list of tuples, where each tuple is of the form 
                      (game_id, killer, victim, time).
    """
    return [(game_id, killer, victim, time)
            for game_id, events in simulation.items()
            for killer, victim, time in events]

def summarize_cheaters_after_killed(simulations, cheaters_data):
    """
    Analyzes the flattened simulation data and counts the number of players who started 
    cheating after being killed by a cheater.

    Takes:
    - simulations (list of tuples): A list of flattened kill events from each simulation.
    - cheaters_data (list of tuples): Data about cheaters, expected by cheaters_after_killed.

    Returns:
    - list of int: A list of counts of players who started cheating after being killed by a cheater.
    """
    results = []

    for flat_kills in simulations:
        
        # Use the cheaters_after_killed function to process the flattened data
        count = cheaters.cheaters_after_killed(flat_kills, cheaters_data)
        results.append(count)

    return results

### Question 3

def create_randomized_world(kills):
    """
    Randomizes the kills and returns the dictionary with the simulation.

    Takes:
    - kills (list): List of kill data to randomize.
    
    Returns:
    - simulated_world (dict): Dictionary storing the randomized kills.
    """

    # Initialize the dictionary inside the function
    simulated_worlds = {}  

    # Initialize the dictionary to group players by game to maintain structure of interactions
    game_players = {} 

    # Group players by game
    for game_id, killer, victim, time in kills:
        if game_id not in game_players:
            game_players[game_id] = []
        game_players[game_id].append((killer, victim, time))

    for game_id, interactions in game_players.items():
        # Extract unique players in the game
        players = set()
        for killer, victim, _ in interactions:
            players.add(killer)
            players.add(victim)

        # Shuffle player IDs
        shuffled_players = list(players)
        random.shuffle(shuffled_players)
        player_map = {original: shuffled for original, shuffled in zip(players, shuffled_players)}

        # Replace player IDs in interactions and include the original time
        for killer, victim, time in interactions:
            if game_id not in simulated_worlds:
                simulated_worlds[game_id] = []
            simulated_worlds[game_id].append((player_map[killer], player_map[victim], time))

    # Return the dictionary containing the simulation
    return simulated_worlds  

def generate_simulated_worlds(kills_data, num_simulations=20):
    """
    Run simulations by randomizing the kills data multiple times.
    
    Takes:
    - kills_data: The data to be randomized in each simulation.
    - num_simulations: Number of simulations to run (default is 20).
    
    Returns:
    - A list of simulated worlds.
    """
    simulations = []
    for _ in range(num_simulations):
        simulated_world = create_randomized_world(kills_data)
        simulations.append(simulated_world)
    return simulations


def summarize_simulation_results(simulations, cheaters_data, observers, filtered_kills_by_cheating_time):
    """
    Analyzes simulated worlds to count the number of players who observed a cheater
    and started cheating.

    Takes:
    - simulations (list of list of tuples): A list of flattened kill events from each simulation.
    - cheaters_data (list of lists): The cheaters data as expected by `filter_cheaters`.
    - observers (dict): A dictionary where the key is match_id and the value is a set of observer_ids.
    - filtered_kills_by_cheating_time (dict): A dictionary where key is match_id and value is a list of tuples
                                               (killer_id, killed_id, kill_time, observed_time) for kills after 
                                               the first observed cheater.

    Returns:
    - list of int: A list of counts from each simulation.
    """
    simulation_results = []

    for flat_kills in simulations:
        # Filter kills based on the observed time
        filtered_kills = cheaters.filter_kills_by_cheating_time(flat_kills, cheaters_data)

        # For each match, find observers using the filtered kills
        observers_in_match = cheaters.find_observers(filtered_kills, cheaters_data)

        # Pass the filtered kills and observers to filter_cheaters
        count = cheaters.filter_cheaters(observers_in_match, filtered_kills, cheaters_data)

        # Store the result
        simulation_results.append(count)
    
    return simulation_results