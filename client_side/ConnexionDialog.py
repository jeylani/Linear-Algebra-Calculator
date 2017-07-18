import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class ConnexionDialog:
	def __init__(self,parent=None):
        	self.builder=Gtk.Builder()
        	self.builder.add_from_file('./glade/ConnexionDialog.glade')
        	self.dialog=self.builder.get_object('dialog')
        	self.dialog.set_transient_for(parent)
        	
        	self.valider_button=self.dialog.add_button('Valider',Gtk.ResponseType.OK)
        	self.cancel_button=self.dialog.add_button('Annuler',Gtk.ResponseType.CANCEL)
        	
        	self.entry=self.builder.get_object("entry")
        	self.spinbutton=self.builder.get_object("spinbutton")
        
        def run(self):
        	return self.dialog.run()
    	def destroy(self):
        	self.dialog.destroy()
        def show_error(self):
        	error_box=self.builder.get_object("error_box")
        	error_box.show_all()
        def get_address(self):
        	ip=self.entry.get_text()
        	port=self.spinbutton.get_value_as_int()
        	return (ip,port)
