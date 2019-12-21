from random import randint
import pickle


def create_relations():
    """Creates the dictionnary storing the person who you have to gift."""
    # Neded variables to create the dictionnary with all the relevant values
    To_Gift = []

    Gifted = []

    Relations = {}

    try:
        # Associate a person to every person
        for family in Big_Family:
            for person in family:
                To_Gift = list(set(Family1 + Family2 + Family3 + Family4 +
                                   Family5 + Family6 + Family7) - set(family + Gifted))
                Relations[person] = To_Gift[randint(0, len(To_Gift) - 1)]
                Gifted.append(Relations[person])

        # Create a new order if someone's person is repeated
        try:
            # Don't check if there are only two people in the relations
            if len((Relations.keys())) != 2:
                for key in Relations:
                    if Relations[key] == relations_past[key]:
                        return create_relations()
        except KeyError:
            pass

        return Relations
    # Handle when there aren't enough people to gift (same family)
    except OSError:
        return create_relations()


# Define all the subjects for the gifts, create different lists for each group and add them after to Big_Family
Family1 = ["María"]

Family2 = ["Isa"]

Family3 = ["Luis"]

Family4 = ["Laurence", "Jaime", "Sara", "Oscar"]

Family5 = ["Nacho", "Carmen", "Elena", "Begoña"]

Family6 = ["Marga", "Carlos"]

Family7 = ["Jordi", "Teresa"]

Big_Family = [Family1, Family2, Family3, Family4, Family5, Family6, Family7]

# Handle when it is the first time the program is run
try:
    # Get the invisible friends from the previous year
    with open("Gifts.pck", "rb") as gift_file:
        relations_past = pickle.load(gift_file)

except OSError:
    relations_past = {}

# Store the invisible friends for next year
with open("Gifts.pck", "wb") as gift_file:
    relations = create_relations()
    pickle.dump(relations, gift_file, protocol=pickle.HIGHEST_PROTOCOL)
