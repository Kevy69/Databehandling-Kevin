import pandas as pd

class Load_data:
    olympic_data = None
    
    @classmethod
    def load(cls):
        cls.olympic_data = pd.read_csv("Data/athlete_events.csv")
        
