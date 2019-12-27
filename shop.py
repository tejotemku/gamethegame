class Shop:
    def __init__(self):
        self._items = {'small potion': 15, 'big potion': 35, 'golden key': 75}

    @property
    def items(self):
        return self._items
