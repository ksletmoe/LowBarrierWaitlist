from low_barrier_waitlist.rank_calculator import calc_rank


class Ranker:
    """
    :param participants: [Participant]
    create with list of Participant records.
    After creating, get ranker.ranked_participants
    """

    def __init__(self, participants):
        # convert dicts into Participant objects
        self.ranked_participants = []
        for p in participants:
            self.ranked_participants.append(RankedParticipant(p))
        # sort objects
        self.ranked_participants.sort(key=lambda part: part.rank, reverse=True)


class RankedParticipant:

    def __init__(self, participant):
        """
        :param participant: Participant (from models.py)
        """
        # see rank_calculator.py for ranking algorithm
        # print(participant.dump())
        self.participant = participant
        self.rank = calc_rank(
            participant.age, participant.veteran, participant.disability_status
        )
