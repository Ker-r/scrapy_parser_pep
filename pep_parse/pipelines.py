import csv
from collections import defaultdict
from datetime import datetime as dt
from pathlib import Path

DATETIME_FORMAT = '%m-%d-%Y_%H-%M-%S'
DATETIME = dt.now().strftime(DATETIME_FORMAT)

BASE_DIR = Path(__file__).parent.parent
DIR_RESULT = BASE_DIR / 'results'


class PepParsePipeline:

    def open_spider(self, spider):
        self.status_count = defaultdict(int)
        self.total = 0

    def process_item(self, item, spider):
        self.status_count[item['status']] += 1
        self.total += 1
        return item

    def close_spider(self, spider):
        DIR_RESULT.mkdir(exist_ok=True)
        file_status = BASE_DIR / 'results' / f'status_summary_{DATETIME}.csv'
        with open(file_status, mode='w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(('Статус', 'Количество'))
            writer.writerows(self.status_count.items())
            writer.writerow(('Total', self.total))
