from string import *
import re
import tkinter as tk

# Primul criptosistem ales este Substitutia monoalfabetica

def invert_dict(dict):  # este necesara pentru decriptare
    inverse_dict = {}
    for key, value in dict.items():
        inverse_dict[value] = key
    return inverse_dict


def encrypt_mono(mesaj, dict):
    mesaj_criptat = ''
    for letter in mesaj:
        mesaj_criptat += dict[letter.upper()]
    return mesaj_criptat


def decrypt_mono(mesaj, dict):
    return encrypt_mono(mesaj, invert_dict(dict))


# Al doilea criptosistem ales este Cifrul Nihilist
dim_patrat = 5
alfa = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
        'W', 'X', 'Y', 'Z']
poz_i = []
poz_j = []


def patrat_poly(key):
    patrat = []
    ok = 1
    if key:
        # adaugam din cheie
        for i in range(dim_patrat):
            if ok == 1:
                for j in range(dim_patrat):
                    if (i * dim_patrat + j) >= len(key):
                        ok = 0
                        break
                    if key[i * dim_patrat + j] not in patrat:
                        if key[i * dim_patrat + j] in ['I', 'J']:
                            if len(patrat) != 0:
                                okij = 0
                                for k in range(len(patrat)):
                                    if patrat[k] in ['I', 'J']:
                                        okij = 1
                                        break
                                if okij == 0:
                                    patrat.append(key[i * dim_patrat + j])
                            else:
                                patrat.append(key[i * dim_patrat + j])
                        else:
                            patrat.append(key[i * dim_patrat + j])
            else:
                break
    # adaugam alfabetul initial sau ce mai ramane neadaugat din alfabet
    for i in range(dim_patrat):
        for j in range(dim_patrat):
            if alfa[i * dim_patrat + j] not in patrat:
                if alfa[i * dim_patrat + j] in ['I', 'J']:
                    okij = 0
                    for k in range(len(patrat)):
                        if patrat[k] in ['I', 'J']:
                            okij = 1
                            break
                    if okij == 0:
                        patrat.append(alfa[i * dim_patrat + j])
                else:
                    patrat.append(alfa[i * dim_patrat + j])

    return patrat


def cod_lit(text, patrat):
    text_cifrat = []
    for idx in range(0, len(text)):
        ok = 0  # pp ca nu este cifrat
        for i in range(dim_patrat):
            for j in range(dim_patrat):
                if text[idx] == patrat[i * dim_patrat + j] or (
                        text[idx] in ['I', 'J'] and patrat[i * dim_patrat + j] in ['I', 'J']):
                    text_cifrat.append((i + 1) * 10 + (j + 1))
                    ok = 1
                if ok == 1:
                    break
    return text_cifrat


def encrypt_nihi(text, key1, key2):
    patrat = patrat_poly(key1)
    text_cif = cod_lit(text, patrat)
    key2_cif = cod_lit(key2, patrat)
    text_codat = []
    for idx in range(len(text_cif)):
        text_codat.append(text_cif[idx] + key2_cif[idx % len(key2_cif)])
    return text_codat


def decrypt_nihi(text, key1, key2):
    patrat = patrat_poly(key1)
    key2_cif = cod_lit(key2, patrat)
    text_decriptat = ''
    for idx in range(len(text)):
        cod_fara_cheie = text[idx] - key2_cif[idx % len(key2_cif)]
        cod_patrat = int(cod_fara_cheie / 10 - 1) * dim_patrat + cod_fara_cheie % 10 - 1
        text_decriptat += patrat[cod_patrat]
    return text_decriptat


def listTostring(list):
    sir = ""
    for s in list:
        sir += s
    return sir


