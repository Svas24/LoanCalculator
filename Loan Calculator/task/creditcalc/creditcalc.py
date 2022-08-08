import math
import argparse
import sys

if len(sys.argv) != 5:
    print("Incorrect parameters")
    sys.exit(1)

parser = argparse.ArgumentParser(sys.argv[0])
parser.add_argument("--type", choices=["diff", "annuity"], help='Use "diff" or "annuity" ', required=True)
parser.add_argument("--principal", type=int, help="Principal")
parser.add_argument("--periods", type=int, help="Period (in months)")
parser.add_argument("--interest", type=float, help="specified without a percent sign")
parser.add_argument("--payment", type=int, help="The monthly payment amount")
arguments = parser.parse_args()


if arguments.interest is None:
    print("Incorrect parameters")
    sys.exit(1)

i = arguments.interest / 12 / 100  # nominal interest

if arguments.type == "diff":
    if arguments.payment is not None:
        print("Incorrect arguments.")
        sys.exit(1)
    n = arguments.periods
    p = arguments.principal
    s = 0
    for m in range(1, n + 1):
        d = int(math.ceil(p / n + i * (p - (p * (m - 1)) / n)))
        s += d
        print(f"Month {m}: payment is {d}")
    print(f"\nOverpayment = {s - p}")

else:  # annuity
    if arguments.payment is None:  # calc payment
        j = (1 + i) ** arguments.periods
        k = i * j / (j - 1)
        payment = math.ceil(arguments.principal * k)
        print(f"Your annuity payment = {payment}")
        print(f"Overpayment = {round(payment * arguments.periods - arguments.principal)}")

    elif arguments.principal is None:  # calc principal
        j = (1 + i) ** arguments.periods
        k = i * j / (j - 1)
        principal = arguments.payment // k
        print(f"Your loan principal = {principal}!")
        print(f"Overpayment = {arguments.payment * arguments.periods - principal}")

    else:  # calc period
        periods = math.ceil(math.log(arguments.payment / (arguments.payment - i * arguments.principal), 1 + i))
        years = periods // 12
        months = periods % 12
        answer = "It will take "
        if years == 1:
            answer += "1 year "
        if years > 1:
            answer += str(years) + " years "
        if years != 0 and months != 0:
            answer += "and "
        if months == 1:
            answer += "1 month "
        if months > 1:
            answer += str(months) + " months "
        print(answer,  " to reply this loan!")
        print(f"Overpayment = {arguments.payment * periods - arguments.principal}")
