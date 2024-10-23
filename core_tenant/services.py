from django_elasticsearch_dsl import Document, Index, fields
from elasticsearch_dsl import Q
from elasticsearch.exceptions import NotFoundError
from .utils import get_tenant_from_subdomain
from elasticsearch_dsl import Search
from .documents import ProductIndex



def search_products(query, page=1, page_size=10):
    tenant_schema = get_tenant_from_subdomain().schema_name
    index_name = f"product_{tenant_schema}_index"

    # Log the index name and query for debugging
    print(f"Searching in index: {index_name} with query: '{query}'")

    # s = Search(index=index_name).query("multi_match", query=query, fields=['name', 'description','price'])
    s = Search(index=index_name)
    # If query is not empty, apply the search filter
    if not  query == '':
        s = s.query("multi_match", query=query, fields=['name', 'description'])

    start = (page - 1) * page_size
    s = s[start:start + page_size]
    try:
        response = s.execute()
        print(f"Search response: {response}")  # Log the response for debugging
        return response  # Return both response and total hits
    except Exception as e:
        print(f"Search execution failed: {e}")  # Log any errors that occur
        return None # Return None if there's an error