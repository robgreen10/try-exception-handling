VIP = ["Alice", "Bob", "Charlie"]

type = input("Hi please input your name: ")
clean_answer = type.strip().title()


if clean_answer in VIP:
    print(f"Welcome back {clean_answer}!")

    try:
        money = float(input("Great now what's your total bill amount: "))
        print("Since you're in VIP we have applied a 10% discount!")
        final_bill = money * .90
        print(f"Your final bill amount is: ${final_bill:.2f}")
    except ValueError:
        print("That's not a valid number, please try again!")
else:
    print("Ok, you're not in VIP, no worries")
    try:
        bill = float(input("What does your bill say?: "))
        print(f"Ok let me ring you up for ${bill:.2f}")
    except ValueError:
        print("That's not a valid number, please try again!")
        print("You're all set")
