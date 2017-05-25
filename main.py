import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from Handler             import Handler
from MatrixEditorDialog  import MatrixEditorDialog
from NamesInputDialog    import NamesInputDialog

class LAC_ApplicationWindow:
	def __init__(self):
	    	 self.current_operation="INVERSER"	
		 self.matrix_list={}
		 self.builder=Gtk.Builder()
		 self.builder.add_from_file("LAC_Applicationwindow.glade")
		 
		 self.window=self.builder.get_object("window")
		 
		 handlers={
		 	"on_envoyer_button_clicked":self.on_envoyer_button_clicked,
		 	"on_add_matrix_button_clicked":self.on_add_matrix_button_clicked,
		 	"on_ajouter_resultat_button_clicked":self.on_ajouter_resultat_button_clicked,
		 	"on_delete_matrix_button_clicked":self.on_delete_matrix_button_clicked,
		 	"on_edit_matrix_button_clicked":self.on_edit_matrix_button_clicked,
		 }
		 self.builder.connect_signals(handlers)
		 self.builder.connect_signals(Handler(self))
		   
		 self.ajouter_resultat_button=self.builder.get_object('ajouter_resultat_button')
		 self.delete_matrix_button=self.builder.get_object('delete_matrix_button')
		 self.edit_matrix_button=self.builder.get_object('edit_matrix_button')
		 
		 self.premiere_op_box=self.builder.get_object("premiere_op_box")
		 self.deuxieme_op_box=self.builder.get_object("deuxieme_op_box")
		 
		 self.operation_label=self.builder.get_object("operation_label")
		 self.premiere_op_label=self.builder.get_object("premiere_op_label")
		 self.comboboxtext1=self.builder.get_object("comboboxtext1")
		 self.entry1=self.builder.get_object("entry1")
		 
		 self.deuxieme_op_label=self.builder.get_object("deuxieme_op_label")
		 self.comboboxtext2=self.builder.get_object("comboboxtext2")
		 self.entry2=self.builder.get_object("entry2")
		 self.spinbutton=self.builder.get_object("spinbutton")
		            
		 self.treeview=self.builder.get_object("treeview")
		 self.liststore=Gtk.ListStore(str,int,int)
		 self.treeview.set_model(self.liststore)
		 renderer=Gtk.CellRendererText()
		 column=Gtk.TreeViewColumn("Nom",renderer,text=0)
		 self.treeview.append_column(column)
		 column=Gtk.TreeViewColumn("Nbr Ligne",renderer,text=1)
		 self.treeview.append_column(column)
		 column=Gtk.TreeViewColumn("Nbr Col",renderer,text=2)
		 self.treeview.append_column(column)
		 selection=self.treeview.get_selection()
		 selection.connect('changed',self.on_selection_changed)
		 self.window.show_all()
		 
		 self.ajouter_resultat_button.hide()
		 self.deuxieme_op_box.set_visible(False)
		 self.premiere_op_label.set_text("Choisir une matrice")
		 self.entry1.set_visible(False)
		 
		 self.resultat_label=self.builder.get_object("resultat_label")
		 self.resultat_box=self.builder.get_object("resultat_box")
		 self.resultat_grid1=self.builder.get_object("resultat_grid1")
		 self.resultat_grid2=self.builder.get_object("resultat_grid2")
		 
		 
		 self.window.connect("delete-event",Gtk.main_quit)
	def on_add_matrix_button_clicked(self,button):
		 dialog=MatrixEditorDialog()
		 response=dialog.run()
		 if response == Gtk.ResponseType.OK :
		      name,m,n,p=dialog.get_object()
		      self.matrix_list[name]=(m,n,p)
		      self.liststore.append([name,n,p])
		 """elif response == Gtk.ResponseType.CANCEL :"""
		 dialog.destroy()
	def on_ajouter_resultat_button_clicked(self,button):
		 if self.current_operation=="PASSAGE":
		 	dialog=NamesInputDialog("Quel nom voulez-vous donner a la matrice de passage?","Quel nom voulez-vous donner a la matrice diagonale?")
		 elif self.current_operation=="VECTEURS PROPRES":
		 	dialog=NamesInputDialog("Avec quel prefixe voulez-vous nommer les vecteurs propres?")
		 else :
		 	dialog=NamesInputDialog("Quel nom voulez-vous donner a la matrice?")
		 	
		 response=dialog.run()
		 if response == Gtk.ResponseType.OK :
		     self.ajouter_resultat_button.hide()
		     name1,name2=dialog.get_names()
		     print name1,name2
		 dialog.destroy()
	def on_envoyer_button_clicked(self,button):
		self.resultat_box.show()
		self.resultat_label.hide()
		self.resultat_grid1.hide()
		self.resultat_grid2.hide()
		self.ajouter_resultat_button.show()
	    	if self.current_operation=="DIAGONALISER":
	    		self.resultat_grid1.show()
	    		self.resultat_grid2.show()
		elif self.current_operation in ("SUITE","EQUADIF"):
	    		self.resultat_label.show()
	    	else:
	    		self.resultat_grid1.show()
	def get_selected_name(self):
		 selection=self.treeview.get_selection()
		 model,treeiter=selection.get_selected()
		 item=model[treeiter]
		 return item[0]
	def on_edit_matrix_button_clicked(self,button):
		 name=self.get_selected_name()
		 m,n,p=self.matrix_list[name]
		 
		 dialog=MatrixEditorDialog(name,m,n,p)
		 response=dialog.run()
		 if response == Gtk.ResponseType.OK :
		      name,m,n,p=dialog.get_object()
		      self.matrix_list[name]=(m,n,p)
		      self.liststore[self.treeiter][1:]=[n,p]
		 """elif response == Gtk.ResponseType.CANCEL :"""
		 dialog.destroy()
	def on_selection_changed(self,selection):
		 model,treeiter=selection.get_selected()
		 
		 if treeiter!=None:
		    self.delete_matrix_button.set_sensitive(True)
		    self.edit_matrix_button.set_sensitive(True)
		    self.treeiter=treeiter
		 else:
		    self.delete_matrix_button.set_sensitive(False)
		    self.edit_matrix_button.set_sensitive(False)
		    
	def on_delete_matrix_button_clicked(self,button):
		 selection=self.treeview.get_selection()
		 model,treeiter=selection.get_selected()
		 item=model[treeiter]
		 del self.matrix_list[item[0]]
		 model.remove(treeiter)
	def on_radiobutton_group_changed(self,radiobutton):
    		print radiobutton.get_label()
	def saisir_operandes(self,name,operandes,msg):
 	        """self.resultat_box.hide()"""
 	        self.current_operation=name
 	        self.operation_label.set_text(msg)
 	        if operandes=="MATRICE":
 	        	self.premiere_op_label.set_text("Choisir une matrice")
                   	self.comboboxtext1.show()
                elif operandes=="FAMILLE_VECTEUR":
                	self.premiere_op_label.set_text("Saisir une famille de vecteur")
	           	self.entry1.show()
		           	
	           	self.deuxieme_op_label.show()
	           	self.deuxieme_op_label.set_text("Une autre famille de vecteur")
	           	self.entry2.show()
	        elif operandes=="DEUX_MATRICES":
	        	self.premiere_op_label.set_text("Premiere operande")
	           	self.comboboxtext1.show()
		           	
	           	self.deuxieme_op_label.show()
	           	self.deuxieme_op_label.set_text("Deuxieme operande")
	           	self.comboboxtext2.show()
	        elif operandes=="MATRICE_ENTIER":
	        	self.premiere_op_label.set_text("Choisir une matrice")
	           	self.comboboxtext1.show()
		           	
	           	self.deuxieme_op_label.show()
	           	self.deuxieme_op_label.set_text("Saisir un entier")
	           	self.spinbutton.show()		
	def show_all(self):
           	self.window.show_all()

app=LAC_ApplicationWindow()
Gtk.main()
