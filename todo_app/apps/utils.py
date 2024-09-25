import hashlib
import time
from uuid import uuid4

from slugify import slugify


def generate_custom_id(*args):
    hash_values = ':'.join([str(x) for x in args])
    current_time = str(time.time_ns())
    hash_values += current_time
    return hashlib.sha256(hash_values.encode('utf-8')).hexdigest()[:16]

def unique_slug_generator(instance, slug_field, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(slug_field)
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = f'{slug}-{str(uuid4())[:8]}'
        return unique_slug_generator(instance, slug_field=slug_field, new_slug=new_slug)
    return slug[-40:]