
def calc_rank(age, is_veteran=False, has_disability=False):
    """
    Calculate a participant's rank. A higher number is higher ranked (top of the list).
    (i.e., Reverse this when sorting.)

    Change this function to change the ranking algorithm.
    """

    # base factor is 1.0
    factor = 1.0

    # adjust for age based on research
    if age < 30:
        factor *= 1
    elif age < 40:
        factor *= 1.04
    elif age < 50:
        factor *= 1.63
    elif age < 60:
        factor *= 2.7
    elif age < 70:
        factor *= 4.28
    else:
        # any age 70 and up
        factor *= 11.67

    if is_veteran:
        # based on research
        factor *= 1.33
    if has_disability:
        # research not available
        factor *= 1.5

    # result is a number between 1 and about 23
    return factor
