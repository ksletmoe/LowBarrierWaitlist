from low_barrier_waitlist.ranker import calc_rank

if __name__ == "__main__":
    samples = [
        {"age": 48, "vet": False, "dis": False},
        {"age": 55, "vet": False, "dis": False},
        {"age": 56, "vet": True, "dis": False},
        {"age": 48, "vet": False, "dis": True},
        {"age": 65, "vet": False, "dis": True},
        {"age": 40, "vet": True, "dis": True},
        {"age": 75, "vet": True, "dis": True},
    ]
    print("Samples:")
    for s in samples:
        r = calc_rank(s["age"], s["vet"], s["dis"])
        print(
            "  Age: {}{}{} \t==> Rank: {}".format(
                s["age"],
                ", is a veteran" if s["vet"] else "              ",
                ", has a disability" if s["dis"] else "                  ",
                r,
            )
        )
