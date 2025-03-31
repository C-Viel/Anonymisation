import fitz  # PyMuPDF pour gérer les PDF
import tkinter as tk
from tkinter import filedialog, messagebox

# Fonction pour caviarder le PDF
def caviarder_pdf(fichier_entree, fichier_sortie, mots_a_caviarder):
    try:
        doc = fitz.open(fichier_entree)

        for page in doc:
            for mot in mots_a_caviarder:
                zones = page.search_for(mot)
                for zone in zones:
                    page.add_redact_annot(zone, fill=(0, 0, 0))  # Ajoute un bloc noir
            page.apply_redactions()  # Applique les caviardages

        # Sauvegarder le fichier anonymisé sous un autre nom
        doc.save(fichier_sortie)

        messagebox.showinfo("Succès", f"PDF anonymisé enregistré sous : {fichier_sortie}")
    except Exception as e:
        messagebox.showerror("Erreur", str(e))

# Fonction pour sélectionner un fichier PDF
def selectionner_fichier():
    fichier = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if fichier:
        entry_fichier.delete(0, tk.END)
        entry_fichier.insert(0, fichier)

# Fonction pour lancer le caviardage
def lancer_caviardage():
    fichier_entree = entry_fichier.get()
    mots_a_caviarder = entry_mots.get().split(",")  # Séparer les mots par des virgules
    # Remplacer "caviarde" par "anonymise" dans le nom du fichier de sortie
    fichier_sortie = fichier_entree.replace(".pdf", "_anonymise.pdf")

    if fichier_entree and mots_a_caviarder:
        caviarder_pdf(fichier_entree, fichier_sortie, mots_a_caviarder)
    else:
        messagebox.showwarning("Attention", "Veuillez sélectionner un fichier et entrer des mots.")

# Interface Graphique
app = tk.Tk()
app.title("Anonymisation PDF")
app.geometry("400x200")

tk.Label(app, text="Sélectionner un fichier PDF :").pack()
entry_fichier = tk.Entry(app, width=50)
entry_fichier.pack()
tk.Button(app, text="Parcourir...", command=selectionner_fichier).pack()

tk.Label(app, text="Mots à anonymiser (séparés par des virgules) :").pack()
entry_mots = tk.Entry(app, width=50)
entry_mots.pack()

tk.Button(app, text="Anonymiser", command=lancer_caviardage).pack()

app.mainloop()
