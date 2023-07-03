import pandas as pd


def update_player_df(shot_df, player_game_df):

    if shot_df.loc[0, 'shot_made'] == 'Miss':
        print('Knows its a miss')
        if shot_df.loc[0, 'shot_type'] == '2pt Field Goal':
            player_game_df.loc[player_game_df['Shot Type']
                               == 'shoot2FGA', 'PNR BH'] = 1

            return player_game_df
