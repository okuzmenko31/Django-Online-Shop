from datetime import date
import random


def generate_end_date(start_date):
    """This function returns generated deactivation
    date of coupon."""
    s_date = start_date

    if s_date.month < 12:
        end_date_month = random.randint(s_date.month + 1, 12)
        end_date_day = random.randint(1, 25)
        end_date_year = s_date.year
    else:
        end_date_month = random.randint(1, 12)
        end_date_day = random.randint(1, 25)
        end_date_year = s_date.year + 1

    end_date = date(end_date_year, end_date_month, end_date_day)
    return end_date
