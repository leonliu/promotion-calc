import pandas as pd
import argparse

excel_file = 'menu.xlsx'

def calculate_price_and_profit(stack, record):
    price = record[2]*record[3]
    profit = record[2]*record[3]*record[5]
    for item in stack:
        if record[0] == item[0]:
            price = record[2]
            profit = record[2]*record[5]
    return price, profit


def print_result(title, result, stack):
    print("{}: {:.2f}".format(title, result))
    print("===================================")
    new_stack = list()
    while stack:
        item = stack.pop()
        price, profit = calculate_price_and_profit(new_stack, item)
        print("  {}  {:.2f}  {:.2f}".format(item[1], price, profit))
        new_stack.append(item)

def find_min_order(records, min_amount, curr_amount, record_stack, final_stack, threshold):
    result = min_amount
    stack = final_stack

    for record in records:
        amount = curr_amount + calculate_price_and_profit(record_stack, record)[0]

        if amount <= threshold:   # go to next round
            record_stack.append(record)
            result, stack = find_min_order(records, result, amount, record_stack, stack, threshold)
            record_stack.pop()
        elif result == 0:  # initialize once
            record_stack.append(record)
            result = amount
            stack = record_stack.copy()
            record_stack.pop()
        elif amount < result:  # find a better choice in current round
            result = amount
            record_stack.append(record)
            stack = record_stack.copy()
            record_stack.pop()

    return result, stack

def find_min_profit(records, min_profit, curr_profit, curr_amount, record_stack, final_stack, threshold):
    result = min_profit
    stack = final_stack

    for record in records:
        dprice, dprofit = calculate_price_and_profit(record_stack, record)
        amount = curr_amount + dprice
        profit = curr_profit + dprofit

        if amount <= threshold:
            record_stack.append(record)
            result, stack = find_min_profit(records, result, profit, amount, record_stack, stack, threshold)
            record_stack.pop()
        elif result == 0:
            record_stack.append(record)
            result = profit
            stack = record_stack.copy()
            record_stack.pop()
        elif profit < result:
            record_stack.append(record)
            result = profit
            stack = record_stack.copy()
            record_stack.pop()

    return result, stack


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate best promotion strategy.")
    parser.add_argument('amount', type=float, help="promotion amount")
    args = parser.parse_args()

    amount = args.amount

    xl = pd.ExcelFile(excel_file)
    sheet = xl.parse('Sheet1')
    df = sheet[sheet["折扣"] >= 1]

    stack = list()
    final_stack = list()
    result, final_stack = find_min_order(df.values, 0, 0, stack, final_stack, amount)
    print_result("最小订单价组合:", result, final_stack)

    stack.clear()
    final_stack.clear()
    result, final_stack = find_min_profit(df.values, 0, 0, 0, stack, final_stack, amount)
    print_result("最小毛利润组合:", result, final_stack)