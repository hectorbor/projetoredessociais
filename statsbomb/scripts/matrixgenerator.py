import os 
import json
import ast
import pandas as pd
from datetime import timedelta
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

class Substitution:
    def __init__(self, time, teamid,old_playerid, new_playerid):
        self.time = time
        self.teamid=teamid
        self.old_playerid = old_playerid
        self.new_playerid = new_playerid

class Shift:
    def __init__(self, time, teamid, players):
        self.time = time
        self.teamid = teamid
        self.players = players

class Node:
    def __init__(self, playerid, nodeid):
        self.playerid = playerid
        self.nodeid=nodeid

class Team:
    def __init__(self, team, teamid, players):
        self.team = team
        self.teamid = teamid
        self.players=players
        self.matrices=[]

class Start:
    def __init__(self, name, age):
        self.name = name
        self.age = age

def matrixGenerator(path):

    file_path = path

    originaldf = pd.read_csv(file_path)

    passdf=originaldf.copy()
    startdf=originaldf.copy()
    subsdf=originaldf.copy()
    shiftdf=originaldf.copy()

    passdf = originaldf[originaldf['type'] == 'Pass']
    startdf = originaldf[originaldf['type'] == 'Starting XI']
    subsdf = originaldf[originaldf['type'] == 'Substitution']
    shiftdf = originaldf[originaldf['type'] == 'Tactical Shift']

    subslist=[]

    for index, row in subsdf.iterrows():
        minutesaux=int(row['minute'])%60
        #print("minutos "+str(row['minute']))
        hoursaux=int(row['minute'])//60
        #print("horas "+str(int(row['minute'])/60))
        secondsaux  =int(row['second'])
        time=timedelta(hours=hoursaux,minutes=minutesaux,seconds=secondsaux)
        old_playerid=int(row['player_id'])
        new_playerid=int(row['substitution_replacement_id'])
        teamid=int(row['team_id'])
        #print(time)
        auxobj=Substitution(time,teamid,old_playerid,new_playerid)
        #print(str(time)+' '+str(old_playerid)+' '+str(new_playerid))
        subslist.append(auxobj)

    shiftslist=[]

    for index, row in shiftdf.iterrows():
        minutesaux=int(row['minute'])%60
        #print("minutos "+str(row['minute']))
        hoursaux=int(row['minute'])//60
        #print("horas "+str(int(row['minute'])/60))
        secondsaux=int(row['second'])
        time=timedelta(hours=hoursaux,minutes=minutesaux,seconds=secondsaux)
        teamid=int(row['team_id'])
        jsontactics = ast.literal_eval(str(row['tactics']))
        jsonplayers=jsontactics['lineup']
        playersshift=[]
        playercount=1
        for item in jsonplayers:
            itemplayerid=item['player']['id']
            #print(itemplayerid)
            playersshift.append(Node(itemplayerid,playercount))
            playercount+=1
        auxobj=Shift(time,teamid,playersshift)
        shiftslist.append(auxobj)

    #print(len(startdf))
    team1row=startdf.iloc[0]
    team1name=str(team1row['team'])
    team1id=int(team1row['team_id'])
    team1jsontactics = ast.literal_eval(str(team1row['tactics']))
    team1jsonplayers=team1jsontactics['lineup']
    team1playersstart=[]
    playercount=1
    for item in team1jsonplayers:
        itemplayerid=item['player']['id']
        #print(itemplayerid)
        team1playersstart.append(Node(itemplayerid,playercount))
        playercount+=1
    team1=Team(team1name,team1id,team1playersstart)

    team2row=startdf.iloc[1]
    team2name=str(team2row['team'])
    team2id=int(team2row['team_id'])
    team2jsontactics = ast.literal_eval(str(team2row['tactics']))
    team2jsonplayers=team2jsontactics['lineup']
    team2playersstart=[]
    playercount=1
    for item in team2jsonplayers:
        itemplayerid=item['player']['id']
        #print(itemplayerid)
        team2playersstart.append(Node(itemplayerid,playercount))
        playercount+=1
    team2=Team(team2name,team2id,team2playersstart) 

    currentmatrix = [[0 for _ in range(11)] for _ in range(11)]

    currentteamid=int(passdf.iloc[0]['team_id'])
    currentpossession=int(passdf.iloc[0]['possession'])

    # print("team1")
    # for i, item in enumerate(team1.players):
    #     print(str(item.playerid)+" "+str(item.nodeid))
    # print("team2")
    # for i, item in enumerate(team2.players):
    #     print(str(item.playerid)+" "+str(item.nodeid))

    for index, row in passdf.iterrows():
        minutesaux=int(row['minute'])%60
        hoursaux=int(row['minute'])//60
        secondsaux=int(row['second'])
        time=timedelta(hours=hoursaux,minutes=minutesaux,seconds=secondsaux)
        while(subslist and time>subslist[0].time):
            #print("playersub con tiempo de pase: "+str(time)+" y tiempo de sub: "+str(subslist[0].time)+" entra "+str(subslist[0].old_playerid)+" sale "+str(subslist[0].new_playerid))
            subaux=subslist.pop(0)
            if(team1.teamid==subaux.teamid):
                for i, item in enumerate(team1.players):
                    if item.playerid == subaux.old_playerid:
                        team1.players[i].playerid=subaux.new_playerid
                        break
                # print("team1")
                # for i, item in enumerate(team1.players):
                #     print(str(item.playerid)+" "+str(item.nodeid))
            else:
                for i, item in enumerate(team2.players):
                    if item.playerid == subaux.old_playerid:
                        team2.players[i].playerid=subaux.new_playerid
                        break
                # print("team2")
                # for i, item in enumerate(team2.players):
                #     print(str(item.playerid)+" "+str(item.nodeid))
        while( shiftslist and time>shiftslist[0].time):
            #print("playershift con equipo "+ str(shiftslist[0].teamid))
            shiftaux=shiftslist.pop(0)
            if(team1.teamid==shiftaux.teamid):
                team1.players=shiftaux.players
            else:
                team2.players=shiftaux.players

        if(int(row['possession'])!=currentpossession):
            #print('changeinpos')
            if(team1.teamid==currentteamid):
                team1.matrices.append(currentmatrix)
                currentmatrix = [[0 for _ in range(11)] for _ in range(11)]
                currentteamid=int(row['team_id'])
                currentpossession=int(row['possession'])
            else:
                team2.matrices.append(currentmatrix)
                currentmatrix = [[0 for _ in range(11)] for _ in range(11)]
                currentteamid=int(row['team_id'])
                currentpossession=int(row['possession'])

        if(pd.isna(row['pass_outcome'])):
            #print("id equipo 1: "+str(team1.teamid)+" id actual: "+str(currentteamid))
            if(team1.teamid==currentteamid):
                indexplayer=-1
                cont=0
                for item in team1.players:
                    #print("jugador de la lista: "+str(item.playerid)+" y jugador del pase: "+str(int(row['player_id']))+" con longitud de lista "+str(len(team1.players)))
                    if item.playerid == int(row['player_id']):
                        indexplayer=cont
                        break
                    cont+=1
                indexreceiver=-1
                cont=0
                for item in team1.players:
                    if item.playerid == int(row['pass_recipient_id']):
                        indexreceiver=cont
                        break
                    cont+=1
                #print("ocurre1 con indexplayer="+str(indexplayer)+" "+str(team1.players[indexplayer].nodeid)+" y indexreceiver="+str(indexreceiver)+" con jugador: "+str(int(row['player_id']))+" y receptor: "+str(int(row['pass_recipient_id'])))
                if(indexplayer >=0 and indexreceiver >= 0):
                    currentmatrix[(team1.players[indexplayer].nodeid)-1][(team1.players[indexreceiver].nodeid)-1]+=1
            else:
                indexplayer=-1
                #print(team2.players[0].playerid)
                cont=0
                for item in team2.players:
                    #print("jugador de la lista: "+str(item.playerid)+" y jugador del pase: "+str(int(row['player_id']))+" con longitud de lista "+str(len(team2.players)))
                    if item.playerid == int(row['player_id']):
                        indexplayer=cont
                        break
                    cont+=1
                indexreceiver=-1
                cont=0
                for item in team2.players:
                    if item.playerid == int(row['pass_recipient_id']):
                        indexreceiver=cont
                        break  
                    cont+=1
                #print("ocurre2con indexplayer="+str(indexplayer)+" "+str(team2.players[indexplayer].nodeid)+" y indexreceiver="+str(indexreceiver)+" con jugador: "+str(int(row['player_id'])))
                if(indexplayer >=0 and indexreceiver >= 0):
                    currentmatrix[(team2.players[indexplayer].nodeid)-1][(team2.players[indexreceiver].nodeid)-1]+=1

    #print(team2.matrices[2])

    resgraph1= [[0 for _ in range(11)] for _ in range(11)]

    for matrix in team1.matrices:
        for i in range(11):
            for j in range(11):
                resgraph1[i][j] += matrix[i][j]

    resgraph2= [[0 for _ in range(11)] for _ in range(11)]

    for matrix in team2.matrices:
        for i in range(11):
            for j in range(11):
                resgraph2[i][j] += matrix[i][j]

    return team1.team,team2.team,resgraph1,resgraph2
    # print(exgrapM)
    # players = ['GK', 'LB', 'CB1', 'CB2', 'RB', 'LM', 'CM', 'RM', 'LW', 'ST', 'RW']
    # # Create a graph from the adjacency matrix
    # G = nx.from_numpy_array(np.array(exgrapM))
    # G = nx.relabel_nodes(G, dict(enumerate(players)))

    # positions = {
    #     'GK': (0, 0),
    #     'LB': (-3, 1),
    #     'CB1': (-1, 1),
    #     'CB2': (1, 1),
    #     'RB': (3, 1),
    #     'LM': (-2, 3),
    #     'CM': (0, 3),
    #     'RM': (2, 3),
    #     'LW': (-3, 5),
    #     'ST': (0, 5),
    #     'RW': (3, 5)
    # }

    # degrees = dict(G.degree())
    # print("Degrees:", degrees)  # Check degrees to understand distribution

    # min_size = 500
    # max_size = 2000

    # degree_values = np.array(list(degrees.values()))
    # # To avoid log(0), we add 1
    # log_degrees = np.log1p(degree_values)

    # # Normalize log degrees to range [0, 1]
    # normalized_log_degrees = (log_degrees - log_degrees.min()) / (log_degrees.max() - log_degrees.min())

    # # Apply to size range
    # node_sizes = min_size + normalized_log_degrees * (max_size - min_size)


    # # Color nodes based on degree (for added visual clarity)
    # node_colors = [degrees[node] for node in G.nodes()]

    # plt.figure(figsize=(10, 6))
    # nx.draw(
    #     G,
    #     pos=positions,
    #     with_labels=True,
    #     node_color=node_colors,
    #     cmap=plt.cm.plasma,
    #     node_size=node_sizes,
    #     font_weight='bold',
    #     edge_color='gray'
    # )
    # plt.gca().invert_yaxis()
    # plt.title("4-3-3 Soccer Formation (Node Size & Color = Degree)")
    # plt.axis('off')
    # plt.show()



