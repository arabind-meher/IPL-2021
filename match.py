from os.path import join

import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class Match:
    def __init__(self, match_file: str, match_details: pd.Series) -> None:
        path = join('dataset', match_file)

        color_code = {
            'CSK': ['#FFFF3C', '#0081E9'],
            'DC': ['#0000B8', '#EF1B23'],
            'KKR': ['#2E0854', '#B3A123'],
            'MI': ['#004BA0', '#D1AB3E'],
            'PBKS': ['#DCDDDF', '#ED1B24'],
            'RCB': ['#EC1C24', '#2B2A29'],
            'RR': ['#EA1B85', '#254AA5'],
            'SRH': ['#FF822A', '#000000'],
        }

        self.match = pd.read_csv(path)
        self.team_names = [match_details['team_1'], match_details['team_2']]
        self.team_abbreviation = [match_details['team_1_sh'], match_details['team_2_sh']]
        self.team_colors = [color_code[self.team_abbreviation[0]], color_code[self.team_abbreviation[1]]]

    def teams_score(self) -> plt.Figure:
        # total runs for both teams
        teams_run = self.match.groupby('batting_team')[['batsman_run', 'extra_runs', 'total_runs']].sum()

        # plotting pie chart for runs scored
        fig, ax = plt.subplots(1, 2, figsize=(10, 5))

        ax[0].pie(
            teams_run.loc[self.team_names[0]][:2],
            startangle=90,
            wedgeprops=dict(width=.4),
            labels=[f'Batsman ({teams_run.loc[self.team_names[0]][0]})',
                    f'Extras ({teams_run.loc[self.team_names[0]][1]})'],
            colors=self.team_colors[0],
        )

        ax[1].pie(
            teams_run.loc[self.team_names[1]][:2],
            startangle=90,
            wedgeprops=dict(width=.4),
            labels=[f'Batsman ({teams_run.loc[self.team_names[1]][0]})',
                    f'Extras ({teams_run.loc[self.team_names[1]][1]})'],
            colors=self.team_colors[1],
        )

        ax[0].text(
            0., 0.,
            f"{self.team_abbreviation[0]}: {teams_run.loc[self.team_names[0]][2]}",
            horizontalalignment='center',
            verticalalignment='center',
            size=15
        )

        ax[1].text(
            0., 0.,
            f"{self.team_abbreviation[1]}: {teams_run.loc[self.team_names[1]][2]}",
            horizontalalignment='center',
            verticalalignment='center',
            size=15
        )

        ax[0].axis('equal')
        ax[1].axis('equal')

        ax[0].set_title('First Innings')
        ax[1].set_title('Second Innings')
        fig.suptitle(
            f'{self.team_names[0]} ({self.team_abbreviation[0]}) vs {self.team_names[1]} ({self.team_abbreviation[1]})')

        return fig

    def get_teams_runs_per_over(self) -> tuple:
        # team 1 runs per over & cumulative score
        team_1_runs_per_over = self.match[self.match['inning'] == '1st innings'].groupby(
            ['inning', 'batting_team', pd.cut(self.match['ball'], np.arange(21))]
        ).agg(
            runs=('total_runs', 'sum')
        ).reset_index([0, 1], drop=True).reset_index()

        team_1_runs_per_over['cumm_sum'] = team_1_runs_per_over['runs'].cumsum()

        # team 2 runs per over & cumulative score
        team_2_runs_per_over = self.match[self.match['inning'] == '2nd innings'].groupby(
            ['inning', 'batting_team', pd.cut(self.match['ball'], np.arange(21))]
        ).agg(
            runs=('total_runs', 'sum')
        ).reset_index([0, 1], drop=True).reset_index()

        team_2_runs_per_over['cumm_sum'] = team_2_runs_per_over['runs'].cumsum()

        return team_1_runs_per_over, team_2_runs_per_over

    def runs_per_over_bar(self) -> plt.Figure:
        team_1_runs_per_over, team_2_runs_per_over = self.get_teams_runs_per_over()

        # plotting bar graph for runs per over
        fig, ax = plt.subplots(figsize=(15, 8))

        width = .25
        x = np.arange(1, 21)

        ax.bar(
            x - width / 2,
            team_1_runs_per_over['runs'],
            width=width,
            color=self.team_colors[0][0],
            label=self.team_names[0]
        )

        ax.bar(
            x + width / 2,
            team_2_runs_per_over['runs'],
            width=width,
            color=self.team_colors[1][0],
            label=self.team_names[1]
        )

        ax.set_title(
            f'{self.team_names[0]} ({self.team_abbreviation[0]}) vs {self.team_names[1]} ({self.team_abbreviation[1]})',
            size=15)
        ax.set_xlabel('Overs', size=15)
        ax.set_ylabel('Runs', size=15)
        ax.set_xticks(x)

        for score in ax.containers:
            ax.bar_label(score, size=10, padding=5)

        ax.legend(prop={'size': 10})
        
        return fig

    def runs_per_over_line(self) -> plt.Figure:
        team_1_runs_per_over, team_2_runs_per_over = self.get_teams_runs_per_over()

        fig, ax = plt.subplots(figsize=(15, 8))

        ax.plot(
            np.arange(1, 21),
            team_1_runs_per_over['cumm_sum'],
            label=self.team_names[0],
            color=self.team_colors[0][0]
        )

        ax.scatter(
            np.arange(1, 21),
            team_1_runs_per_over['cumm_sum'],
            color=self.team_colors[0][0]
        )

        ax.plot(
            np.arange(1, 21),
            team_2_runs_per_over['cumm_sum'],
            label=self.team_names[1],
            color=self.team_colors[1][0]
        )

        ax.scatter(
            np.arange(1, 21),
            team_2_runs_per_over['cumm_sum'],
            color=self.team_colors[1][0]
        )

        ax.set_title(
            f'{self.team_names[0]} ({self.team_abbreviation[0]}) vs {self.team_names[1]} ({self.team_abbreviation[1]})',
            size=15)
        ax.set_xlabel('Overs', size=15)
        ax.set_ylabel('Runs', size=15)
        ax.set_xticks(np.arange(1, 21))

        for score in ax.containers:
            ax.bar_label(score, size=10, padding=5)

        ax.legend(prop={'size': 10})

        return fig

    def teams_batting_score(self, team) -> tuple:
        # team 1 batsmen score
        team_1_batsmen = self.match[self.match['inning'] == '1st innings'].groupby(
            ['batting_team', 'batsman'],
        ).agg(
            runs=('batsman_run', 'sum'),
            balls=('batsman_run', 'count')
        ).reset_index(level=0, drop=True).reset_index(level=0).sort_values(['runs', 'balls'], ascending=[False, True])

        # team 2 batsmen score
        team_2_batsmen = self.match[self.match['inning'] == '2nd innings'].groupby(
            ['batting_team', 'batsman'],
        ).agg(
            runs=('batsman_run', 'sum'),
            balls=('batsman_run', 'count')
        ).reset_index(level=0, drop=True).reset_index(level=0).sort_values(['runs', 'balls'], ascending=[False, True])

        max_score = max(team_1_batsmen['runs'].max(), team_2_batsmen['runs'].max())

        start = 0
        end = int(math.ceil(max_score / 10)) * 10
        step = ((end - start) // 10) + 1

        if team == 1:
            return team_1_batsmen, start, end, step
        elif team == 2:
            return team_2_batsmen, start, end, step

    def team_1_batting_score(self) -> plt.Figure:
        team_1_batsmen, start, end, step = self.teams_batting_score(1)

        fig, ax = plt.subplots(figsize=(15, 8))

        width = .25
        x = np.arange(len(team_1_batsmen))

        ax.bar(
            x - width / 2,
            team_1_batsmen['runs'],
            width=width,
            color=self.team_colors[0][0],
            label='Runs'
        )

        ax.bar(
            x + width / 2,
            team_1_batsmen['balls'],
            width=width,
            color=self.team_colors[0][1],
            label='Balls'
        )

        for score in ax.containers:
            ax.bar_label(score, size=12, padding=5)

        ax.set_title(f'{self.team_names[0]} ({self.team_abbreviation[0]})', size=15)

        ax.set_xlabel('Players', size=12)

        ax.set_xticks(
            np.arange(12),
            team_1_batsmen['batsman'].tolist() + ([''] * (12 - len(team_1_batsmen['batsman']))),
            size=10,
            rotation=45
        )

        ax.set_yticks(np.linspace(start, end, step))

        ax.legend(prop={'size': 10})

        return fig

    def team_2_batting_score(self) -> plt.Figure:
        team_2_batsmen, start, end, step = self.teams_batting_score(2)

        fig, ax = plt.subplots(figsize=(15, 8))

        width = .25
        x = np.arange(len(team_2_batsmen))

        ax.bar(
            x - width / 2,
            team_2_batsmen['runs'],
            width=width,
            color=self.team_colors[1][0],
            label='Runs'
        )

        ax.bar(
            x + width / 2,
            team_2_batsmen['balls'],
            width=width,
            color=self.team_colors[1][1],
            label='Balls'
        )

        for score in ax.containers:
            ax.bar_label(score, size=12, padding=5)

        ax.set_title(f'{self.team_names[1]} ({self.team_abbreviation[1]})', size=15)

        ax.set_xlabel('Players', size=12)

        ax.set_xticks(
            np.arange(12),
            team_2_batsmen['batsman'].tolist() + ([''] * (12 - len(team_2_batsmen['batsman']))),
            size=10,
            rotation=45
        )

        ax.set_yticks(np.linspace(start, end, step))

        ax.legend(prop={'size': 10})

        return fig
