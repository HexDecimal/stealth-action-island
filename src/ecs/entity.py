
class Entity(object):
    _RESERVED_ATTRIBUTES = ('parent', 'children', 'components')
    def __init__(self, components=(), children=(), **kargs):
        self.parent = None
        self.children = []
        self.components = []
        for component in components:
            self.add_component(component)
        for name, value in kargs.items():
            self.__setattr__(name, value)
        for child in children:
            self.add_child(child)

    def __repr__(self):
        return "%s(components=%r, children=%r, %s)" % (
            self.__class__.__name__,
            tuple(c for c in self.components if not c.name),
            tuple(self.children),
            ', '.join('%s=%r' % (c.name, c)
                      for c in self.components if c.name),
            )

    @property
    def root(self):
        """Return the root entity."""
        return self.parent.root if self.parent else self

    @property
    def all_children(self):
        """Iterate over all child entities recursively."""
        for child in self.children:
            yield from child.all_children
            yield child

    def add_child(self, entity):
        """Add a child entity to this instance."""
        assert entity not in self.children
        assert entity.parent is None
        self.children.append(entity)
        entity.parent = self
        self.propagate_up('ev_entity_added', entity)
        entity.propagate_down('ev_entity_connected', entity)

        for component in entity.components:
            self.propagate_up('ev_component_added', component)
        for child in entity.all_children:
            self.propagate_up('ev_entity_added', child)
            for component in child.components:
                self.propagate_up('ev_component_added', component)

    def remove_child(self, entity):
        """Remove a child entity from this instance."""
        for child in entity.all_children:
            self.propagate_up('ev_entity_removed', child)
            for component in child.components:
                self.propagate_up('ev_component_removed', component)

        self.propagate_up('ev_entity_removed', entity)
        entity.propagate_down('ev_entity_disconnected', entity)
        self.children.remove(entity)
        entity.parent = None

    def add_component(self, component):
        """Add a component to this instance."""
        assert component not in self.components
        assert component.entity is None
        component.entity = self
        self.components.append(component)
        self.propagate_up('ev_component_added', component)

    def remove_component(self, component):
        """Remove a component from this instance."""
        self.propagate_up('ev__component_removed', component)
        if component.name:
            object.__delattr__(self, component.name)
            component.name = None
        component.entity = None
        self.components.remove(component)

    def propagate_up(self, ev_name, *args, **kargs):
        """Visit the function named `ev_name` in self and all parent entities.
        """
        if self.parent:
            self.parent.propagate_up(ev_name, *args, **kargs)
        for component in self.components:
            func = getattr(component, ev_name, None)
            if func:
                func(*args, **kargs)

    def propagate_down(self, ev_name, *args, **kargs):
        """Visit the function named `ev_name` in self and all child entities.
        """
        for component in self.components:
            func = getattr(component, ev_name, None)
            if func:
                func(*args, **kargs)
        for entity in self.children:
            entity.propagate_down(ev_name, *args, **kargs)

    # Disabled until I'm sure I actually need this.
    #def __getattr__(self, name):
    #    """Inherit the components of my parents, recursively."""
    #    if self.parent is None:
    #        raise AttributeError(
    #            "Attribute %r does not exist in this object nor it's parents.")
    #    return getattr(self.parent, name)

    def __setattr__(self, name, value):
        """Assign a component to an attribute name."""
        if name in self._RESERVED_ATTRIBUTES:
            return object.__setattr__(self, name, value)
        assert not isinstance(value, Entity), \
            "Named attributes are for components only."
        assert value.name is None, \
            "A component can not be assigned to multiple attributes."
        if name in self.__dict__:
            self.__delattr__(self, name)
        value.name = name
        object.__setattr__(self, name, value)
        self.add_component(value)

    def __delattr__(self, name):
        """Delete an assigned component attribute."""
        self.remove_component(object.__getattr__(self, name))
