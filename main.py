def election_results():
    print("Welcome to election results! A fun way to calculate the results of an election and the seat distribution of a Parliament! I will have to ask some questions")

    # Collecting input data
    registered_voters = int(input("How many people were registered to vote? (Please enter the total number of registered voters) "))
    actual_voters = int(input("How many people actually voted? (Please enter the total number of voters) "))
    num_parties = int(input("How many parties are competing in the election? (Please enter the total number of parties) "))
    total_seats = int(input("How many seats are available in the Parliament? (Please enter the total number of seats) "))
    threshold_percentage = float(input("What is the threshold for a party to get a seat? (Please enter the threshold in percentage) "))

    print("Thank you for the information! I will now calculate the results of the election and the seat distribution in the Parliament.")

    votes = []
    for i in range(1, num_parties + 1):
        votes.append(int(input(f"How many votes did party {i} get? (Please enter the number of votes) ")))

    total_votes_cast = sum(votes)
    voter_turnout = (total_votes_cast / registered_voters) * 100

    print(f"The total number of votes cast in the election is: {total_votes_cast}")
    print(f"The voter turnout in the election is: {voter_turnout}%")

    threshold_votes = (threshold_percentage / 100) * total_votes_cast
    print(f"The threshold for a party to get a seat in the Parliament is: {threshold_votes} votes")

    # Filter parties that meet the threshold
    valid_votes = [vote for vote in votes if vote >= threshold_votes]
    valid_parties_indices = [i for i, vote in enumerate(votes) if vote >= threshold_votes]

    print("The following parties meet the threshold and get a seat in the Parliament:")
    for i in valid_parties_indices:
        print(f"Party {i + 1}")

    # Calculate the proportional seats
    valid_total_votes = sum(valid_votes)
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

    print("\nThe seat distribution in the Parliament is as follows:")
    for i in range(num_parties):
        print(f"Party {i + 1} has {seats[i]} seats")

    print(f"\nThe total number of seats in the Parliament is: {sum(seats)}")

    print("Thank you for using election results! I hope you enjoyed calculating the results of the election and the seat distribution in the Parliament!")

# Run the election results function
election_results()