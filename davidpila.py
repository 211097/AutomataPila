import re
import tkinter as tk
from tkinter import scrolledtext

class PDA:
    def __init__(self, grammar, terminals):
        self.grammar = grammar
        self.terminals = terminals
        self.stack = []
        self.stack_history =[]


    # automata de pila
    def parse(self, inbound_string):
        self.stack.append("S")  # Símbolo de inicio
        print("Pila:", self.stack)
        self.stack_history.append("Pila inicial: " + str(self.stack))
        index = 0
        while self.stack and index <= len(inbound_string):
            # print("Pila:", self.stack)
            index = self.skip_whitespace(
                inbound_string, index
            )  # Saltar espacios en blanco
            if index >= len(inbound_string):
                break

            top = self.peek()
            remaining_input = inbound_string[index:]

            if top in self.grammar:
                self.process_non_terminal(top, remaining_input)
            elif self.match_terminal(top, remaining_input):
                match_length = len(
                    re.match(self.terminals[top], remaining_input).group()
                )
                index += match_length
                self.pop()
            else:
                raise Exception(f"Error de sintaxis cerca de la posición {index}")
            self.stack_history.append("Pila inicial: " + str(self.stack))
            print("Pila:", self.stack)
        return len(self.stack) == 0

    def process_non_terminal(self, non_terminal,inbound_string ):
        self.pop()

        if non_terminal == "S":
            self.choose_production_for_S(inbound_string)
        elif non_terminal == "D":
            self.choose_production_for_D(inbound_string)
        elif non_terminal == "V":
            self.push_production(self.grammar["V"][0])
        else:
            # Para otros no terminales NT
            self.choose_production(non_terminal, inbound_string)

    # FUNCIONES PARA AYUDAR A ELEGIR OPCIONES DE LAS REGLAS

    def choose_production_for_D(self, inbound_string):
        if re.match(self.terminals["X0"], inbound_string):
            self.push_production(self.grammar["D"][0])
        elif re.match(self.terminals["Y0"], inbound_string):
            self.push_production(self.grammar["D"][1])

    def choose_production_for_S(self, inbound_string):
        if re.match(self.terminals["A"], inbound_string):
            self.push_production(self.grammar["S"][0])  # "A B"
        elif re.match(self.terminals["K"], inbound_string):
            self.push_production(self.grammar["S"][1])  # "K L"
        elif re.match(self.terminals["H1"], inbound_string):
            self.push_production(self.grammar["S"][2])  # "H1 H2"
        elif re.match(self.terminals["G1"], inbound_string):
            self.push_production(self.grammar["S"][3])  # "G1 G2"
        else:
            raise Exception(
                f"No se pudo encontrar una producción adecuada para 'S' con entrada {inbound_string}"
            )

        # self.push_production(self.grammar["S"][0])

    def choose_production(self, non_terminal, inbound_string):
        for production in self.grammar[non_terminal]:
            if self.is_valid_production(production, inbound_string):
                self.push_production(production)
                return
        raise Exception(
            f"No se pudo encontrar una producción adecuada para {non_terminal} con entrada {inbound_string}"
        )

    def is_valid_production(self, production, inbound_string):
        symbols = production.split()
        if not symbols:
            return False
        first_symbol = symbols[0]
        if first_symbol in self.terminals:
            return re.match(self.terminals[first_symbol], inbound_string) is not None
        else:
            return False

    def push_production(self, production):
        for symbol in reversed(production.split()):
            self.push(symbol)

    def skip_whitespace(self, inbound_string, index):
        while index < len(inbound_string) and inbound_string[index].isspace():
            index += 1
        return index

    def match_terminal(self, terminal, inbound_string):
        pattern = self.terminals[terminal]
        return re.match(pattern, inbound_string)

    def push(self, symbol):
        if symbol != "ε":  # ε representa la cadena vacía
            self.stack.append(symbol)

    def pop(self):
        return self.stack.pop()

    def peek(self):
        return self.stack[-1] if self.stack else None


