import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from Handler               import Handler
from MatrixEditorDialog    import MatrixEditorDialog
from NamesInputDialog      import NamesInputDialog
from ConnexionDialog       import ConnexionDialog
from client                import ClientTCP
import socket

def vector_to_matrix(v,n,p):
        m=[[0 for i in range(p)] for j in range(n)]
        for i in range(n):
                for j in range(p):
                        m[i][j]=v[i*n+j]
        return m

class LAC_ApplicationWindow:
        def __init__(self):
                self.client_tcp=None
                self.operator="INV"
                self.operandes="MATRICE"		
                self.matrix_list={}
                self.builder=Gtk.Builder()
                self.builder.add_from_file("LAC_Applicationwindow.glade")

                self.window=self.builder.get_object("window")  
                self.spinner=self.builder.get_object('spinner')
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

                self.combobox1_type="MATRICE"
                self.combobox2_type=""

                self.builder.connect_signals(Handler(self))

        def print_base_on_textbuffer(self,textbuffer,list_name):
                chaine='{'+', '.join(list_name)+'}'
                textbuffer.set_text(chaine)

        def on_add_matrix_button_clicked(self,button):
                dialog=MatrixEditorDialog(parent=self.window)
                response=dialog.run()
                if response == Gtk.ResponseType.OK:
                        name,m,n,p=dialog.get_object()
                        self.matrix_list[name]=(m,n,p)
                        self.liststore.append([name,n,p])
                        self.set_combobox_list(self.comboboxtext1,self.combobox1_type)
                        self.set_combobox_list(self.comboboxtext2,self.combobox2_type)
                dialog.destroy()
        def on_ajouter_resultat_button_clicked(self,button):
                if self.operator=="PASSAGE":
                        NamesInputDialog("Quel nom voulez-vous donner a la matrice de passage?","Quel nom voulez-vous donner a la matrice diagonale?")
                elif self.operator=="VECTEURS PROPRES":
                        dialog=NamesInputDialog("Avec quel prefixe voulez-vous nommer les vecteurs propres?")
                else :
                        dialog=NamesInputDialog("Quel nom voulez-vous donner a la matrice?")

                response=dialog.run()
                if response == Gtk.ResponseType.OK :
                        self.ajouter_resultat_button.hide()
                        name1,name2=dialog.get_names()
                        print(name1,name2)
                dialog.destroy()
        def set_matrix_data(self,label,data=[]):
        	label.show()
        	text=''
        
        	for u in data:
        		ch='       '.join(['{: f}'.format(x) for x in u])
        		text+=ch+'\n'
        	label.set_text(text)

        def get_operandes(self):
                if self.operandes=='MATRICE':
                        name=self.comboboxtext1.get_active_text().split('(')[0]
                        v,n,p=self.matrix_list[name]
                        matrix=vector_to_matrix(v,n,p)
                        return matrix


        def on_envoyer_button_clicked(self,button):
                self.spinner.start()
                self.client_tcp.set_operation(self.operator,self.get_operandes())


        def display_result(self,result):
                self.spinner.stop()
                self.error_label.hide()
                self.resultat_label2.hide()
                self.resultat_label1.hide()
                self.ajouter_resultat_button.hide()

		print 'Le resultat est %s'%result
                if 'error' in result:
                        if result['error']=='Singular matrix':
                                self.error_label.set_text("La matrice saisie n'est pas inversible!")
                        self.error_label.show()
                        return
                elif 'result' in result:
                        
                        if not 'result2' in result and not hasattr(result['result'], "__len__"):

                        	self.resultat_label1.set_text("Resultat: %s"%self.operator)
                        	self.resultat_label1.show()    
		                self.ajouter_resultat_button.hide()
			elif not 'result2' in result and hasattr(result['result'], "__len__"): 
				self.ajouter_resultat_button.show()
				self.set_matrix_data(self.resultat_label1,result['result'])
			else:
					
			        self.set_matrix_data(self.resultat_label1,[[1.5,2.0],[2.5,-3.7]])
			        self.set_matrix_data(self.resultat_label2,[[1.5,2.0],[2.5,-3.7]])
                		
            
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
                        name,m,n,p=dialog.get_object()
                        self.matrix_list[name]=(m,n,p)
                        self.liststore[self.treeiter][1:]=[n,p]
                        """elif response == Gtk.ResponseType.CANCEL :"""
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



