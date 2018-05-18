
def calc_rank(age, is_veteran=False, has_disability=False):
    """
    Calculate a participant's rank. A higher number is higher ranked (top of the list).
    (i.e., Reverse this when sorting.)

    Change this function to change the ranking algorithm.
    """

    age_points = 0
    # over 55? add more points
    if age >= 55:
        age_points += 10
    # over 65? add even more points (this is cumulative with the above)
    if age >= 65:
        age_points += 15

    vet_points = 10
    dis_points = 15

    points = age_points
    if is_veteran:
        points += vet_points
    if has_disability:
        points += dis_points

    return points
