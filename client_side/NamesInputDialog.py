import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class NamesInputDialog:
    def __init__(self,parent=None,twice=False):
    	self.twice=twice
        self.builder=Gtk.Builder()
        self.builder.add_from_file("./glade/NamesInputDialog.glade")
        self.dialog=self.builder.get_object('dialog')
	self.dialog.set_transient_for(parent)
        self.valider_button=self.dialog.add_button('Valider',Gtk.ResponseType.OK)
        self.cancel_button=self.dialog.add_button('Annuler',Gtk.ResponseType.CANCEL)

        self.label1=self.builder.get_object("label1")
        self.entry1=self.builder.get_object("entry1")

        self.label2=self.builder.get_object("label2")
        self.entry2=self.builder.get_object("entry2")

        self.label1.set_text('Nom du premier resultat')

        if twice:
            self.label2.set_text('Nom du deuxieme resultat')
        else:
            self.label2.hide()
            self.entry2.hide()

    def run(self):
        return self.dialog.run()
    def destroy(self):
        self.dialog.destroy()
    def get_names(self):
        name=self.entry1.get_text()
        
	if self.twice:
		name2=self.entry2.get_text()
        	return (name,name2)
	else:
		return (name,None)




