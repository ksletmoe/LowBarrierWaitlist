
def calc_rank(age, is_veteran=False, has_disability=False):
    """
    Calculate a participant's rank. A higher number is higher ranked (top of the list).
    (i.e., Reverse this when sorting.)

    Change this function to change the ranking algorithm.
    
    The code in the comments below is a ranking system based on mortality vulerability, as described in several research papers namely:
    http://journals.plos.org/plosone/article?id=10.1371/journal.pone.0073979
    http://journals.plos.org/plosone/article?id=10.1371/journal.pone.0073979
    
    This code cannot currently be used to to a JOHS agreement regarding this ranking system but should be argued for in the future as it
    has a scientific basis.
    
    # This is the base vulnerability score
    factor = 1.0

    age_multiplier = {
        range(0, 30): 1,
        range(30, 40): 1.04,
        range(40, 50): 1.63,
        range(50, 60): 2.7,
        range(60, 70): 4.28,
        range(70, 120): 11.67
    }

    # find and apply the age rr multiplier
    factor *= [age_multiplier[key] for key in age_multiplier if age in key][0]

    # is the participant a vet? Apply the vet rr multiple
    if is_veteran:
        factor *= 1.33

    # is the participant disabled? Apply the disabled rr multipler
    if has_disability:
        factor *= 1.5

    # result is a number between 1 and about 22
    return factor
    """
    
    age_points = 0
    # over 55? add more points
    if age >= 55:
        age_points += 1

    vet_points = 1
    dis_points = 1

    points = age_points
    if is_veteran:
        points += vet_points
    if has_disability:
        points += dis_points

    # result is a number between 0 and 3
    return points
