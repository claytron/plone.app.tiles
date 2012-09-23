from plone.app.registry.browser import controlpanel

from plone.app.tiles.interfaces import IDecoSettings, _


class DecoControlPanelEditForm(controlpanel.RegistryEditForm):

    schema = IDecoSettings
    label = _(u"Deco settings")
    description = _(u"""""")

    def updateFields(self):
        super(DecoControlPanelEditForm, self).updateFields()

    def updateWidgets(self):
        super(DecoControlPanelEditForm, self).updateWidgets()


class DecoControlPanel(controlpanel.ControlPanelFormWrapper):
    form = DecoControlPanelEditForm
