import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from BaseEditionDialog    import BaseEditionDialog

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
	def on_pass_radiobutton_toggled(self,button):
		active=button.get_active()
		if active:
			self.app.saisir_operandes("PASS","DEUX_BASES","Calcul de la matrice de passage entre deux bases")
	def on_spec_radiobutton_toggled(self,button):
		active=button.get_active()
		if active:
			self.app.saisir_operandes("SPEC","MATRICE","Calcul du spectre d'une matrice")
	def on_vp_radiobutton_toggled(self,button):
		active=button.get_active()
		if active:
			self.app.saisir_operandes("VP","MATRICE","Calcul des vecteurs propres d'une matrice")	
	def on_diag_radiobutton_toggled(self,button):
		active=button.get_active()
		if active:
			self.app.saisir_operandes("DIAG","MATRICE","Diagonalisation d'une matrice")
	def on_det_radiobutton_toggled(self,button):
		active=button.get_active()
		if active:
			self.app.saisir_operandes("DET","MATRICE","Calcul du determinant d'une matrice")
	def on_equadif_radiobutton_toggled(self,button):
		active=button.get_active()
		if active:
			self.app.saisir_operandes("EDL","DEUX_VECTEURS","Resolution d'une equation differentielle lineaire")			
	def on_sl_radiobutton_toggled(self,button):
		active=button.get_active()
		if active:
			self.app.saisir_operandes("SL","MATRICE_VECTEUR","Resolution d'un systeme lineaire")
	def on_prod_radiobutton_toggled(self,button):
		active=button.get_active()
		if active:
			self.app.saisir_operandes("PROD","MIXTE","Calcul du produit de matrices ou vecteurs")	
	def on_som_radiobutton_toggled(self,button):
		active=button.get_active()
		if active:
			self.app.saisir_operandes("SOM","MIXTE","Calcul de la somme de deux matrices ou vecteurs")	
	def on_diff_radiobutton_toggled(self,button):
		active=button.get_active()
		if active:
			self.app.saisir_operandes("DIFF","MIXTE","Calcul de la difference de deux matrices ou vecteurs")	
	def on_factlu_radiobutton_toggled(self,button):
		active=button.get_active()
		if active:
			self.app.saisir_operandes("FACT LU","MATRICE","Factorisation LU d'une matrice")
	def on_tr_radiobutton_toggled(self,button):
		active=button.get_active()
		if active:
			self.app.saisir_operandes("TR","MATRICE","Calcul de la trace d'une matrice")
	def on_edit_base_button1_clicked(self,button):
		dialog=BaseEditionDialog([['v1',4,True],['v2',2,True],['v3',3,False],['v4',4,False],['v6',4,False],['v7',4,False],['v5',4,False]],3)
		response=dialog.run()
		if response == Gtk.ResponseType.OK :
			selected=dialog.get_selected()
			print selected
			self.app.print_base_on_textbuffer(self.app.textbuffer1,selected)
		dialog.destroy()
	def on_edit_base_button2_clicked(self,button):
		dialog=BaseEditionDialog([['v1',4,True],['v2',2,True],['v3',3,False],['v4',4,False],['v6',4,False],['v7',4,False],['v5',4,False]],3)
		response=dialog.run()
		if response == Gtk.ResponseType.OK :
			selected=dialog.get_selected()
			print selected
			self.app.print_base_on_textbuffer(self.app.textbuffer2,selected)
		dialog.destroy()

          


   
