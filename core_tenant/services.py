from django_elasticsearch_dsl import Document, Index, fields
from elasticsearch_dsl import Q
# from .documents import ProductDocument
from elasticsearch.exceptions import NotFoundError

# def tenant_index_name(tenant):
#     return f"{tenant.schema_name}_products"

# def search_products(query, page=1, page_size=10, tenant=None):
    
#     search = ProductDocument.search()
#     search = search.query(Q("multi_match", query=query, fields=['name', 'description']))
    
#     # Pagination
#     search = search[(page - 1) * page_size: page * page_size]

#     if tenant:
#         index = tenant_index_name(tenant)
#         search = search.index(index)
#     else:
#         search = search.index('public_products')  # Use default index for anonymous users
        
#     return search.execute()



# def create_index_if_not_exists(index_name):
#     try:
#         if not ProductDocument._index.exists():
#             ProductDocument._index.create(index=index_name)
#     except NotFoundError:
#         ProductDocument._index.create(index=index_name)



from elasticsearch_dsl import Search
from .documents import ProductIndex

def search_products(query, page=1, page_size=10):
    s = Search(index=f"product_{get_current_tenant().schema_name}_index").query("multi_match", query=query, fields=['name', 'description'])

    # Paginate results
    start = (page - 1) * page_size
    s = s[start:start + page_size]

    response = s.execute()
    return response, response.hits.total.value 