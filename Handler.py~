import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class Handler:
        def __init__(self,app):
        	self.app=app
        def on_window_delete_event(self,window,event):
        	Gtk.main_quit()
        def on_envoyer_button_clicked(self,button):
        	self.app.on_envoyer_button_clicked(button)
        def on_add_matrix_button_clicked(self,button):
        	self.app.on_add_matrix_button_clicked(button)
        def on_ajouter_resultat_button_clicked(self,button):
        	self.app.on_ajouter_resultat_button_clicked(button)
        def on_delete_matrix_button_clicked(self,button):
        	self.app.on_delete_matrix_button_clicked(button)
        def on_edit_matrix_button_clicked(self,button):
        	self.app.on_edit_matrix_button_clicked(button)
        def on_treeview_selection_changed(self,selection):
        	self.app.on_selection_changed(selection)
	def on_inv_radiobutton_toggled(self,button):
		active=button.get_active()
		if active:
			self.app.saisir_operandes("INV","MATRICE","Calcul de l'inverse d'une matrice")
	def on_puiss_radiobutton_toggled(self,button):
		active=button.get_active()
		if active:
			self.app.saisir_operandes("PUIS","MATRICE_ENTIER","Calcul de la puissance d'une matrice")
	def on_srl_radiobutton_toggled(self,button):
		active=button.get_active()
		if active:
			self.app.saisir_operandes("SRL","DEUX_VECTEURS","Calcul du terme general d'une suite recurente lineaire")
	def on_trans_radiobutton_toggled(self,button):
		active=button.get_active()
		if active:
			self.app.saisir_operandes("TRANS","MATRICE","Calcul de la transposee d'une matrice")	
		

          


   
