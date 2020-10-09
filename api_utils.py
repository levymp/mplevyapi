import os
import uuid
import pandas as pd
from pathlib import Path
from datetime import datetime
from pytz import timezone, utc

# Global Directories
_ROOT = Path('/home/michaellevy/data/mbot/')
_LOG = _ROOT.joinpath('log')
_PKL = _ROOT.joinpath('pickle')
_PICKLE = Path('/home/michaellevy/data/mbot/mbot_table.pkl')

def get_time():
    # current time in EST
    date = datetime.now(tz=timezone('US/Eastern'))

    # get directory and file_name formats
    yyyy_mm_dd = date.strftime('%Y_%m_%d')
    hh_mm_ss = date.strftime('%H:%M:%S')

    return [yyyy_mm_dd, hh_mm_ss]

def get_file_info():
    # return file name
    time = get_time()
    
    # yyyy-mm-dd-H:M:S
    base_file_name = time[0] + '_' + time[1]

    # setup result
    payload = {'log': {}, 'pkl_initial': {}, 'pkl_final': {}}

    # New log directory
    NEW_LOG = _LOG.joinpath(time[0])
    NEW_LOG.mkdir(exist_ok=True)
    
    # New pickle directory
    NEW_PKL = _PKL.joinpath(time[0])
    NEW_PKL.mkdir(exist_ok=True)

    # setup log name and path
    payload['log']['name'] = base_file_name + '.log'
    payload['log']['path'] = NEW_LOG.joinpath(payload['log']['name'])
    
    # setup initial pickle name and path
    # this is created in the log directory and then moved to the pickle directory
    payload['pkl_initial']['name'] = base_file_name + '_log' + '.pkl'
    payload['pkl_initial']['path'] = NEW_LOG.joinpath(payload['pkl_initial']['name'])
    
    # setup final pkl name and path
    payload['pkl_final']['name'] = base_file_name + '.pkl'
    payload['pkl_final']['path'] = NEW_PKL.joinpath(payload['pkl_final']['name'])

    return payload

def update_mbot_table(botname, file_info):
    '''Append File Structure Lookup Pandas DataFrame'''
    if not isinstance(botname, str): 
        return -1
    elif not isinstance(file_info, dict):
        return -1
    
    # COLUMNS
    # ['BOT NAME', 'PICKLE NAME', 'PICKLE PATH', 'LOG NAME', 'LOG PATH']
    
    # trim botname
    botname.replace(' ', '')
    
    # append name
    result = []
    known_bots = ['MICHAEL', 'SAM', 'HAMIL', 'XUN']

    if botname.upper() in known_bots:
        result.append(botname.upper())
    else: 
        result.append('-')
    
    # check pickle
    if file_info['pkl_final']['path'].is_file():
        result.append(file_info['pkl_final']['name'])
        result.append(str(file_info['pkl_final']['path'].absolute()))
    else:
        result.extend(['-', '-'])
        
    # check log
    if file_info['log']['path'].is_file():
        result.append(file_info['log']['name'])
        result.append(str(file_info['log']['path'].absolute()))
    else:
        result.extend(['-', '-'])

    # read table
    if _PICKLE.is_file():
        # read pickle and update
        df = pd.read_pickle(_PICKLE)
        # keep track of RunId
        RunId = len(df)
        df.loc[RunId] = result
        # write pickle
        df.to_pickle(_PICKLE)
        file_info['RunId'] = RunId
        file_info['result'] = result
        return 0
    else:
        return -2

def get_file_address(RunId, column):
    df = pd.read_pickle(_PICKLE)
    # check for valid RunId
    if RunId < len(df) and RunId >= 0:
        return Path(df.loc[0]['PICKLE PATH'])
    else:
        return -1




if __name__ == "__main__":
    payload = get_file_info()
    r = update_mbot_table('MICHAEL', payload)
    print(r)

    