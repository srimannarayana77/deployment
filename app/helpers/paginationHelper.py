import math
def paginationResponse(message, count, limit, page, respData):
    totalPages = math.ceil(count / int(limit))
    response_data = {
            "success": True,
            "message": message,
            "count": count,
            "totalPages": totalPages,
            "currentPage": page,
            "resultsPerPage": limit,
            "nextPage": page + 1 if page < totalPages else None,
            "previousPage": page - 1 if page > 1 else None,
            "data": respData
            }
    return response_data