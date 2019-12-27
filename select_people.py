from random import seed, sample
from pickle import load, dump, HIGHEST_PROTOCOL
from os import path


def create_relations(family_group, family_group_set, past_relations):
    '''This function creates the dictionnary storing the person who you have to gift.'''
    # Neded variables to create the dictionnary with all the relevant values
    to_gift = []
    gifted = set()
    relations = {}
    finished = False

    while not finished:
        error = False
        # Associate each person with the person it will be giving the gift to
        for family in family_group:
            for person in family:
                to_gift = family_group_set - set(family).union(gifted)

                if not to_gift:
                    error = True
                    break

                relations[person] = sample(to_gift, 1)[0]
                gifted.add(relations[person])

        # Create a new relationship if someone's person is repeated with the previous year's data but
        # only check if there are more than 2 people in the group
        if len(family_group_set) < 2 and past_relations:
            for key in relations:
                if relations[key] == past_relations[key]:
                    error = True
                    break

        if not error:
            finished = True

        return relations


def merge_lists_into_sets(*sets):
    '''This function merges all the given lists into one set and returns it.'''
    result_set = set()

    for merge_set in sets:
        result_set.update(merge_set)

    return result_set


def get_people():
    '''This function gets the group of people from the people.txt file.'''
    if path.exists('people.txt'):
        with open('people.txt', 'r', encoding='utf-8') as f:
            people = f.readlines()

        clean_people = []

        for line in people:
            clean_people.append(line.strip().split(', '))

        return clean_people
    else:
        raise OSError(
            'Missing people file to get group of people participating.')


def make_and_save_relations():
    '''This function creates the association for every person to the person they will be gifting and saves
    the content into the 'gifts.pck' file'''
    # Define all the subjects for the gifts, create different lists for each group and add them after to big_Family

    big_family_list = get_people()
    big_family_set = merge_lists_into_sets(*big_family_list)

    # Handle when it is the first time the program is run
    if path.exists('gifts.pck'):
        # Get the invisible friends from the previous year
        with open('gifts.pck', 'rb') as gift_file:
            past_relations = load(gift_file)
    else:
        past_relations = {}

    # Store the invisible friends for next year
    with open('gifts.pck', 'wb') as gift_file:
        relations = create_relations(
            big_family_list, big_family_set, past_relations)
        dump(relations, gift_file, protocol=HIGHEST_PROTOCOL)
