from kivy.storage.jsonstore import JsonStore
from kivy.logger import Logger
import json
import datetime


class RoundRecord(object):
    store_name = 'round.json'

    def __init__(self,
                 personal_id,
                 opp_name,
                 opp_id,
                 deck_name,
                 agenda_points,
                 outcome,
                 victory_type,
                 **kwargs):

        self.personal_id   = personal_id
        self.opp_name      = opp_name
        self.opp_id        = opp_id
        self.deck_name     = deck_name
        self.agenda_points = agenda_points
        self.outcome       = outcome
        self.victory_type  = victory_type
        if not kwargs.get('date'):
            self.date      = datetime.datetime.now()
        else:
            self.date      = kwargs.get('date')
            del kwargs['date']
        self.extras = dict()
        for k, v in kwargs.iteritems():
            self.extras[k] = v

    @classmethod
    def initialize_store(cls):
        store = JsonStore(cls.store_name)
        Logger.info('creating store.')
        return store

    def save(self):
        store = self.initialize_store()
        if not store.exists(key=self.date):
            store.put(str(self.date),
                      personal_id=self.personal_id,
                      opponent_name=self.opp_name,
                      opponent_id=self.opp_id,
                      deck_name=self.deck_name,
                      agenda_points=self.agenda_points,
                      outcome=self.outcome,
                      victory_type=self.victory_type,
                      date=str(self.date.date())
                      )

