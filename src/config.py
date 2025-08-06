class Config():
    def __init__(self, db_url, db_auth_token=None, verbose=True):
        self.db_url = db_url
        self.db_auth_token = db_auth_token
        self.verbose = verbose

