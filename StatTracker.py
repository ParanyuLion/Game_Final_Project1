import csv
from pathlib import Path


class StatTracker:
    _instance = None

    @staticmethod
    def get_instance():
        if StatTracker._instance is None:
            StatTracker()
        return StatTracker._instance

    def __init__(self):
        if StatTracker._instance is not None:
            raise Exception("This class is a singleton!")
        StatTracker._instance = self

        self.game_stats_per_min = Path(r'data_record/game_stats_per_min.csv')
        self.game_stats_per_min_fields = ['minutes','level','enemy_defeated_per_min','score_per_min','distance_per_min']

        self.item_bought = Path(r'data_record/item_bought.csv')
        self.item_bought_fields = ['item_name']

        self.enemy_defeated = Path(r'data_record/enemy_defeated.csv')
        self.enemy_defeated_fields = ['enemy_type']

        self.level_complete = Path(r'data_record/level_complete.csv')
        self.level_complete_fields = ['level_complete', 'time_used']

        self._cached_rows = []  # For game_stats_per_min

    def log(self, event_type, value=None, minutes=None, level=None,
            enemy_dead=None, score=None, distance=None, time_used=None):
        if event_type == 'item_bought':
            row = {
                'item_name': value,
            }
            with open(self.item_bought, mode='a', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=self.item_bought_fields)
                writer.writerow(row)
        elif event_type == 'enemy_defeated':
            row = {
                'enemy_type': value,
            }
            with open(self.enemy_defeated, mode='a', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=self.enemy_defeated_fields)
                writer.writerow(row)
        elif event_type == 'level_complete':
            row = {
                'level_complete': value,
                'time_used': time_used
            }
            with open(self.level_complete, mode='a', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=self.level_complete_fields)
                writer.writerow(row)
        else:
            row = {
                'minutes': minutes,
                'level': level,
                'enemy_defeated_per_min': enemy_dead,
                'score_per_min': score,
                'distance_per_min': distance
            }
            with open(self.game_stats_per_min, mode='a', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=self.game_stats_per_min_fields)
                writer.writerow(row)
