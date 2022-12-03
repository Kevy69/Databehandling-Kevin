import plotly.express as px
from Load_data import Load_data as ld


class Data:
    
    sports3 = ['Basketball', 'Football', 'Ice Hockey']
    
    olympic_data_sports = None
    
    olympic_data_sports_unique_players = None
    
    olympic_data_finland = None
    olympic_data_finland_with_medals = None
    olympic_data_finland_unique_players = None
    
    @classmethod
    def initialize(cls):
        
        cls.olympic_data_sports = ld.olympic_data.query(f"Sport == '{Data.sports3[0]}' | Sport == '{Data.sports3[1]}' | Sport == '{Data.sports3[2]}'")
        
        cls.olympic_data_sports_unique_players = Data.olympic_data_sports.drop_duplicates("Name")
        
        cls.olympic_data_finland = ld.olympic_data.loc[ld.olympic_data['NOC'] == 'FIN']
        cls.olympic_data_finland_with_medals = cls.olympic_data_finland[cls.olympic_data_finland['Medal'].notna()]
        
        # Remove duplicate players (by looking at name hash)
        cls.olympic_data_finland_unique_players = cls.olympic_data_finland.drop_duplicates('Name')


class General:
    @staticmethod
    def medal_distribution_sports(country: str):

        # drop all rows that dont involve our sport
        olympic_data_sport = ld.olympic_data.drop(ld.olympic_data[ld.olympic_data['Sport'] != country].index)
        
        # get all medals (remove nan's)
        olympic_data_sport_with_medals = olympic_data_sport[olympic_data_sport['Medal'].notna()]
        
        # Group by 'NOC' and count all medals
        medals_per_country_sport = olympic_data_sport_with_medals.groupby('NOC')['Medal'].count()

        medals_per_country_sport = medals_per_country_sport.sort_values(ascending=False)

        fig = px.bar(
            x=medals_per_country_sport.index,
            y=medals_per_country_sport,
            title=f"Medal distribution across countries in {country.lower()}",
            labels={
                'x': '',
                'y': 'Medals'
            }
        )

        # plotly.graph_objs._figure.Figure

        return fig
    
    @staticmethod
    def age_distribution_3sports():
        fig = px.histogram(
            data_frame=Data.olympic_data_sports,
            color='Sport',
            x="Age",
            title="Age distribution across sports"
        )

        return fig
    
    @staticmethod
    def height_distribution_3sports():
        # Take out height over 195, drop duplicate athletes and plot graph
        olympic_data_sports_height = Data.olympic_data_sports_unique_players.query('Height > 195')
        
        fig = px.histogram(
            data_frame=olympic_data_sports_height,
            color='Sport',
            x="Sport",
            y = "Height",
            title="Height distribution across sports"
        )

        return fig
    
    @staticmethod
    def weight_distribution_3sports():
        # Take out height over 195, drop duplicate athletes and plot graph
        olympic_data_sports_height = Data.olympic_data_sports_unique_players.query('Weight > 110')
        
        fig = px.histogram(
            data_frame=olympic_data_sports_height,
            color='Sport',
            x="Sport",
            y = "Weight",
            title="Weight distribution across sports"
        )

        return fig


class Finland:
    
    @staticmethod
    def medal_distribution_sports_finland():

        # Filter the rows into groups of sports, than sum the "Medals" column for each given sport
        medals_per_finland_sport = Data.olympic_data_finland_with_medals.groupby('Sport')['Medal'].count()

        medals_per_finland_sport = medals_per_finland_sport.sort_values(ascending=False)

        # Take the top 5 sports with most medals scored
        medals_per_sport_top5_finland = medals_per_finland_sport[:5]

        fig = px.bar(
            x=medals_per_sport_top5_finland.index,
            y=medals_per_sport_top5_finland,
            title="Medal distribution across the olympic sports in finland",
            labels={
                'x': '',
                'y': 'Medals'
            }
        )
        
        return fig
    
    
    @staticmethod
    def medal_distribution_olympics_finland():
        # Filter the rows into groups of games, than sum the "Medals" column for each given game
        medals_per_os = Data.olympic_data_finland_with_medals.groupby('Games')['Medal'].count()

        medals_per_os.index = medals_per_os.index.sort_values()

        fig = px.bar(
            x=medals_per_os.index,
            y=medals_per_os,
            title="Medal distribution across the olympic games in finland",
            labels={
                'x': '',
                'y': 'Medals'
            }
        )

        return fig
    
    
    @staticmethod
    def age_distribution_olympics_finland():
        fig = px.histogram(
            data_frame=Data.olympic_data_finland,
            x="Age",
            title="Age distribution across the OS contenders"
        )

        return fig
    
    @staticmethod
    def height_distribution_olympics_finland():
        fig = px.histogram(
            data_frame=Data.olympic_data_finland_unique_players,
            x="Height",
            title="height distribution"
        )

        return fig
    
    @staticmethod
    def weight_distribution_olympics_finland():
        # Get a series of the value counts of the ages
        olympic_data_finland_weights = Data.olympic_data_finland_unique_players['Weight'].value_counts()

        olympic_data_finland_weights = olympic_data_finland_weights.sort_values(ascending=False)


        fig = px.histogram(
            x=olympic_data_finland_weights.index,
            y=olympic_data_finland_weights,
            title="Weight distribution",
            
            labels={
                'x': 'Kg',
                'y': 'Number of people'
            }
        )

        fig.update_layout(yaxis_title="Number of people")
        return fig
    
    @staticmethod
    def medal_distribution_finland_players():
        medal_holders = Data.olympic_data_finland_with_medals
        medal_holders['Count_Of_Medals'] = 1
        medal_holders_fin = medal_holders[medal_holders["NOC"] == "FIN"]
        medal_holders_fin.head(1)
        
        highest_medals_fin = medal_holders_fin[['Name', 'Year', 'Team', 'Count_Of_Medals']].groupby(['Name','Year','Team']).sum().sort_values('Count_Of_Medals', ascending=False)

        highest_medals_fin2 = highest_medals_fin.groupby(['Name','Team']).sum().sort_values('Count_Of_Medals', ascending=False).head(10)
        highest_medals_fin2.reset_index(inplace=True)
        
        fig = px.pie(highest_medals_fin2, values='Count_Of_Medals', names='Name', title='Highest Medal Winners Finland')
        return fig
        
