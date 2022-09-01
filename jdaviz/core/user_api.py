__all__ = ['UserApiWrapper', 'PluginUserApi']


class UserApiWrapper:
    """
    This is an API wrapper around an internal object.  For a full list of attributes/methods,
    call dir(object).
    """
    def __init__(self, obj, expose=[]):
        self._obj = obj
        self._expose = expose
        if obj.__doc__ is not None:
            self.__doc__ = self.__doc__ + "\n\n\n" + obj.__doc__

    def __dir__(self):
        return self._expose

    def __repr__(self):
        return self._obj.__repr__()

    def __getattr__(self, attr):
        if attr in ['_obj', '_expose', '__doc__'] or attr not in self._expose:
            return super().__getattribute__(attr)

        exp_obj = getattr(self._obj, attr)
        return getattr(exp_obj, 'user_api', exp_obj)

    def __setattr__(self, attr, value):
        if attr in ['_obj', '_expose', '__doc__'] or attr not in self._expose:
            return super().__setattr__(attr, value)

        exp_obj = getattr(self._obj, attr)
        from jdaviz.core.template_mixin import BaseSelectPluginComponent, PlotOptionsSyncState
        if isinstance(exp_obj, BaseSelectPluginComponent):
            # this allows setting the selection directly without needing to access the underlying
            # .selected traitlet
            exp_obj.selected = value
            return
        elif isinstance(exp_obj, PlotOptionsSyncState):
            # this allows setting the value immediately, and unmixing state, if appropriate,
            # even if the value matches the current value
            if value == exp_obj.value:
                exp_obj.unmix_state()
            else:
                exp_obj.value = value
            return

        return setattr(self._obj, attr, value)


class PluginUserApi(UserApiWrapper):
    """
    This is an API wrapper around an internal plugin.  For a full list of attributes/methods,
    call dir(plugin_object) and for help on any of those methods, call help(plugin_object.attribute).

    For example::
      help(plugin_object.show)
    """
    def __init__(self, plugin, expose=[]):
        expose = list(set(list(expose) + ['open_in_tray', 'show']))
        super().__init__(plugin, expose)

    def __repr__(self):
        return f'<{self._obj._registry_label} API>'
