from django.core.cache import cache
from django_redis import get_redis_connection
import pickle


def save_category_to_cache(category):
    # Формируем ключ кэша
    cache_key = f'category_{category.pk}'
    query_params = ''
    cache_key_catgeory_all = f'category_list_{query_params}'
    cache.delete(cache_key)
    cache.delete(cache_key_catgeory_all)
    
    cache_ttl = 3600  
    
    redis_conn = get_redis_connection("default")
    
    serialized_category = pickle.dumps(category)
    
    redis_conn.setex(cache_key, cache_ttl, serialized_category)



