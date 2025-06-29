from datetime import datetime

# Get cheaters data 
def get_cheaters_data(fname):

    """
    Function to read the cheaters.txt file 
    
    Takes the name of a file and the number of columns as an argument.
    Returns the data split by line, and with the specified number of columns. 
    
    """
    
    data = []
    
    with open(fname, 'r') as f: 
        f.readline()
        for line in f:
            player_acc_id, cheating_start_date, banned_date = line.strip().split('\t')
            data.append([player_acc_id, 
                        datetime.strptime(cheating_start_date, "%Y-%m-%d"), 
                        datetime.strptime(banned_date, "%Y-%m-%d")
                        ])
    return data

# Get team data 
def get_team_data(fname):
    """
    Function to read the teams.txt file

    Takes the name of the file.
    Returns the data split by line, and with the specified number of columns. 
    """

    data = []
    
    with open(fname, 'r') as f: 
        f.readline()
        for line in f.readlines():
            match_id, player_acc_id, team_id = line.strip().split('\t')
            data.append([match_id, player_acc_id, team_id
                        ])
    return data

# Get kills data
def get_kills_data(fname):
    """
    Function to read the kills.txt file

    Takes the name of a file as an argument.
    Returns the data split by line, and with the specified columns.
    """

    data = []
    
    with open(fname, 'r') as f: 
        f.readline()
        for line in f.readlines():
            match_id, killer_acc_id, killed_acc_id, kill_time = line.strip().split('\t')
            data.append([match_id, killer_acc_id, killed_acc_id,
                          datetime.strptime(kill_time, "%Y-%m-%d %H:%M:%S.%f")
                        ])
    return data