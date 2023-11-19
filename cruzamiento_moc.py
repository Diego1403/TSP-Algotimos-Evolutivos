

def cruzamiento_MOC(s1, s2,random):
    # Determine the crossover point
    crossover_point = random.randint(1, len(s1) - 2)

    # Select the right substrings from the crossover point
    right_s1 = s1[crossover_point:]
    right_s2 = s2[crossover_point:]

    # Initialize child strings with placeholders
    b1 = ['*'] * len(s1)
    b2 = ['*'] * len(s2)

    # Place the right substrings into the children
    b1[crossover_point:] = right_s1
    b2[crossover_point:] = right_s2

    # Fill in the left part of the children
    fill_left_part(b1, s2, crossover_point)
    fill_left_part(b2, s1, crossover_point)

    return b1, b2

def fill_left_part(child, parent, crossover_point):
    # Fill in the elements from the parent string into the child
    fill_index = 0
    for element in parent:
        if element not in child:
            if fill_index == crossover_point:
                fill_index += len(child) - crossover_point
            child[fill_index] = element
            fill_index += 1