terminals = {
    "A": r"[A-Z]",
    "LET": r"[a-z]*",
    "NUM": r"[0-9]+",
    "X0": r"int",
    "Y0": r"str",
    "F": r"/=",
    "I": r'"',
    "K": r"for",
    "M": r"\(",
    "T": r"\;",
    "W": r"(<|>|=<|=>|==)",
    "Z4": r"\++",
    "Z6": r"\)",
    "Z8": r"\{",
    "Z10": r"contenido",
    "Z11": r"\}",
    "H1": r"if",
    "H12": r"else",
    "G1": r"fun",
}

# Gramática de ejemploo
grammar = {
    "S": ["A B", "K L", "H1 H2", "G1 G2"],  # PX
    "B": ["LET D"],  # B
    "D": ["X0 X1", "Y0 Y1"],
    "X1": ["F NUM"],
    "Y1": ["F H"],
    "H": ["I J"],
    "J": ["LET I"],
    "L": ["M N"],  # for
    "N": ["A O"],
    "O": ["X0 P"],
    "P": ["F Q"],
    "Q": ["NUM R"],
    "R": ["T U"],
    "U": ["A V"],
    "V": ["W Z0"],
    "Z0": ["NUM Z1"],
    "Z1": ["T Z2"],
    "Z2": ["A Z3"],
    "Z3": ["Z4 Z5"],
    "Z5": ["Z6 Z7"],
    "Z7": ["Z8 Z9"],
    "Z9": ["Z10 Z11"],
    "H2": ["M H3"],
    "H3": ["A H4"],
    "H4": ["LET H5"],
    "H5": ["W H6"],
    "H6": ["NUM H7"],
    "H7": ["Z6 H8"],
    "H8": ["Z8 H9"],
    "H9": ["Z10 H10"],
    "H10": ["Z11 H11"],
    "H11": ["H12 H13"],
    "H13": ["Z8 H14"],
    "H14": ["Z10 Z11"],
    "G2": ["LET G3"],
    "G3": ["M G4"],
    "G4": ["Z6 G5"],
    "G5": ["Z8 G6"],
    "G6": ["Z10 Z11"],
}



def analyze():
    inbound_string = text_area.get("1.0", tk.END)
    pda = PDA(grammar, terminals)
    valid = pda.parse(inbound_string)

    # Mostrar el historial de la pila
    stack_HistTXT = "\n".join(pda.stack_history)
    stack_history.config(state=tk.NORMAL)  # Habilitar edición para actualizar
    stack_history.delete("1.0", tk.END)  # Borrar contenido anterior
    stack_history.insert(tk.END, stack_HistTXT)  # Insertar historial de la pila
    stack_history.config(state=tk.DISABLED)  # Deshabilitar edición

    if valid:
        result.config(text="La cadena está correctamente escrita.")
    else:
        result.config(text="La cadena no está correctamente escrita.")

# Creación de la ventana principal
vent = tk.Tk()
vent.title("Pila AAA")
vent.configure(background='#7c1324')

# Input section (column 1)
input_S1 = tk.Frame(vent)
input_S1.grid(row=0, column=0, padx=10, pady=10)

text_label = tk.Label(input_S1, text="Ingrese su cadena:",)
text_label.pack()

# Text area for input
text_area = scrolledtext.ScrolledText(input_S1, wrap=tk.WORD, height=5,bg="olive drab", font="Helvetica 15 bold")
text_area.pack()

# Analyze button
confirm_button = tk.Button(input_S1, text="Analizar Cadena", command=analyze)
confirm_button.pack(pady=5)

# Result section (column 2)
result_S2 = tk.Frame(vent)
result_S2.grid(row=0, column=1, padx=10, pady=10)

# Stack history area
stack_history = scrolledtext.ScrolledText(result_S2, wrap=tk.WORD, height=25, state=tk.DISABLED,bg="olive drab", font="Helvetica 25 bold")
stack_history.pack()

# Result label
result = tk.Label(result_S2, text="")
result.pack(pady=10)

# Run the application
vent.mainloop()