import datetime

FINAL_DAY = datetime.datetime.strptime('13May2019', '%d%b%Y')


def suggested_spending(actual_total, days_left):
    """
    :param actual_total:
    :param days_left:
    :return: how much money should be spent everyday to last the semester
    """
    money_suggested = actual_total / days_left
    return float("%.2f" % money_suggested)


#  runs only if user has to add money aka predicted total wasted is > what's left on meal plan
def money_to_add(actual_total, avg, days_left):
    """
    :param actual_total:
    :param avg:
    :param days_left:
    :return: how many days are left once meal plan reaches 0 and how much $ to add back based on that
    """
    while days_left > 0:
        actual_total -= avg

        if actual_total <= 0:
            return [days_left, (days_left * avg)]
        days_left -= 1


def predicted_total(avg, days_left):
    """
    :param avg:
    :param days_left:
    :return: how much would be spent for the rest of semester based on avg spent and days left
    """
    return avg * days_left


#  returns results. We apply these results on db only if logged
def main_func(actual_total, avg):
    """

    :param actual_total:
    :param avg:
    :return: string containing when meal plan will finish plus money to add OR
            states that user is ok plus suggested daily amount to spend to drag meal plan to 0 at the end

    we have two cases: either fore casted amount to spend is more than what they currently have left
    or it is less. If it is less, then user is good as they won't overspend
    If its more then we inform on what date we predict they'll run out of money
    and based on remaining days left of semester with $0, how much they'll need to add into meal plan to last
    """
    days_remaining = (FINAL_DAY - datetime.datetime.today()).days

    predicted_total_spent = predicted_total(avg, days_remaining)

    ret_text = "With a current meal plan of ${} and an average spending of ${}...\n".format(actual_total, avg)

    if predicted_total_spent > actual_total:

        cash_to_add = money_to_add(actual_total, avg, days_remaining)

        #  num of days left in semester when meal plan is set to reach $0
        days_broke = cash_to_add[0]

        net_cash_lost = cash_to_add[1]
        net_cash_lost_sliced = '%.2f' % net_cash_lost
        net_cash_lost_float = float(net_cash_lost_sliced)
        #  date_days_broke is the actual date when meal plan is set to reach $0
        date_days_broke = datetime.datetime.fromordinal(FINAL_DAY.toordinal() - days_broke).strftime("%A %B %d, %Y")
        ret_text += "You'll run out of money on {}.\nWith your current spending habits, " \
                    "you'd need to add ${} of your own money.\n".format(date_days_broke, net_cash_lost_float)

    else:
        net_cash_gain = actual_total - predicted_total_spent
        net_cash_gain_sliced = '%.2f' % net_cash_gain
        net_cash_gain_float = float(net_cash_gain_sliced)
        ret_text += "Your meal plan will last! You will have ${} left over!\n".format(net_cash_gain_float)

    ret_text += "We suggest spending ${} each day to take full advantage of your meal plan.".format(
        suggested_spending(actual_total, days_remaining))

    return ret_text


def money_will_last(actual_total, avg):
    """
    :param actual_total:
    :param avg:
    :return: list of estimated_final_date/ final_day and amount of money to add/ money left over

    modified version of main function that returns list of TWO elements: datetime obj and float %
        if money will last, then the date returned is the final day of class with $ difference (roll-over)
        otherwise, date is the estimated end date and estimated $ to add (its neg here to signify debt)
    """
    days_remaining = (FINAL_DAY - datetime.datetime.today()).days
    predicted_total_spent = predicted_total(avg, days_remaining)

    if predicted_total_spent > actual_total:
        cash_to_add = money_to_add(actual_total, avg, days_remaining)
        days_broke = cash_to_add[0]
        actual_cash_to_add = cash_to_add[1]
        actual_cash_to_add_sliced = '%.2f' % actual_cash_to_add
        actual_cash_to_add_float = float(actual_cash_to_add_sliced)
        date_days_broke = datetime.datetime.fromordinal(FINAL_DAY.toordinal() - days_broke)

        return [date_days_broke, -actual_cash_to_add_float]

    else:
        roll_over = actual_total - predicted_total_spent
        roll_over_sliced = '%.2f' % roll_over
        roll_over_float = float(roll_over_sliced)
        return [FINAL_DAY, roll_over_float]
