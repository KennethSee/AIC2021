def compare_dates(date1: str, date2: str):
    day1, month1, year1 = split_date(date1)
    day2, month2, year2 = split_date(date2)

    if year1 < year2:
        return -1
    elif year1 > year2:
        return 1
    else:
        if month1 < month2:
            return -1
        elif month1 > month2:
            return 1
        else:
            if day1 < day2:
                return -1
            elif day1 > day2:
                return 1
            else:
                return 0


def split_date(date: str):
    '''
    Splits date and returns tuple of date, month, and year
    '''
    date_lst = date.split('/')
    return int(date_lst[0]), int(date_lst[1]), int(date_lst[2])
