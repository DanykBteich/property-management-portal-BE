from flask import request
from werkzeug.exceptions import BadRequest
from sqlalchemy.orm import Query as BaseQuery

def paginate_query(query: BaseQuery, schema):
    try:
        page = int(request.args.get("page", 1))
        per_page = min(int(request.args.get("per_page", 20)), 100)
    except ValueError:
        raise BadRequest("Page and Per_Page must be integers")
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return {
        "items": schema.dump(pagination.items),
        "total": pagination.total,
        "page": pagination.page,
        "per_page": pagination.per_page,
        "pages": pagination.pages
    }