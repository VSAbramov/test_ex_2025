from sqlalchemy import inspect
from tabulate import tabulate


def get_head(session, model, limit=5):
    """
    Return a string with the first N rows of a table
    """
    # Get column headers
    mapper = inspect(model)
    headers = [column.key for column in mapper.attrs]

    # Query first N rows
    rows = session.query(model).limit(limit).all()

    # Convert rows to list of dictionaries
    data = []
    for row in rows:
        row_dict = {}
        for header in headers:
            row_dict[header] = getattr(row, header)
        data.append(row_dict)

    # Convert to list of lists for tabulate
    table_data = [[row[header] for header in headers] for row in data]

    # Generate table string
    table_str = tabulate(table_data, headers=headers, tablefmt="grid")

    return "\n" + model.__tablename__ + "\n" + table_str
