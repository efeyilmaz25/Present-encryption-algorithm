"""
Author: Efe Yılmaz Taşyürek


=================Little information about Present======================
This cipher is a SPN but, interestingly, it was not inspired by the AES.
Indeed, while many SPN-based ciphers have permutation layers close in
structure to that of the AES (see LED or mCrypton), that of PRESENT is
completely different: it is bit oriented and is rather simple. It can be
implemented in hardware using simple wiring. However, since bit-oriented
permutations are not software-friendly, the target of PRESENT is clearly
a hardware implementation. Its S-box was selected for its good
cryptographic properties as well as for its small hardware footprint.

Source:https://www.cryptolux.org/index.php/Lightweight_Block_Ciphers#PRESENT
"""

import random
import sys

s_box = {"input": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
         "output": [12, 5, 6, 11, 9, 0, 10, 13, 3, 14, 15, 8, 4, 7, 1, 2]}

random_numbers = [random.randint(0, 15) for _ in range(32)]

def show_sBox():
    print("s-box to be used for encryption:", s_box)

def show_random_numbers():
    print("32-bit data to be encrypted:", random_numbers)

def show_personal_data(data):
    print("32-bit data to be encrypted:", data)


def substitution_box(random_numbers, s_box, info):
    s_box_outputs = [s_box["output"][s_box["input"].index(num)] for num in random_numbers]
    s_box_outputs_binary = [bin(num)[2:].zfill(4) for num in s_box_outputs]

    if(info==True):
        # print results
        print("Input:", random_numbers)
        print("Output:", s_box_outputs)
        print("4 bit results:", s_box_outputs_binary)

    bit_128(s_box_outputs_binary, info)

def bit_128(s_box_outputs_binary, info):
    diffusion_first = ""
    diffusion_last = ""
    str_128bit = ""

    for i in s_box_outputs_binary:
        str_128bit += i

    if(info==True):
        print("128 bit: ", str_128bit)
        print("lenght: ", len(str_128bit))

    str_first64 = ""
    str_last64 = ""

    str_first64 = str_128bit[:64]
    str_last64 = str_128bit[64:]

    if(info==True):
        print("First 64 bit:", str_first64)
        print("Last 64 bit:", str_last64)

    diffusion_first = layer(str_first64)
    diffusion_last = layer(str_last64)
    show_diffusion_results(diffusion_first, diffusion_last, info)


def layer(data):
    diffused_str = ""
    diffused_bit = 0

    for i in range(len(data)):
        if i == 63:
            diffused_bit = data[63]
        else:
            diffused_bit = data[(16 * i) % 63]

        diffused_str += str(diffused_bit)

    return diffused_str


def show_diffusion_results(diffusion_first, diffusion_last, info):
    list_of_128bitdiffusion = []
    variable = []

    if(info==True):
        print("diffusion first 64 bit result: ", diffusion_first)
        print("diffusion last 64 bit result: ", diffusion_last)

    diffusion_128bit = diffusion_first + diffusion_last

    if(info==True):
        print("diffusion result 128bit: ", diffusion_128bit)

    list_of_128bitdiffusion = list(diffusion_128bit)
    variable = list_of_128bitdiffusion.copy()

    xor_128bitdiffusion(diffusion_128bit, variable, info)


def xor_gate(first, last):
    if(first != last):
        result = 1
    else:
        result = 0

    return result

def xor_128bitdiffusion(diffusion_128bit, variable, info):

    for i in range(len(diffusion_128bit)):
        if i == 0:
            continue

        if diffusion_128bit[i - 1] == '0':
            first = 0
        else:
            first = 1
        if diffusion_128bit[i] == '0':
            last = 0
        else:
            last = 1

        result = xor_gate(first, last)
        variable[i] = str(result)

    show_xor_result(variable, info)



def show_xor_result(variable, info):
    xor_result_128bit = ""
    chiper_text = ""

    for i in variable:
        xor_result_128bit += i

    if(info==True):
        print("XOR result 128 bit: ", xor_result_128bit)

    chiper_text = convert_to_hex(xor_result_128bit)
    show_chiper_text(chiper_text)

def convert_to_hex(data):
    temp = hex(int(data, 2))[2:]
    return temp.zfill(len(data) // 4)

def show_chiper_text(chiper_text):
    print("Chiper text:", chiper_text)

def get_personal_data():
    personal_data = []
    print("Enter data between 0 and 15")
    for i in range(32):
        singular_entry = input()
        while (singular_entry.isdigit() != True):
            singular_entry = input("Please enter number:")

        singular_entry = int(singular_entry)

        while ((int(singular_entry) < 0) or (int(singular_entry) > 15)):
            singular_entry = input("The number you enter must be between 0 and 15. Try again:")

        singular_entry = int(singular_entry)
        personal_data.append(singular_entry)
    return personal_data


while True:
    print("\n")
    print("1-)Encrypt random numbers")
    print("2-)Encrypt your own data")
    print("3-)Press 3 to exit")
    selection1 = int(input("Make your choice: "))

    if(selection1 == 1):
        show_sBox()
        show_random_numbers()
        selection2 = str(input("If you want to get information about the encryption steps, enter True, otherwise enter False: "))

        while ((selection2 != "True") and (selection2 != "False") and (selection2 != "true") and (selection2 != "false")):
            selection2 = str(input("You entered incorrectly. Enter True or False:"))

        selection2 = selection2.capitalize()
        if (selection2 == "False"):
            selection2 = 0
        elif (selection2 == "True"):
            selection2 = 1
        selection2 = bool(selection2)
        substitution_box(random_numbers, s_box, selection2)

    elif(selection1 == 2):
        show_sBox()
        personal_data = get_personal_data()

        selection2 = str(input("If you want to get information about the encryption steps, enter True, otherwise enter False: "))

        while ((selection2 != "True") and (selection2 != "False") and (selection2 != "true") and (
                selection2 != "false")):
            selection2 = str(input("You entered incorrectly. Enter True or False:"))


        selection2 = selection2.capitalize()
        if(selection2 == "False"):
            selection2 = 0
        elif(selection2 == "True"):
            selection2 = 1
        selection2 = bool(selection2)

        show_personal_data(personal_data)
        substitution_box(personal_data, s_box, selection2)

    elif(selection1 == 3):
        sys.exit(1)
    else:
        print("You entered incorrectly, try again.")


