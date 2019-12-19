import pandas as pd


class User():
    def __init__(self, id=-1, username="none", users_dataset=pd.DataFrame()):
        self.id = id
        self.username = username
        self.users_dataset = users_dataset
