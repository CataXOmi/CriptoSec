import tkinter as tk
import sympy
import random
from bitstring import BitStream, BitArray

x = random.randint(3, 3*10**10)
y = random.randint(4, 4*10**10)


def cmmdc(a, b):
    while b > 0:
        a = b
        b = a % b
    return a


def choose_prime(x):
    p = sympy.nextprime(x)
    while p % 4 != 3:
        p = sympy.nextprime(p)
    return p


def choose_seed(p, q):
    seed = random.randint(2, 10**10)
    while seed % p == 0 and seed % q == 0:
        seed = random.randint(2, 10**10)
    return seed


def check_size():
    # alegem bitul cel mai putin semnificativ si facem conversie MB in biti, astfel nr_bits e practic numarul de numere
    global nr_bits
    try:
        nr_bits = int(user_input.get())*8388608
    except ValueError:
        print('Please enter an integer')
    print(nr_bits)


def generate(fout, x, M):
    bit_output = ""
    for ceva in range(nr_bits):
        x = (x * x) % M
        lsbit = x % 2
        bit_output += str(lsbit)
    fout.write(bit_output.encode('ascii'))


p = choose_prime(x)
q = choose_prime(y)
while p == q:
    p = choose_prime(x)
    q = choose_prime(y)
M = p*q
seed = choose_seed(p, q)

# GUI title
window = tk.Tk()
user_input = tk.StringVar()
window.title("Project 2")
w, h = window.winfo_screenwidth(), window.winfo_screenheight()
window.geometry("%dx%d+0+0" % (w, h))
title = tk.Label(text="Welcome to my project", foreground="green")
title.config(font=("Comic Sans MS", 30, 'bold italic'))
title.pack(pady=5)

# GUI INFO
info = tk.Label(text="To use the generator, type the numerical value in the box and press the Get Size button, then the Generate button", foreground="purple")
info.config(font=("Rockwell", 20, 'bold italic'))
info.pack(pady=5)

# GUI size
nr_bits = 0
size_label = tk.Label(text="Size(MB)")
size_label.config(font=("Rockwell", 20, 'bold'))
size_label.pack()
size_entry = tk.Entry(width=100, justify="center", font=5, textvariable=user_input)
size_entry.pack(pady=5)
size_but = tk.Button(text='Get Size', width=30, height=2, bg="light blue", command=check_size, font=5).pack(pady=5)

# GUI generate
fout = open("outputpb2.txt", "wb")
generate_but = tk.Button(text='Generate', width=30, height=2, bg="light green", command=lambda: generate(fout, seed, M), font=5).pack(pady=5)

# GUI Datas
info_p = tk.Label(text="p", foreground="red")
info_p.config(font=("Rockwell", 20, 'bold'))
info_p.pack(pady=5)
info_p_entry = tk.Entry(width=100, justify="center", font=5)
info_p_entry.insert(0, p)
info_p_entry.config(state='readonly')
info_p_entry.pack(pady=5)

info_q = tk.Label(text="q", foreground="red")
info_q.config(font=("Rockwell", 20, 'bold'))
info_q.pack(pady=5)
info_q_entry = tk.Entry(width=100, justify="center", font=5)
info_q_entry.insert(0, q)
info_q_entry.config(state='readonly')
info_q_entry.pack(pady=5)

info_M = tk.Label(text="M", foreground="red")
info_M.config(font=("Rockwell", 20, 'bold'))
info_M.pack(pady=5)
info_M_entry = tk.Entry(width=100, justify="center", font=5)
info_M_entry.insert(0, M)
info_M_entry.config(state='readonly')
info_M_entry.pack(pady=5)

info_seed = tk.Label(text="Seed", foreground="red")
info_seed.config(font=("Rockwell", 20, 'bold'))
info_seed.pack(pady=5)
info_seed_entry = tk.Entry(width=100, justify="center", font=5)
info_seed_entry.insert(0, seed)
info_seed_entry.config(state='readonly')
info_seed_entry.pack(pady=5)

window.mainloop()
fout.close()