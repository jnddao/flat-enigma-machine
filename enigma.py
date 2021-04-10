import string
# gets inputs from user
def getInputs():
    sPosition, rotorOrder, code = "", 0, ""
    done = False
    while done == False :
        # starting position
        print("Please enter 3 letter starting position in ALL CAPS: ", end = '')
        sPosition = input()
        
        # rotor order
        print("Please enter rotor order number from left to right (eg 123): ", end = '')
        rotorOrder = input()

        # request coded msg
        print("Please enter coded message in ALL CAPS: ", end = '')

        # Removes spaces and punctuation
        code = code.translate(str.maketrans('', '', string.punctuation))
        code = input().replace(" ", "")

        # double check if input is correct
        if rotorOrder.isnumeric and sPosition.isalpha() and sPosition.isupper() and code.isalpha() and code.isupper() and len(sPosition) is 3:
            done = True
        else:
            print("Input Invalid. Please check input and try again\n\n")

    return sPosition, rotorOrder, code

# get's the next letter of a rotor given the next array being array
# used for both alphabet and random cipher
def getForward(rLetter, array):
    counter = 0
    for letter in array:
        if letter == rLetter:
            break
        else:
            counter += 1
    
    return counter

# gets the reflector given the 'reflectee' 
# reference is the given letter
# ref is the array of letters
# curr is the position currently pointing at
def getRef(reference, ref, curr):
    i = 0
    for char in ref:
        if char == reference and i != curr:
            return i
        else : 
            i += 1

# Given a rotor and the number of times to be rotated, will rotate the rotor
# Rotates by placing index 0 at the end of the array
def rotate(rotor, alphabetRotor, number) :
    counter = 0
    # keeps rotating it until it it is rotated correct number of times
    while counter < number:
        # temp
        firstIndex = rotor[0]
        alphabetFirstIndex = alphabetRotor[0]
        rotor.append(rotor.pop(rotor.index(firstIndex)))
        alphabetRotor.append(alphabetRotor.pop(alphabetRotor.index(alphabetFirstIndex)))
        counter += 1

    return rotor, alphabetRotor

# added one more repetition to rotors to help prevent end of array errors
# only ment for short words and NOT sentences
# removes spaces but does not support full stops
def main() :
    # required rotors and references
    rotor1String = "EKMFLGDQVZNTOWYHXUSPAIBRCJEKMFLGDQVZNTOWYHXUSPAIBRCJ"
    rotor2String = "AJDKSIRUXBLHWTMCQGZNPYFVOEAJDKSIRUXBLHWTMCQGZNPYFVOE"
    rotor3String = "BDFHJLCPRTXVZNYEIWGAKMUSQOBDFHJLCPRTXVZNYEIWGAKMUSQO"
    refString = "ABCDEFGDIJKGMKMIEBFTCVVJAT"
    alphabetArray = "ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ"

    # splitting to avoid long array declarations

    # alphabet section of array
    alp = list(alphabetArray)
    alphabet1 = list(alphabetArray)
    alphabet2 = list(alphabetArray)
    alphabet3 = list(alphabetArray)
    ref = list(refString)
    rotor1 = list(rotor1String)
    rotor2 = list(rotor2String)
    rotor3 = list(rotor3String)
    temp = [[], [], []]

    # added +1 toggles
    toggle1 = [17, 43] 
    toggle2 = [5, 31] 
    toggle3 = [22, 48]
    # temporary 2d array to assign toggles
    tempToggle = [[], [], []]

    # gets the first positions of the rotors 
    # and all other needed user input data
    sPosition, rotorOrder, code = getInputs()

    # sets the starting positions by the static alphabet 
    # assuming doesnt change by rotor
    r1 = ord(sPosition[0]) - 65
    r2 = ord(sPosition[1]) - 65
    r3 = ord(sPosition[2]) - 65

    # rotating rotors to starting position
    rotor1, alphabet1 = rotate(rotor1, alphabet1, r1)
    rotor2, alphabet2 = rotate(rotor2, alphabet2, r2)
    rotor3, alphabet3 = rotate(rotor3, alphabet3, r3)

    # loop to set rotor order
    counter = 0
    for num in list(str(rotorOrder)):
        if num == "1":
            temp[counter] = rotor1.copy()
            tempToggle[counter] = toggle1.copy()
        elif num == "2":
            temp[counter] = rotor2.copy()
            tempToggle[counter] = toggle2.copy()
        elif num == "3":
            temp[counter] = rotor3.copy()
            tempToggle[counter] = toggle3.copy()

        counter += 1
    
    # setting rotor order
    rotor1 = temp[0]
    rotor2 = temp[1]
    rotor3 = temp[2]
    toggle1 = tempToggle[0]
    toggle2 = tempToggle[1]
    toggle3 = tempToggle[2]

    # enigma loop!
    for char in code:
        r3 += 1 # increment 3rd by 1
        rotor3, alphabet3 = rotate(rotor3, alphabet3, 1)
        # check if they all have to be incremented
        if r3 in toggle3: 
            rotor2, alphabet2 = rotate(rotor2, alphabet2, 1) 
            r2 += 1
        if r2 in toggle2: 
            rotor1, alphabet1 = rotate(rotor1, alphabet1,  1)
            r1 += 1
        if r1 in toggle1:
            pass # nothing happens here as r1 is not affeliated with anything
        
        # check if any of the rs are over 51. Will set to 0 otherwise.
        # still need to do edge cases where rotor is at the end or key is greater than array reaches
        if (r3 > 51): r3 = 0
        if (r2 > 51): r2 = 0
        if (r1 > 51): r1 = 0


        # number to keep track of position
        # getFoward is position of alp
        # first half of encryption
        curr = (ord(char) - 65) # get the initial position

        curr = getForward(rotor3[curr], alphabet3)
        curr = getForward(rotor2[curr], alphabet2)
        curr = getForward(rotor1[curr], alphabet1)

        # getting reflection and starting again
        referenceLetter = ref[curr]
        curr = getRef(referenceLetter, ref, curr)
        # second half of encryption
        # gerForward is location of rotor
        curr = getForward(alphabet1[curr], rotor1)
        curr = getForward(alphabet2[curr], rotor2)
        curr = getForward(alphabet3[curr], rotor3)

        # printing
        print("%s" % alp[curr], end = '')
    # end of line
    print ("")


if __name__ == "__main__":
    main()
