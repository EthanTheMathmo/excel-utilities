import re
import string

def convert_to_tuple(cell_address):
    """
    Converts from Excel A1 stype notation to cartesian (1,1) styple notation

    e.g. converts A1 to (1,1), converts AC1 to (1*26 + 3,1) DE1 to (4*26+5,1), CZE to (3*26^2 + 26*26^1 + 5*26^0)
    bit of a headache, but with some messing about it makes sense!
    """
    letters = re.search("[A-Z]{1,}",cell_address).group()
    numbers = re.search("[0-9]{1,}",cell_address).group()
    return (sum([(ord(x[1])-64)*26**x[0] for x in enumerate(reversed(letters))]), int(numbers))

digs = "0" + string.ascii_letters[-26:]
#from SO
def int2base(x, base):
    """
    function from SO. Benefit that it works. Was a bit lazy to take it but oh well
    """
    if x < 0:
        sign = -1
    elif x == 0:
        return digs[0]
    else:
        sign = 1

    x *= sign
    digits = []

    while x:
        digits.append(digs[int(x % base)])
        x = int(x / base)

    if sign < 0:
        digits.append('-')

    digits.reverse()

    return ''.join(digits)

def convert_base_26_to_base_26_no_zero(num):
    #num should be a string, with no zero at the front
    for index, dig in enumerate(num):
        if dig=="0":
            prev_char = num[index-1]
            if prev_char != "A":
                #e.g. C0D goes to BZD, and we perform the step again on BZD
                #e.g. AFC0A0 would go to AFBZA0, and then we run the function on AFBZA0
                return convert_base_26_to_base_26_no_zero(num[:index-1]+chr(ord(num[index-1])-1)+"Z"+num[index+1:])
            else:
                #the previous character was an A, in which case things are different:
                #A0 goes to 0Z
                #e.g. BA0 goes to B0Z, and then we perform the recusrive step
                if index-1 == 0:
                    #e.g. A00ZZ, we convert to Z0ZZ
                    return convert_base_26_to_base_26_no_zero("Z"+num[2:])
                else:
                    #not at start, so there are characters in front of it, e.g. AA0 or BXASA0A
                    #recall, num[index-1] = "A" currently
                    return convert_base_26_to_base_26_no_zero(num[:index-1]+ "0" + "Z" + num[index+1:])
                
        else:
            pass
    return num

def convert_from_tuple(tuple_address):
    """
    Takes a cell, say, (1,1) and returns it in excel notation A1
    """
    return convert_base_26_to_base_26_no_zero(int2base(tuple_address[0],26))+str(tuple_address[1])


def block_to_list(block_address):
    """
    E.g., converts $A$1:$B$2 to $A$1,$A$2,$B$1,$B$2
    """
    first_and_last = block_address.split(":")

    if len(first_and_last) == 1:
        #i.e. is just a single cell passed in.
        #we cover this case to deal with edge cases where a user's 
        #block selection is just a single cell
        return block_address

    first = first_and_last[0]
    last = first_and_last[1]
    first_tuple = convert_to_tuple(first)
    last_tuple = convert_to_tuple(last)
    return ",".join([",".join([convert_from_tuple((i,j)) for j in range(first_tuple[1], last_tuple[1]+1)]) for i in range(first_tuple[0], last_tuple[0]+1)])


def AZ_to_base10(address):
    """converts from AZ notation to a normal number (written in base 10)"""
    return sum([(ord(x[1])-64)*26**x[0] for x in enumerate(reversed(address))])

def char_lim_255(address):
    """
    breaks a string of addresses into ones which are sub<255 chars

    Used in, for example, color_cells, in case the range selected has addresses of length >=255 chars
    """

    if len(address) > 255:
        for i in reversed(range(256)):
            if address[i] == ",":
                return [address[:i]] + char_lim_255(address[i+1:])
            else:
                pass
    else:
        return [address]



def next_down(cell_address):
    """
    given a cell, say, $B$6, this returns the address of the next cell down, in this example, $B$7
    """
    address_split = cell_address.split("$")
    address_split[-1] = str(int(address_split[-1])+1)
    return "$".join( address_split)

def next_along(cell_address):
    """
    Given a cell, say, $B$6, returns the next cell along, in this case, $C$6
    """
    cell_tuple = convert_to_tuple(cell_address)
    return convert_from_tuple((cell_tuple[0]+1, cell_tuple[1]))


def adding_one(x):
    return x+1