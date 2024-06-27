from itertools import combinations

def election_results():
    print("Welcome to election results! A fun way to calculate the results of an election and the seat distribution of a Parliament! I will have to ask some questions")

    # Collecting input data
    registered_voters = int(input("\nHow many people were registered to vote? (Please enter the total number of registered voters)\n"))
    actual_voters = int(input("\nHow many people actually voted? (Please enter the total number of voters)\n"))

    while True:
        invalid_votes = int(input("\nHow many invalid votes were there? (Please enter the number of invalid votes)\n"))
        blank_votes = int(input("\nHow many blank votes were there? (Please enter the number of blank votes)\n"))
        num_parties = int(input("\nHow many parties are competing in the election? (Please enter the total number of parties)\n"))
        
        parties = []
        votes = []
        for i in range(1, num_parties + 1):
            party_name = input(f"\nWhat is the name of party {i}?\n")
            party_votes = int(input(f"\nHow many votes did {party_name} get? (Please enter the number of votes)\n"))
            parties.append(party_name)
            votes.append(party_votes)

        total_votes_cast = sum(votes) + invalid_votes + blank_votes

        if total_votes_cast != actual_voters:
            print("\n\n\nError: The total votes cast (votes by all parties + invalid votes + blank votes) does not equal the number of actual voters. Please re-enter the data.\n")
        else:
            break

    total_seats = int(input("\nHow many seats are available in the Parliament? (Please enter the total number of seats)\n"))
    threshold_percentage = float(input("\nWhat is the threshold for a party to get a seat? (Please enter the threshold in percentage)\n"))

    voter_turnout = (actual_voters / registered_voters) * 100

    invalid_votes_percentage = (invalid_votes / actual_voters) * 100
    blank_votes_percentage = (blank_votes / actual_voters) * 100

    print(f"\n\n\nThe total number of votes cast in the election is: {total_votes_cast}")
    print(f"The voter turnout in the election is: {voter_turnout:.2f}%")
    print(f"The percentage of invalid votes is: {invalid_votes_percentage:.2f}%")
    print(f"The percentage of blank votes is: {blank_votes_percentage:.2f}%")

    valid_votes = sum(votes)
    threshold_votes = (threshold_percentage / 100) * valid_votes
    print(f"\nThe threshold for a party to get a seat in the Parliament is: {threshold_votes} votes")

    # Filter parties that meet the threshold
    valid_parties_votes = [vote for vote in votes if vote >= threshold_votes]
    valid_parties_indices = [i for i, vote in enumerate(votes) if vote >= threshold_votes]

    print("The following parties meet the threshold and get a seat in the Parliament:\n")
    for i in valid_parties_indices:
        print(f"{parties[i]}")

    # Seat allocation methods
    def dhondt_method(votes, total_seats):
        seats = [0] * num_parties
        for _ in range(total_seats):
            max_votes = 0
            max_index = -1
            for i in range(num_parties):
                if votes[i] >= threshold_votes:
                    quotient = votes[i] / (seats[i] + 1)
                    if quotient > max_votes:
                        max_votes = quotient
                        max_index = i
            if max_index >= 0:
                seats[max_index] += 1
        return seats

    def sainte_lague_method(votes, total_seats):
        seats = [0] * num_parties
        for _ in range(total_seats):
            max_votes = 0
            max_index = -1
            for i in range(num_parties):
                if votes[i] >= threshold_votes:
                    quotient = votes[i] / (2 * seats[i] + 1)
                    if quotient > max_votes:
                        max_votes = quotient
                        max_index = i
            if max_index >= 0:
                seats[max_index] += 1
        return seats

    def first_past_the_post(votes, total_seats):
        seats = [0] * num_parties
        for _ in range(total_seats):
            max_votes = max(votes)
            max_index = votes.index(max_votes)
            seats[max_index] += 1
            votes[max_index] = -1  # Remove the winner's votes to not count them again
        return seats

    def simple_proportional_representation(votes, total_seats):
        valid_total_votes = sum(votes)
        seats = [round((vote / valid_total_votes) * total_seats) for vote in votes]
        allocated_seats = sum(seats)
        while allocated_seats != total_seats:
            if allocated_seats < total_seats:
                fractional_seats = [(vote / valid_total_votes) * total_seats - seat for vote, seat in zip(votes, seats)]
                max_fraction_index = fractional_seats.index(max(fractional_seats))
                seats[max_fraction_index] += 1
            elif allocated_seats > total_seats:
                fractional_seats = [(vote / valid_total_votes) * total_seats - seat for vote, seat in zip(votes, seats)]
                min_fraction_index = fractional_seats.index(min(fractional_seats))
                seats[min_fraction_index] -= 1
            allocated_seats = sum(seats)
        return seats

    # Ask user for seat allocation method
    print("\n\n\nPlease select the seat allocation method:")
    print("1. D'Hondt Method")
    print("2. Sainte-Laguë Method")
    print("3. First-Past-The-Post")
    print("4. Simple Proportional Representation")

    method_choice = int(input("\nEnter the number of the method you want to use:\n"))

    if method_choice == 1:
        seats = dhondt_method(votes, total_seats)
    elif method_choice == 2:
        seats = sainte_lague_method(votes, total_seats)
    elif method_choice == 3:
        seats = first_past_the_post(votes, total_seats)
    elif method_choice == 4:
        seats = simple_proportional_representation(votes, total_seats)
    else:
        print("Invalid choice. Using D'Hondt Method by default.")
        seats = dhondt_method(votes, total_seats)

    print("\nThe seat distribution in the Parliament is as follows:\n")
    for i in range(num_parties):
        party_percentage = (votes[i] / sum(votes)) * 100
        print(f"{parties[i]} get(s) {seats[i]} seats ({party_percentage:.2f}% of votes)\n")

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
            print(f"Coalition: {', '.join(coalition)} with {total_seats} seats")
    else:
        print("\nNo possible coalitions can form a majority.")

# Run the election results function
election_results()