def criptare(fout, text_clar, alfabet, cheie1, cheie2):
    global mesaj_criptat
    msj_cript1 = encrypt_mono(text_clar, alfabet)
    msj_cript_final = encrypt_nihi(msj_cript1, cheie1, cheie2)
    mesaj_criptat = msj_cript_final

    fout.write("---------------------------------------------Criptare---------------------------------------------")
    fout.write("\nTextul clar este: ")
    fout.write(listTostring(text_clar))
    fout.write("\nTextul dupa prima criptare este: ")
    fout.write(listTostring(msj_cript1))
    fout.write("\nTextul dupa a doua criptare este: ")
    fout.write(listTostring(str(msj_cript_final)))

    # adaug mesaj criptat 1 in entry
    text_cript_1_entry.delete(0, tk.END)
    text_cript_1_entry.insert(0, msj_cript1)
    text_cript_1_entry.config(state='readonly')

    # adaug mesaj criptat final in entry
    text_cript_entry.delete(0, tk.END)
    text_cript_entry.insert(0, msj_cript_final)
    text_cript_entry.config(state='readonly')


def decriptare(fout, text_criptat, alfabet, cheie1, cheie2):

    alfabet_sort = {}
    for i in sorted(alfabet.keys()):
        alfabet_sort[i] = alfabet[i]
    text_decriptat_1 = decrypt_nihi(text_criptat, cheie1, cheie2)
    text_decriptat_final = decrypt_mono(text_decriptat_1, alfabet_sort)

    fout.write("\n\n---------------------------------------------Decriptare---------------------------------------------")
    fout.write("\nTextul criptat este: ")
    fout.write(listTostring(str(text_criptat)))
    fout.write("\nTextul dupa prima decriptare este: ")
    fout.write(listTostring(text_decriptat_1))
    fout.write("\nTextul dupa a doua decriptare este: ")
    fout.write(listTostring(text_decriptat_final))

    # adaug mesaj decriptat 1 in entry
    text_decript_1_entry.delete(0, tk.END)
    text_decript_1_entry.insert(0, text_decriptat_1)
    text_decript_1_entry.config(state='readonly')

    # adaug mesaj decriptat final in entry
    text_decript_entry.delete(0, tk.END)
    text_decript_entry.insert(0, text_decriptat_final)
    text_decript_entry.config(state='readonly')


# Aplicare criptosisteme
window = tk.Tk()
window.title("Project 1")
w, h = window.winfo_screenwidth(), window.winfo_screenheight()
window.geometry("%dx%d+0+0" % (w, h))
title = tk.Label(text="Welcome to my project", foreground="blue")
title.config(font=("Comic Sans MS", 30, 'bold italic'))
title.pack(pady=5)
fin = open("inputpb1.txt", 'r')
TextLines = fin.readlines()

# citesc textul care trebuie criptat
msj = TextLines[1].upper()
# sterg caractere care nu sunt din alfabet
msj_clean = re.sub("[^A-Za-z]", "", msj)
# afisez text initial in GUI
text_init_label = tk.Label(text="Text initial")
text_init_label.config(font=("Rockwell", 20, 'bold'))
text_init_label.pack()
text_init_entry = tk.Entry(width=100, justify="center", font=5)
text_init_entry.insert(0, msj_clean)
text_init_entry.config(state='readonly')
text_init_entry.pack(pady=5)

# citesc alfabet
mono_alfa = dict()  # declaram dictionarul pentru alfabetul cifrului monoalfabetic

mono_poz = []
for idx in range(26):
    mono_poz.append(0)

alfab_citit=TextLines[0].upper()
alfab_citit_clean = re.sub("[^A-Za-z]", "", alfab_citit)
idx_lit = 0
while len(mono_alfa) < 26 and idx_lit < len(alfab_citit_clean):
    for idx in range(26):
        if len(mono_alfa) == 26:  # daca s-au ocupat toate literele din alfabet
            break
        if not bool(mono_alfa):  # daca alfabetul este vid
            mono_alfa[chr(ord('A') + idx)] = alfab_citit_clean[idx_lit]
            mono_poz[idx] = 1
            idx_lit += 1
            break
        else:
            if alfab_citit_clean[idx_lit] not in mono_alfa.values():
                if mono_poz[idx] == 0:
                    mono_alfa[chr(ord('A') + idx)] = alfab_citit_clean[idx_lit]
                    mono_poz[idx] = 1
                    idx_lit += 1
                    break
                else:
                    continue
            else:
                idx_lit += 1

