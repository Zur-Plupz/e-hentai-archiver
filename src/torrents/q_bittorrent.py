from qbittorrentapi import Client

def get_client_session(url:str, username:str, password:str, verify:bool=False):
  qb = Client(url, username=username, password=password, VERIFY_WEBUI_CERTIFICATE= verify)
  qb.auth_log_in()

  return qb