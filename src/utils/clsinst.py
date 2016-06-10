'''Utility functions to create an object instance from the class
name.'''


def get_class_by_name(cls_name):
    '''Retrieve a class object by its name.'''

    name_parts = cls_name.split('.')
    
    mod_name = '.'.join(name_parts[0:-1])
    
    item = __import__(mod_name)
    for name in name_parts[1:]:
        item = getattr(item, name)
        
    return item


def get_instance_by_name(cls_name, *args, **kwargs):
    '''Create an instance by class name. 

    *args and **kwargs are passed to the __init__ function of the
     class.'''

    cls = get_class_by_name(cls_name)
    inst = cls(*args, **kwargs)

    return inst


    
