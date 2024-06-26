from itertools import combinations

def election_results():
    print("Welcome to election results! A fun way to calculate the results of an election and the seat distribution of a Parliament! I will have to ask some questions")

    # Collecting input data
    registered_voters = int(input("How many people were registered to vote? (Please enter the total number of registered voters)\n"))
    actual_voters = int(input("How many people actually voted? (Please enter the total number of voters)\n"))
    invalid_votes = int(input("How many invalid votes were there? (Please enter the number of invalid votes)\n"))
    blank_votes = int(input("How many blank votes were there? (Please enter the number of blank votes)\n"))
    num_parties = int(input("How many parties are competing in the election? (Please enter the total number of parties)\n"))
    total_seats = int(input("How many seats are available in the Parliament? (Please enter the total number of seats)\n"))
    threshold_percentage = float(input("What is the threshold for a party to get a seat? (Please enter the threshold in percentage)\n"))

    print("Thank you for the information! I will now calculate the results of the election and the seat distribution in the Parliament.")

    parties = []
    votes = []
    for i in range(1, num_parties + 1):
        party_name = input(f"What is the name of party {i}?\n")
        party_votes = int(input(f"How many votes did {party_name} get? (Please enter the number of votes)\n"))
        parties.append(party_name)
        votes.append(party_votes)

    total_votes_cast = sum(votes)
    voter_turnout = (actual_voters / registered_voters) * 100

    invalid_votes_percentage = (invalid_votes / actual_voters) * 100
    blank_votes_percentage = (blank_votes / actual_voters) * 100

    print(f"The total number of votes cast in the election is: {total_votes_cast}")
    print(f"The voter turnout in the election is: {voter_turnout:.2f}%")
    print(f"The percentage of invalid votes is: {invalid_votes_percentage:.2f}%")
    print(f"The percentage of blank votes is: {blank_votes_percentage:.2f}%")

    valid_votes = total_votes_cast - invalid_votes - blank_votes
    threshold_votes = (threshold_percentage / 100) * valid_votes
    print(f"The threshold for a party to get a seat in the Parliament is: {threshold_votes} votes")

    # Filter parties that meet the threshold
    valid_parties_votes = [vote for vote in votes if vote >= threshold_votes]
    valid_parties_indices = [i for i, vote in enumerate(votes) if vote >= threshold_votes]

    print("The following parties meet the threshold and get a seat in the Parliament:")
    for i in valid_parties_indices:
        print(f"{parties[i]}")

    # Calculate the proportional seats
    valid_total_votes = sum(valid_parties_votes)
    seats = [0] * num_parties

    for i in valid_parties_indices:
        seats[i] = round((votes[i] / valid_total_votes) * total_seats)

    # Adjust the total number of seats to match the total_seats using rounding
    allocated_seats = sum(seats)
    while allocated_seats != total_seats:
        if allocated_seats < total_seats:
            # Find the party with the largest decimal part of its seat allocation
            fractional_seats = [(votes[i] / valid_total_votes) * total_seats - seats[i] for i in valid_parties_indices]
            max_fraction_index = valid_parties_indices[fractional_seats.index(max(fractional_seats))]
            seats[max_fraction_index] += 1
        elif allocated_seats > total_seats:
            # Find the party with the smallest decimal part of its seat allocation
            fractional_seats = [(votes[i] / valid_total_votes) * total_seats - seats[i] for i in valid_parties_indices]
            min_fraction_index = valid_parties_indices[fractional_seats.index(min(fractional_seats))]
            seats[min_fraction_index] -= 1

        allocated_seats = sum(seats)

    print("\nThe seat distribution in the Parliament is as follows:\n")
    for i in range(num_parties):
        party_percentage = (votes[i] / total_votes_cast) * 100
        print(f"{parties[i]} has {seats[i]} seats ({party_percentage:.2f}% of votes)\n")

    print(f"\n\nThe total number of seats in the Parliament is: {sum(seats)}")

    # Calculate possible coalitions
    majority_threshold = (total_seats // 2) + 1
    print(f"\nA majority in the Parliament requires {majority_threshold} seats.")

    def find_coalitions(parties, seats, majority_threshold):
        possible_coalitions = []
        for r in range(1, len(parties) + 1):
            for coalition in combinations(range(len(parties)), r):
                total_seats = sum(seats[i] for i in coalition)
                if total_seats >= majority_threshold:
                    coalition_parties = [parties[i] for i in coalition]
                    possible_coalitions.append((coalition_parties, total_seats))
        return possible_coalitions

    possible_coalitions = find_coalitions(parties, seats, majority_threshold)

    if possible_coalitions:
        print("\nPossible coalitions that can form a majority:")
        for coalition, total_seats in possible_coalitions:
            print(f"Coalition possibility: {', '.join(coalition)} with {total_seats} seats")
    else:
        print("\nNo possible coalitions can form a majority.")

    print("Thank you for using election results! I hope you enjoyed calculating the results of the election and the seat distribution in the Parliament!")

# Run the election results function
election_results()
