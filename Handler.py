import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class Handler:
        def __init__(self,app):
        	self.app=app
	def on_inv_radiobutton_toggled(self,button):
		active=button.get_active()
		if active:
			app.saisir_operandes("INVERSER","MATRICE","Calcul de l'inverse d'une matrice")
	
		

          


   