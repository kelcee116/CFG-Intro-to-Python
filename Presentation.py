# Harry Potter API - all characters https://hp-api.onrender.com/api/characters

# stats to compare are year of birth (most recent year wins)
# ancestry (ranked - pure-blood(1), half-blood(2), quarter-veela(3), half-veela(4), squib(5), muggleborn(6), muggle(7))
# house (randomly ranked by python - 'Ravenclaw', 'Gryffindor', 'Slytherin', 'Hufflepuff')

# pip install requests

import random

import requests


# Function to generate a random Harry Potter character
def random_hp():

    url = 'https://hp-api.onrender.com/api/characters'
    response = requests.get(url)
    hp_characters = response.json()

    # remove characters with missing values
    filtered_characters = []
    for character in hp_characters:
        if character['house'] != '' and character['ancestry'] != '' and character['yearOfBirth'] is not None:
            filtered_characters.append(character)

    # create a new identifier for each character for random selection
    new_id = 0

    for description in filtered_characters:
        new_id = new_id + 1
        description.update({"new_id": new_id})

    # get a random number from the random module and use this to select a Harry Potter character
    generate_number = random.randint(1, 18)

    for item in filtered_characters:
        if item['new_id'] == generate_number:
            chosen_character = item
            break
    else:
        chosen_character = None

    # return only the values that we are interested in
    return {
        'new_id': chosen_character['new_id'],
        'name': chosen_character['name'],
        'yob': chosen_character['yearOfBirth'],
        'ancestry': chosen_character['ancestry'],
        'house': chosen_character['house']
    }


random_hp()


# Function to choose players characters and play the game


def game():

    # choose character for player 1
    my_hp = random_hp()
    print('Your character is {} -\n yob: {}\n ancestry: {}\n house: {}\n' .format(my_hp['name'],
                                                                                  my_hp['yob'],
                                                                                  my_hp['ancestry'],
                                                                                  my_hp['house']))

    # choose stat to play with
    stat_choice = input('Which stat do you want to use? (yob, ancestry, house) \n')

    # choose character for player 2
    opponent_hp = random_hp()
    print('\nYour opponent chose {} -\n yob: {}\n ancestry: {}\n house: {}\n'.format(opponent_hp['name'],
                                                                                     opponent_hp['yob'],
                                                                                     opponent_hp['ancestry'],
                                                                                     opponent_hp['house']))

    # create a variable for the stat chosen for both players
    my_stat = my_hp[stat_choice]
    opponent_stat = opponent_hp[stat_choice]

    # randomly rank the houses and save each players ranking in a txt file
    houses = ['Ravenclaw', 'Gryffindor', 'Slytherin', 'Hufflepuff']
    random.shuffle(houses)

    my_house_index = houses.index(my_hp['house']) + 1
    opponents_house_index = houses.index(opponent_hp['house']) + 1

    with open('my_stats.txt', 'a') as my_stats_file:
        my_house_stat = my_house_index
        my_stats_file.write(str(my_house_stat))

    with open('opponents_stats.txt', 'a') as opponents_stats_file:
        opponents_house_stat = opponents_house_index
        opponents_stats_file.write(str(opponents_house_stat))

    # check the ranking for ancestry and append each players ranking in the appropriate txt file
    ancestry_list = ['pure-blood', 'half-blood', 'quarter-veela', 'half-veela',
                     'squib', 'muggleborn', 'muggle']

    my_ancestry_index = ancestry_list.index(my_hp['ancestry']) + 1
    opponents_ancestry_index = ancestry_list.index(opponent_hp['ancestry']) + 1

    with open('my_stats.txt', 'a') as my_stats_file:
        my_ancestry_stat = my_ancestry_index
        my_stats_file.write(str(my_ancestry_stat))

    with open('opponents_stats.txt', 'a') as opponents_stats_file:
        opponents_ancestry_stat = opponents_ancestry_index
        opponents_stats_file.write(str(opponents_ancestry_stat))

    # remind the players of the rules for winning/losing
    if stat_choice == 'house':
        print('Houses have been randomly ranked in this order: {}\n'.format(houses))
    elif stat_choice == 'ancestry':
        print('Ancestry is ranked in this order: pure-blood, half-blood, quarter-veela, half-veela, '
              'squib, muggleborn, muggle\n')
    else:
        print('The most recent year wins\n')

    # print whether player 1 has won, lost or drew
    if stat_choice == 'yob' and my_stat > opponent_stat:
        result = 'win.'
        print('You Win!')
    elif stat_choice == 'yob' and my_stat < opponent_stat:
        result = 'lose.'
        print('You Lose!')
    elif stat_choice == 'ancestry' and my_ancestry_index < opponents_ancestry_index:
        result = 'win.'
        print('You Win!')
    elif stat_choice == 'ancestry' and my_ancestry_index > opponents_ancestry_index:
        result = 'lose.'
        print('You Lose!')
    elif stat_choice == 'house' and my_house_index < opponents_house_index:
        result = 'win.'
        print('You Win!')
    elif stat_choice == 'house' and my_house_index > opponents_house_index:
        result = 'lose.'
        print('You Lose!')
    else:
        result = 'draw.'
        print('Its a draw!')

    # append the results to a text file
    with open('result.txt', 'a') as result_file:
        new_item = result
        result_file.write(new_item)


game()


# Function to return the result of the game
# Best of 3 games and confirm who is the final winner
# If it is a 3 way tie, do a tie-breaker -
# add the rankings for ancestry and house for each player for all three games - highest ranking (lowest number) wins

def winner():

    three_games = input('\nHave you played three games? (yes, no) \n')

    if three_games == 'yes':
        with open('result.txt', 'r') as text_file:
            contents = text_file.read().strip()
            print('\nThe results of your three games are: {}'.format(contents))
            if contents in ['draw.draw.draw.', 'lose.win.draw.', 'lose.draw.win.', 'win.lose.draw.',
                            'win.draw.lose.', 'draw.win.lose.', 'draw.lose.win.']:
                print('\nWe need a tie breaker!')
                print('\nWe will combine the rankings from ancestry and house for each player for all three games'
                      ' - highest ranked player wins!')
                with open('my_stats.txt', 'r') as my_stats_file:
                    my_rankings = my_stats_file.read()
                    my_overall_ranking = sum([int(i) for i in str(my_rankings)])
                with open('opponents_stats.txt', 'r') as opponents_stats_file:
                    opponents_rankings = opponents_stats_file.read()
                    opponents_overall_ranking = sum([int(i) for i in str(opponents_rankings)])
                print('\nYour overall character ranking is {}'.format(my_overall_ranking))
                print('\nYour opponents overall character ranking is {}'.format(opponents_overall_ranking))
                if my_overall_ranking < opponents_overall_ranking:
                    print('\nYou are the ultimate Harry Potter Champion! Congratulations!')
                elif my_overall_ranking > opponents_overall_ranking:
                    print('\nSorry, your opponent has won. Better luck next time!')
                else:
                    print('\nWe cant believe it! Another tie!')
                    print('You share the title of Ultimate Harry Potter Champion')
                    print('Congratulations to you both!')
            elif contents in ['win.win.win.', 'win.win.lose.', 'win.win.draw.', 'draw.draw.win.',
                              'win.draw.draw.', 'draw.win.draw.', 'draw.win.win', 'lose.win.win.',
                              'win.lose.win', 'win.draw.win.']:
                print('\nYou are the ultimate Harry Potter Champion! Congratulations!')
            else:
                print('\nSorry, your opponent has won. Better luck next time!')
    else:
        print('\nPlay again!')


winner()
