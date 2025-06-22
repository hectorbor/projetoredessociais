from statsbombpy import sb
import os 
import pandas as pd

comps=sb.competitions()
folder_path = '../dataframes'

file_name_comps='competitions.csv'
full_path_comps=os.path.join(folder_path, file_name_comps)

comps.to_csv(full_path_comps,index=False)

copaAmerica=sb.matches(competition_id=223,season_id=282)

file_name_copaAmerica='copaAmerica.csv'
full_path_copaAmerica=os.path.join(folder_path,file_name_copaAmerica)

copaAmerica.to_csv(full_path_copaAmerica,index=False)

for index, row in copaAmerica.iterrows():

    game=sb.events(match_id=row["match_id"])
    lineuphome=sb.lineups(match_id=row["match_id"])[row['home_team']]
    lineupaway=sb.lineups(match_id=row["match_id"])[row['away_team']]
    
    file_name_game='game'+str(row["match_id"])+'.csv'
    file_name_lineuphome='lineup'+str(row["match_id"])+'_'+'home'+row["home_team"]+'.csv'
    file_name_lineupaway='lineup'+str(row["match_id"])+'_'+'away'+row["away_team"]+'.csv'
    full_path_game=os.path.join(folder_path, file_name_game)
    full_path_lineuphome=os.path.join(folder_path, file_name_lineuphome)
    full_path_lineupaway=os.path.join(folder_path, file_name_lineupaway)

    game.to_csv(full_path_game,index=False )
    lineuphome.to_csv(full_path_lineuphome,index=False)
    lineupaway.to_csv(full_path_lineupaway,index=False)

