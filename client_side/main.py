import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from Handler               import Handler
from MatrixEditorDialog    import MatrixEditorDialog
from NamesInputDialog      import NamesInputDialog
from ConnexionDialog       import ConnexionDialog
from client                import ClientTCP
import socket
from fractions import Fraction
from numbers import Number

def vector_to_matrix(v,n,p):
        m=[[0 for i in range(p)] for j in range(n)]
        for i in range(n):
                for j in range(p):
                        m[i][j]=v[i*p+j]
        return m
def matrix_to_vector(matrix):
	v=[]
	for u in matrix:
		v+=u
	n=len(matrix)
	p=len(matrix[0])
	return (v,n,p)

class LAC_ApplicationWindow:
        def __init__(self):
                self.client_tcp=None
                self.operator="INV"
                self.operandes="MATRICE"		
                self.matrix_list={}
                self.builder=Gtk.Builder()
                self.builder.add_from_file("./glade/LAC_Applicationwindow.glade")

                self.window=self.builder.get_object("window")  
                self.spinner=self.builder.get_object('spinner')
                self.ajouter_resultat_button=self.builder.get_object('ajouter_resultat_button')
                self.sendsms_button=self.builder.get_object('sendsms_button')
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
                self.combobox=self.builder.get_object("combobox")
                self.resultat_matrix_box=self.builder.get_object("resultat_matrix_box")
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



                self.error_label=self.builder.get_object("error_label")
                self.resultat_label1=self.builder.get_object("resultat_label1")
                self.resultat_label2=self.builder.get_object("resultat_label2")

                self.textbuffer1=self.builder.get_object("textbuffer1")
                self.textbuffer2=self.builder.get_object("textbuffer2")

                self.ajouter_resultat_button.hide()
                self.deuxieme_op_box.set_visible(False)
                self.premiere_op_label.set_text("Choisir une matrice")
                self.famille_box1.set_visible(False)
                self.error_label.hide()
                self.resultat_label2.hide()
                self.resultat_label1.hide()

                self.combobox1_type="MATRICE"
                self.combobox2_type=""

                self.builder.connect_signals(Handler(self))

        def print_base_on_textbuffer(self,textbuffer,list_name):
                chaine='{'+', '.join(list_name)+'}'
                textbuffer.set_text(chaine)

	def add_matrix(self,name,obj):
		m,n,p=obj
		if name in self.matrix_list:
			flags=Gtk.DialogFlags.MODAL
			mess_type=Gtk.MessageType.WARNING
			buttons=Gtk.ButtonsType.OK_CANCEL
			message='Il existe un object possedant le meme nom.\nVoulez-vous ecrasez ce dernier?'
			dialog=Gtk.MessageDialog(self.window,flags,mess_type,buttons , message)
			response=dialog.run()
			if response == Gtk.ResponseType.CANCEL:
				dialog.destroy()
				return
			dialog.destroy()
			for item in self.liststore:
				if item[0]==name:
					item[1:]=[n,p]
		else:
			self.liststore.append([name,n,p])	
		self.matrix_list[name]=obj
                self.set_combobox_list(self.comboboxtext1,self.combobox1_type)
                self.set_combobox_list(self.comboboxtext2,self.combobox2_type)
        def on_add_matrix_button_clicked(self, button):
                dialog=MatrixEditorDialog(parent=self.window)
                response=dialog.run()
                if response == Gtk.ResponseType.OK:
                        name,obj=dialog.get_object()
                        self.add_matrix(name,obj)
                dialog.destroy()
        def add_result_to_objects_list(self):
                if self.result and self.result2:
                        dialog=NamesInputDialog(twice=True,parent=self.window)
                     	
                elif self.result:
                 	dialog=NamesInputDialog(parent=self.window)
                 	
               	else:
               	 	return

                response=dialog.run()
        	if response == Gtk.ResponseType.OK :
                	self.ajouter_resultat_button.hide()
                	name,name2=dialog.get_names()
                	print (name,self.result)
                	self.add_matrix(name,matrix_to_vector(self.result))
                	
                	if name2:
                		print (name2,self.result2)
                		self.add_matrix(name2,matrix_to_vector(self.result2))
                        
                dialog.destroy()
        def set_matrix_data(self,label,data=[]):
        	
        	if isinstance(data,Number):
        		label.set_text(str(Fraction(data).limit_denominator()).ljust(20 ))
        	else:
        		self.ajouter_resultat_button.show()
        		text=''
			for u in data:
				ch='                       '.join([str(Fraction(x).limit_denominator()).ljust(20) for x in u])
				text+=ch+'\n'
			print text
			label.set_text(text)
		label.show()
        def get_operande_matrix(self,num=1):
        	if num==1:
        		active=self.comboboxtext1.get_active_text()
        	else:
        		active=self.comboboxtext2.get_active_text()
		if active:
        		tab=active.split('(',1)
			if len(tab)>0:
				name=tab[0]
				matrix1=vector_to_matrix(self.matrix_list[name])
				return matrix1
		       	else:
		       		return None
	       	else:
	       		return None
	def get_operande_vector(self,num=1):
        	if num==1:
        		active=self.comboboxtext1.get_active_text()
        	else:
        		active=self.comboboxtext2.get_active_text()
		if active:
        		tab=active.split('(')
			if len(tab)>0:
				name=tab[0]
				vector,n,p=self.matrix_list[name]
				return vector
		       	else:
		       		return None
	       	else:
	       		return None
	def get_operande_base(self,num=1):
		
		if num==1:
			txtbuf=self.textbuffer1
		else:
			txtbuf=self.textbuffer2
		start,end=txtbuf.get_bounds()
		if start.is_end():
			return None
		else:
			text=txtbuf.get_text(start,end,include_hidden_chars=False)
			text=text[1:]
			text=text[:-1]
		
			print text
			return [ self.matrix_list[name][0] for name in text.split(',') ]
        def get_operandes(self):		
	        if self.operandes=='MATRICE':
	        	return self.get_operande_matrix(1)
	      	elif self.operandes=='DEUX_MATRICES' or self.operandes=='MIXTE':
	      		oper1=self.get_operande_matrix(1)
	      		oper2=self.get_operande_matrix(2)
	      	elif self.operandes=='MATRICE_VECTEUR':
	      		oper1=self.get_operande_matrix(1)
	      		oper2=self.get_operande_vector(2)
	      	elif self.operandes=='MATRICE_ENTIER':
	      		oper1=self.get_operande_matrix(1)
	      		oper2=self.spinbutton.get_value_as_int()
	      	elif self.operandes=='DEUX_BASES':
	      		oper1=self.get_operande_base(1)
	      		oper2=self.get_operande_base(2)
	      		print oper1,oper2
	      	else:
	      		return None
	      		
		if oper1 and oper2:
			return (oper1,oper2)
      		else:
      			return None

        def on_envoyer_button_clicked(self,button):
                 operandes=self.get_operandes()
                 if operandes:
		 	self.client_tcp.set_operation(self.operator,operandes)
		 	self.spinner.start()
		 else:
		 	self.error_label.set_text('Veuillez choisir tous les champs')
                        self.error_label.show()
		 
        def display_result(self,result):
                self.spinner.stop()
                
                self.error_label.hide()
                self.resultat_label2.hide()
                self.resultat_label1.hide()
                self.ajouter_resultat_button.hide()
                self.sendsms_button.hide()
                self.result2=None
                self.result=None

		print 'Le resultat est %s'%result
                if 'error' in result:
                      	self.error_label.set_text(result['error'])
                        self.error_label.show()
                        return
                elif 'result' in result:
                	self.set_matrix_data(self.resultat_label1,result['result'])
               		self.result=result['result']
               		self.sendsms_button.show()
                	if 'result2' in result:
			        self.set_matrix_data(self.resultat_label2,result['result2'])
			        self.result2=result['result2']
                	
        def get_selected_name(self):
                selection=self.treeview.get_selection()
                model,self.treeiter=selection.get_selected()
                item=model[self.treeiter]
                return item[0]
        def on_edit_matrix_button_clicked(self,button):
                name=self.get_selected_name()
                m,n,p=self.matrix_list[name]

                dialog=MatrixEditorDialog(name,m,n,p,parent=self.window)
                response=dialog.run()
                if response == Gtk.ResponseType.OK :
                        name,obj=dialog.get_object()
                        self.matrix_list[name]=obj
                        m,n,p=obj
                        self.liststore[self.treeiter][1:]=[n,p]
             
                dialog.destroy()
        def on_selection_changed(self,selection):
                model,self.treeiter=selection.get_selected()

                if self.treeiter!=None:
                        self.delete_matrix_button.set_sensitive(True)
                        self.edit_matrix_button.set_sensitive(True)
                else:
                        self.delete_matrix_button.set_sensitive(False)
                        self.edit_matrix_button.set_sensitive(False)

        def on_delete_matrix_button_clicked(self,button):
                selection=self.treeview.get_selection()
                model,self.treeiter=selection.get_selected()
                item=model[self.treeiter]
                del self.matrix_list[item[0]]
                model.remove(self.treeiter)
                self.set_combobox_list(self.comboboxtext1,self.combobox1_type)
                self.set_combobox_list(self.comboboxtext2,self.combobox2_type)
        def on_radiobutton_group_changed(self,radiobutton):
                print (radiobutton.get_label())

        def set_combobox_list(self,combobox,mode="MATRICE"):
                liststore=combobox.get_model()
                liststore.clear()
                if mode=="MATRICE":
                        for obj in self.matrix_list:
                                n=self.matrix_list[obj][1]
                                p=self.matrix_list[obj][2]
                                if n>1 and p>1:
                                        print (self.matrix_list[obj])
                                        combobox.append_text(obj+'('+str(n)+"x"+str(p)+')')
                elif mode=="VECTEUR":
                        for obj in self.matrix_list:
                                n=self.matrix_list[obj][1]
                                p=self.matrix_list[obj][2]                                
                                if n==1 or p==1:
                                        print (self.matrix_list[obj])
                                        combobox.append_text(obj+'('+str(n)+"x"+str(p)+')')
                elif mode=="MIXTE":
                        for obj in self.matrix_list:
                                n=self.matrix_list[obj][1]
                                p=self.matrix_list[obj][2]
                                print (self.matrix_list[obj])
                                combobox.append_text(obj+'('+str(n)+"x"+str(p)+')')

        def saisir_operandes(self,operator,operandes,msg):
                self.operator=operator
                self.operandes=operandes

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
                        self.combobox1_type="MATRICE"
                        self.combobox2_type=""
                        self.set_combobox_list(self.comboboxtext1)
                        self.comboboxtext1.show()
                elif operandes=="DEUX_BASES":
                        self.combobox1_type=""
                        self.combobox2_type=""
                        self.premiere_op_label.set_text("Premiere famille de vecteurs")
                        self.famille_box1.show()

                        self.deuxieme_op_label.show()
                        self.deuxieme_op_label.set_text("Deuxieme famille de vecteurs")
                        self.famille_box2.show()
                elif operandes=="DEUX_MATRICES":
                        self.combobox1_type="MATRICE"
                        self.combobox2_type="MATRICE"

                        self.premiere_op_label.set_text("Premiere Matrice")
                        self.set_combobox_list(self.comboboxtext1)
                        self.set_combobox_list(self.comboboxtext2)
                        self.comboboxtext1.show()

                        self.deuxieme_op_label.show()
                        self.deuxieme_op_label.set_text("Deuxieme Matrice")
                        self.comboboxtext2.show()
                elif operandes=="DEUX_VECTEURS":
                        self.combobox1_type="VECTEUR"
                        self.combobox2_type="VECTEUR"
                        self.premiere_op_label.set_text("Premier vecteur")
                        self.set_combobox_list(self.comboboxtext1,"VECTEUR")
                        self.set_combobox_list(self.comboboxtext2,"VECTEUR")
                        self.comboboxtext1.show()

                        self.deuxieme_op_label.show()
                        self.deuxieme_op_label.set_text("Deuxieme vecteur")
                        self.comboboxtext2.show()
                elif operandes=="MIXTE":
                        self.combobox1_type="MIXTE"
                        self.combobox2_type="MIXTE"
                        self.premiere_op_label.set_text("Premier Operande")
                        self.set_combobox_list(self.comboboxtext1,"MIXTE")
                        self.set_combobox_list(self.comboboxtext2,"MIXTE")
                        self.comboboxtext1.show()

                        self.deuxieme_op_label.show()
                        self.deuxieme_op_label.set_text("Deuxieme Operande")
                        self.comboboxtext2.show()
                elif operandes=="MATRICE_VECTEUR":
                        self.combobox1_type="MATRICE"
                        self.combobox2_type="VECTEUR"
                        self.premiere_op_label.set_text("Choisir une matrice")
                        self.set_combobox_list(self.comboboxtext1,"MATRICE")
                        self.set_combobox_list(self.comboboxtext2,"VECTEUR")
                        self.comboboxtext1.show()

                        self.deuxieme_op_label.show()
                        self.deuxieme_op_label.set_text("Choisir un vecteur")
                        self.comboboxtext2.show()
                elif operandes=="MATRICE_ENTIER":
                        self.combobox1_type="MATRICE"
                        self.combobox2_type=""
                        self.premiere_op_label.set_text("Choisir une matrice")
                        self.set_combobox_list(self.comboboxtext1)
                        self.comboboxtext1.show()

                        self.deuxieme_op_label.show()
                        self.deuxieme_op_label.set_text("Saisir un entier")
                        self.spinbutton.show()
        def connecter(self,ip,port):
                self.client_tcp=ClientTCP(ip,port,self.display_result)
                self.client_tcp.start()	
        def show_all(self):
                self.window.show_all()
        def __del__(self):
                print "destruction"
                if self.client_tcp:
                        self.client_tcp.disconnect()
                        self.client_tcp.close()
                        self.client_tcp.join()

app=LAC_ApplicationWindow()
dialog=ConnexionDialog(parent=app.window)

while True:
        response=dialog.run()
        if response == Gtk.ResponseType.OK :
                ip,port=dialog.get_address()
                try:
                        app.connecter(ip,port)
                        dialog.destroy()
                        Gtk.main()
                        break
                except socket.error:
                        dialog.show_error()
                        continue
        else:
                dialog.destroy()
                break
app.__del__()	