alfabet_sort = {}
for i in sorted(mono_alfa.keys()):
    alfabet_sort[i] = mono_alfa[i]

print(alfabet_sort)
# afisez alfabet in GUI
alfa_mono_label = tk.Label(text="Alfabet Monosubstitutie")
alfa_mono_label.config(font=("Rockwell", 20, 'bold'))
alfa_mono_label.pack()
alfa_mono_entry = tk.Entry(width=50, justify="center", font=5)
list_afis_alfa_mono = []
for i in mono_alfa.keys():
    list_afis_alfa_mono.append(mono_alfa[i])
list_afis_alfa_mono = listTostring(list_afis_alfa_mono)
alfa_mono_entry.insert(0, list_afis_alfa_mono)
alfa_mono_entry.config(state='readonly')
alfa_mono_entry.pack(pady=5)

# citesc cheie alfabet
key1_cit = TextLines[2].upper()
# sterg caractere care nu sunt din alfabet
key1 = re.sub("[^A-Za-z]", "", key1_cit)
# afisez cheie alfabet in GUI
key1_label = tk.Label(text="Cheie 1")
key1_label.config(font=("Rockwell", 20, 'bold'))
key1_label.pack()
key1_entry = tk.Entry(width=100, justify="center", font=5)
key1_entry.insert(0, key1)
key1_entry.config(state='readonly')
key1_entry.pack(pady=5)

# citesc cheie cifrare
key2_cit = TextLines[3].upper()
# sterg caractere care nu sunt din alfabet
key2 = re.sub("[^A-Za-z]", "", key2_cit)
# afisez cheie alfabet in GUI
key2_label = tk.Label(text="Cheie 2")
key2_label.config(font=("Rockwell", 20, 'bold'))
key2_label.pack()
key2_entry = tk.Entry(width=100, justify="center", font=5)
key2_entry.insert(0, key2)
key2_entry.config(state='readonly')
key2_entry.pack(pady=5)

fout = open("outputpb1.txt", 'w')
# mesaj criptat 1 in GUI
text_cript_1_label = tk.Label(text="Text criptat 1")
text_cript_1_label.config(font=("Rockwell", 20, 'bold'))
text_cript_1_label.pack()
global text_cript_1_entry
text_cript_1_entry = tk.Entry(width=100, justify="center", font=5)
text_cript_1_entry.insert(0, "")
text_cript_1_entry.pack()
# mesaj criptat final in GUI
text_cript_label = tk.Label(text="Text criptat final")
text_cript_label.config(font=("Rockwell", 20, 'bold'))
text_cript_label.pack()
global text_cript_entry
text_cript_entry = tk.Entry(width=100, justify="center", font=5)
text_cript_entry.insert(0, "")
text_cript_entry.pack()
cryptbut = tk.Button(text="Encrypt", width=30, height=2, bg="light blue", command=lambda: criptare(fout, msj_clean, mono_alfa, key1, key2), font=5).pack(pady=5)

# mesaj decriptat 1 in GUI
text_decript_1_label = tk.Label(text="Text decriptat o data")
text_decript_1_label.config(font=("Rockwell", 20, 'bold'))
text_decript_1_label.pack()
global text_decript_1_entry
text_decript_1_entry = tk.Entry(width=100, justify="center", font=5)
text_decript_1_entry.insert(0, "")
text_decript_1_entry.pack()
# mesaj decriptat final in GUI
text_decript_label = tk.Label(text="Text decriptat final")
text_decript_label.config(font=("Rockwell", 20, 'bold'))
text_decript_label.pack()
global text_decript_entry
text_decript_entry = tk.Entry(width=100, justify="center", font=5)
text_decript_entry.insert(0, "")
text_decript_entry.pack()
decryptbut = tk.Button(text="Decrypt", width=30, height=2, bg="light green", command=lambda: decriptare(fout, mesaj_criptat, mono_alfa, key1, key2), font=5).pack(pady=5)

window.mainloop()
fin.close()
fout.close()