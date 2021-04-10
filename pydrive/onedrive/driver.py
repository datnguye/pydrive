import cloudsync
import os
from dotenv import load_dotenv
import ast

def upload(rtoken, atoken, dot_config=None):
    # CONFIG
    if dot_config is not None:
        load_dotenv(dotenv_path=dot_config)
    else:
        load_dotenv(dotenv_path=f'{os.path.dirname(os.path.realpath(__file__))}/.driver')

    LOCAL_ROOT = os.getenv('LOCAL_ROOT')
    REMOTE_ROOT = os.getenv('REMOTE_ROOT')
    FILES_MAPPING  = ast.literal_eval(os.getenv('FILES_MAPPING') or "[]")

    print(f'[onedrive] Upload files from [{LOCAL_ROOT}] to OneDrive at [{REMOTE_ROOT}]')


    # REMOTE
    print(f'[onedrive]      Connecting to remote...')
    oauth_config = cloudsync.command.utils.generic_oauth_config('onedrive')
    remote = cloudsync.create_provider('onedrive', oauth_config=oauth_config)

    creds = {'refresh_token': rtoken, 'access_token': atoken}
    if not rtoken or not atoken:
        creds = prov.authenticate()
        print(creds) #save creds somewhere
        
    remote.connect(creds)
    print(f'[onedrive]           Connected')


    # UPLOAD
    print(f'[onedrive]      Uploading...')
    for file in FILES_MAPPING:        
        print(f'[onedrive]      File mapping: {file}')
        local_file_like = open(f'{LOCAL_ROOT}/{file[0]}', 'rb')
        remote_file = remote.info_path(f'{REMOTE_ROOT}/{file[1]}')
        if remote_file is None:
            remote.create(path=f'{REMOTE_ROOT}/{file[1]}', file_like=local_file_like)
        else:
            remote.upload(remote_file.oid, local_file_like)
        print(f'[onedrive]          Done.')


    # DISCONNECT
    remote.disconnect()
    print(f'[onedrive] Finished. Disconected!')