import pandas as pd


class SaosDAO:
    def __init__(self):
        self.data = pd.read_csv('./klauzule.csv')

    def get_category(self, category):
        for _, text in self.data[self.data['Branża'] == category]['Postanowienie wzorca umowy uznane za niedozwolone'].iteritems():
            yield text
