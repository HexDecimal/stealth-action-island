
class Component(object):
    def __init__(self, *args, **kargs):
        self.name = None
        self.entity = None
        super(Component, self).__init__(*args, **kargs)
