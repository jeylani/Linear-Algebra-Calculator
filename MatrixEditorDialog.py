import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class MatrixEditorDialog:
    def __init__(self,name='?',data=[],nbLigne=2, nbCol=2,parent=None):
        self.col=nbCol
        self.builder=Gtk.Builder()
        self.builder.add_from_file("MatrixEditorDialog.glade")
        self.dialog=self.builder.get_object('dialog')
        self.dialog.set_transient_for(parent)
        self.save_button=self.dialog.add_button('Enregistrer',Gtk.ResponseType.OK)
        self.cancel_button=self.dialog.add_button('Annuler',Gtk.ResponseType.CANCEL)
        self.matrix_grid=self.builder.get_object("matrix_grid")
        self.row_spinbutton=self.builder.get_object("row_spinbutton")
        self.row_spinbutton.connect("value-changed",self.on_row_changed)
        self.row_spinbutton.set_value(nbLigne)
        self.col_spinbutton=self.builder.get_object("col_spinbutton")
        self.col_spinbutton.connect("value-changed",self.on_col_changed)
        self.col_spinbutton.set_value(self.col)
        self.name_entry=self.builder.get_object("name_entry")

        self.name_entry.set_text(name)
        if name!='?' and len(data):
            self.name_entry.set_sensitive(False)
            self.label=self.builder.get_object("label")
            self.label.set_text("Edition d'une matrice ou vecteur")
        self.row=0
        self.add_rows(nbLigne,data)
    def position(self,i,j):
        return i*self.col+j
    def run(self):
        return self.dialog.run()
    def destroy(self):
        self.dialog.destroy()
    def get_object(self):
        n=self.row
        p=self.col
        name=self.name_entry.get_text()
        m=[]
        for j in range(p):
            for i in range(n):
                entry=self.matrix_grid.get_child_at(j,i)
                m.append(float(entry.get_text()))
        return name,m,n,p
    def create_entry(self,text):
        entry=Gtk.Entry()
        entry.set_text(text)
        entry.set_max_width_chars (10)
        entry.set_width_chars(10)
        entry.show()
        return entry
    def add_rows(self,n,data=[]):
        for i in range(n):
            self.matrix_grid.insert_row(self.row)
            for j in range(self.col):
                entry=self.create_entry("0")
                pos=self.position(i,j)
                if pos<len(data):
                    entry.set_text(str(data[pos]))
                self.matrix_grid.attach(entry,j,self.row,1,1) 
            self.row+=1
    def add_columns(self,n,data=[]):
        for j in range(n):
            self.matrix_grid.insert_column(self.col)
            for i in range(self.row):
                entry=self.create_entry("0")
                pos=self.position(i,j)
                if pos<len(data):
                    entry.set_text(str(data[pos]))
                self.matrix_grid.attach(entry,self.col,i,1,1) 
            self.col+=1
    def diminuer_row(self):
        self.matrix_grid.remove_row(self.row-1)
        self.row-=1
    def diminuer_col(self):
        self.matrix_grid.remove_column(self.col-1)
        self.col-=1        
    def on_row_changed(self, spinbutton):
        value=spinbutton.get_value_as_int()
        if value>self.row:
            self.add_rows(value-self.row) 
        elif value<self.row:
            self.diminuer_row()   
    def on_col_changed(self, spinbutton):
        value=spinbutton.get_value_as_int()
        if value>self.col:
            self.add_columns(value-self.col)
        elif value<self.col:
            self.diminuer_col()





