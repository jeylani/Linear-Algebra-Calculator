import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class BaseEditionDialog:
	def __init__(self,base=[],dim=2,parent=None):
		self.cmp=0
		self.dim=dim
		self.base=base
		self.builder=Gtk.Builder()
		self.builder.add_from_file("./glade/BaseEditionDialog.glade")
		self.dialog=self.builder.get_object('dialog')
		self.dialog.set_transient_for(parent)
		self.dialog.add_button('Valider',Gtk.ResponseType.OK)
		self.dialog.add_button('Annuler',Gtk.ResponseType.CANCEL)

		self.error_label=self.builder.get_object("error_label")
		self.error_label.hide()
		spinbutton=self.builder.get_object("spinbutton")
		spinbutton.set_value(dim)
		spinbutton.connect("value-changed",self.on_spinbutton_value_changed)
		
		self.treeview=self.builder.get_object("treeview")
		self.liststore=Gtk.ListStore(str,int,bool)
		for item in base:
			if item[1]==dim:
				self.liststore.append(item)
				if item[1]==True:
					self.cmp+=1
			item[2]=False
		
		self.treeview.set_model(self.liststore)
		renderer=Gtk.CellRendererText()
		column=Gtk.TreeViewColumn("Nom",renderer,text=0)
		self.treeview.append_column(column)
		
		renderer_toggle=Gtk.CellRendererToggle()
		renderer_toggle.connect("toggled",self.on_cell_toggled)
		column=Gtk.TreeViewColumn("Selectionner",renderer_toggle,active=2)
		self.treeview.append_column(column)
		
	def on_spinbutton_value_changed(self,spinbutton):
		self.liststore.clear()
		self.cmp=0
		self.error_label.hide()
		self.dim=spinbutton.get_value_as_int()
		for item in self.base:
			if item[1]==self.dim:
				self.liststore.append(item)
	def on_cell_toggled(self,renderer_toggle, path):
		if self.liststore[path][2]==False:
			if self.cmp<self.dim:
				self.cmp+=1
				self.liststore[path][2]=True
			else:
				self.error_label.show()
				self.error_label.set_text("Vous avez coche le maximum de vecteurs!"+
				"\nVeuillez cliquer sur valider ou decocher un vecteur")	
		else:
			self.error_label.hide()
			self.cmp-=1
			self.liststore[path][2]=False
			
	def run(self):
		return self.dialog.run()
	def destroy(self):
		self.dialog.destroy()
	def get_selected(self):
		selected=list()
		for row in self.liststore:
			if row[2]==True:
				selected.append(row[0])
		return selected

    
          


