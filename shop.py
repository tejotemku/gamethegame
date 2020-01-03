class Shop:
    """
    This is a class of town shop
    """
    def __init__(self):
        """
        This method initiates a shop object
        """
        self._items = {'small potion': 15, 'big potion': 35, 'golden key': 75}

    @property
    def items(self):
        return self._items
