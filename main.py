import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from Handler               import Handler
from MatrixEditorDialog    import MatrixEditorDialog
from NamesInputDialog      import NamesInputDialog

class LAC_ApplicationWindow:
	def __init__(self):
		 self.row1=0
		 self.row2=0
	    	 self.current_operation="INVERSER"	
		 self.matrix_list={}
		 self.builder=Gtk.Builder()
		 self.builder.add_from_file("LAC_Applicationwindow.glade")
	 
		 self.window=self.builder.get_object("window")  
		 self.ajouter_resultat_button=self.builder.get_object('ajouter_resultat_button')
		 self.delete_matrix_button=self.builder.get_object('delete_matrix_button')
		 self.edit_matrix_button=self.builder.get_object('edit_matrix_button')
		 
		 self.premiere_op_box=self.builder.get_object("premiere_op_box")
		 self.deuxieme_op_box=self.builder.get_object("deuxieme_op_box")
		 
		 self.operation_label=self.builder.get_object("operation_label")
		 self.premiere_op_label=self.builder.get_object("premiere_op_label")
		 self.comboboxtext1=self.builder.get_object("comboboxtext1")
		 self.famille_box1=self.builder.get_object("famille_box1")
		 
		 self.deuxieme_op_label=self.builder.get_object("deuxieme_op_label")
		 self.comboboxtext2=self.builder.get_object("comboboxtext2")
		 self.famille_box2=self.builder.get_object("famille_box2")
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
		 self.window.show_all()
		 
		 self.ajouter_resultat_button.hide()
		 self.deuxieme_op_box.set_visible(False)
		 self.premiere_op_label.set_text("Choisir une matrice")
		 self.famille_box1.set_visible(False)
		 
		 self.resultat_label=self.builder.get_object("resultat_label")
		 self.resultat_box=self.builder.get_object("resultat_box")
		 self.resultat_grid1=self.builder.get_object("resultat_grid1")
		 self.resultat_grid2=self.builder.get_object("resultat_grid2")
		 
		 self.textbuffer1=self.builder.get_object("textbuffer1")
		 self.textbuffer2=self.builder.get_object("textbuffer2")
		 
	 	 self.builder.connect_signals(Handler(self))
	def print_base_on_textbuffer(self,textbuffer,list_name):
		chaine='{'+', '.join(list_name)+'}'
		textbuffer.set_text(chaine)
		
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
	def calculer_operation(name,operandes):
		res1=[]
		res2=[]
		return res1,res2
	"""def print_matrix_on_grid(self,grid,matrix):
		grid.clear()"""
		
	def on_envoyer_button_clicked(self,button):
		self.resultat_box.show()
		self.resultat_label.hide()
		
		"""print range(self.row1)"""
		for row in range(self.row1):
	    		self.resultat_grid1.remove_row(0)
	    	self.row1=0
	    	
	    	"""print range(self.row2)"""
	    	for row in range(self.row2):
	    		self.resultat_grid2.remove_row(0)
	    	self.row2=0
	    			
		self.resultat_grid1.hide()
		self.resultat_grid2.hide()
		self.ajouter_resultat_button.show()
	    	if self.current_operation in ("DIAG","FACT LU"):
	    		for i in range(3):
	    			self.resultat_grid1.insert_row(i)
	    			self.row1+=1
	    			for j in range(2):
	    				label=Gtk.Label(str(i*3+j))
	    				label.show()
	    				self.resultat_grid1.attach(label,j,i,1,1)
	    		for i in range(2):
	    			self.resultat_grid2.insert_row(i)
	    			self.row2+=1
	    			for j in range(3):
	    				label=Gtk.Label(str(i*3+j))
	    				label.show()
	    				self.resultat_grid2.attach(label,j,i,1,1)

	    		self.resultat_grid1.show()
	    		self.resultat_grid2.show()
		elif self.current_operation in ("SRL","EDL","DET","TR"):
			self.resultat_label.set_text("Resultat: %s"%self.current_operation)
	    		self.resultat_label.show()
	    	else:
	    		for i in range(3):
	    			self.resultat_grid1.insert_row(i)
	    			self.row1+=1
	    			for j in range(2):
	    				label=Gtk.Label(str(i*3+j))
	    				label.show()
	    				self.resultat_grid1.attach(label,j,i,1,1)
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
		self.current_operation=name
		
 	        self.deuxieme_op_box.show()
 	        self.comboboxtext1.hide()
 	        self.famille_box1.hide()
	        self.deuxieme_op_label.hide()
 	        self.famille_box2.hide()
 	        self.comboboxtext2.hide()
 	        self.spinbutton.hide()
 	        
 	        self.operation_label.set_text(msg)
 	        if operandes=="MATRICE":
 	        	self.premiere_op_label.set_text("Choisir une matrice")
                   	self.comboboxtext1.show()
                elif operandes=="DEUX_BASES":
                	self.premiere_op_label.set_text("Premiere famille de vecteurs")
	           	self.famille_box1.show()
		           	
	           	self.deuxieme_op_label.show()
	           	self.deuxieme_op_label.set_text("Deuxieme famille de vecteurs")
	           	self.famille_box2.show()
	        elif operandes=="DEUX_MATRICES":
	        	self.premiere_op_label.set_text("Premiere Matrice")
	           	self.comboboxtext1.show()
		           	
	           	self.deuxieme_op_label.show()
	           	self.deuxieme_op_label.set_text("Deuxieme Matrice")
	           	self.comboboxtext2.show()
	        elif operandes=="DEUX_VECTEURS":
	        	self.premiere_op_label.set_text("Premier vecteur")
	           	self.comboboxtext1.show()
		           	
	           	self.deuxieme_op_label.show()
	           	self.deuxieme_op_label.set_text("Deuxieme vecteur")
	           	self.comboboxtext2.show()
	        elif operandes=="MIXTE":
	        	self.premiere_op_label.set_text("Premier Operande")
	           	self.comboboxtext1.show()
		           	
	           	self.deuxieme_op_label.show()
	           	self.deuxieme_op_label.set_text("Deuxieme Operande")
	           	self.comboboxtext2.show()
	        elif operandes=="MATRICE_VECTEUR":
	        	self.premiere_op_label.set_text("Choisir une matrice")
	           	self.comboboxtext1.show()
		           	
	           	self.deuxieme_op_label.show()
	           	self.deuxieme_op_label.set_text("Choisir un vecteur")
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
