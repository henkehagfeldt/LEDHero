letters = ['a', 'a#', 'b', 'c', 'c#', 'd', 'd#', 'e', 'f', 'f#', 'g', 'g#']

def get_tone(let, num):
    print(letters[(letters.index(let)+num)%(len(letters))])
