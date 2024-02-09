def sortHelper(sortBY, sortBy, queryObj):
    if sortBy.lower() == 'desc':
        queryObj = queryObj.order_by(f'-{sortBY}')
    else:
        queryObj = queryObj.order_by(sortBY)

    return queryObj