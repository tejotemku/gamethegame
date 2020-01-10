class Shop:
    """
    This is a class of town shop
    """
    def __init__(self):
        """
        This method initiates a shop object
        """
        self._items = {'small potion': 15, 'big potion': 35}

    @property
    def items(self):
        return self._items

    @staticmethod
    def leave_shop():
        print('leave - to leave the shop')

    def __str__(self):
        string = ""
        for i in self.items:
            string += f'{i}: {self.items.get(i)}\n'
        return string[:-2]
