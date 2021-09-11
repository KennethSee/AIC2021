import pandas as pd

from utils.settings import get_session_id


def retrieve_financials(db):
    company_id = get_session_id()

    retrieved_data = db.get_company_financials(company_id)
    if retrieved_data is None:
        return None

    # build initial df
    items = []
    sort_order = []
    direction = []
    is_fixed = []
    for key, val in retrieved_data['mapping'].items():
        items.append(key)
        sort_order.append(val['sortOrder'])
        direction.append(val['direction'])
        is_fixed.append(val['isFixed'])
    df = pd.DataFrame(list(zip(items, sort_order, direction, is_fixed)),
                      columns=['Items', 'SortOrder', 'Direction', 'IsFixed'])
    df = df.sort_values('SortOrder').drop(['SortOrder'], axis=1)

    # merge financials to df
    retrieved_data.pop('mapping', None)
    for date, financials in retrieved_data.items():
        # build financial df for each date
        items = []
        values = []
        for item, value in financials.items():
            items.append(item)
            values.append(value)
        df_fin = pd.DataFrame(list(zip(items, values)), columns=['Items', date])

        # merge
        df = df.merge(df_fin, how='left', on='Items')
    return df
