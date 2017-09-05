from kivy.network.urlrequest import UrlRequest
from kivy.storage.jsonstore import JsonStore
import json
from kivy.logger import Logger


class IdentityStore(object):
    store_name = 'identity.store'
    url = 'https://netrunnerdb.com/api/2.0/public/cards'

    def __init__(self):
        self.ids = None

    def update(self):
        UrlRequest(self.url, self.url_callback, on_progress=self.progress_callback)

    def progress_callback(self, request, current_size, total_size):
        percent = int((float(current_size) / total_size) * 100)
        Logger.info('Downloading {p}'.format(p=percent))


    def url_callback(self, request, data):
        data = json.loads(data.decode()) if not isinstance(data, dict) else data
        data = data.get('data', {})
        self.store = self.initialize_store()
        for card in data:
            if card.get('type_code') == 'identity':
                Logger.info('Card: {c}'.format(c=card.get('title').encode('ascii', 'ignore').decode('ascii')))
                self.id_drop(card)

    def id_drop(self, card):
        if not self.store.exists(card.get('code')):
            self.store.put(
                card.get('code'),
                title=card.get('title'),
                text=card.get('text'),
                flavor=card.get('flavor'),
                side_code=card.get('side_code'),
                minimum_deck_size=card.get('minimum_deck_size'),
                faction_code=card.get('faction_code'),
                influence_limit=card.get('influence_limit'),
                    )

    @classmethod
    def initialize_store(cls):
        store = JsonStore(cls.store_name)
        Logger.info('creating store.')
        return store

    @classmethod
    def get_id_list(cls, side_code, store=None):
        if not store: store = cls.initialize_store()
        retval = list()
        for key in store.keys():
            id = store.get(key=key)
            if id.get('side_code') == side_code:
                retval.append(str(id.get('title').encode('ascii', 'ignore').decode('ascii')))
        return retval

    def serialize(self):
        pass

    def save(self):
        pass

    @classmethod
    def winning_agenda_points(cls, id1, id2):
        return 7

if __name__ == '__main__':
    i = IdentityStore()
    i.update()