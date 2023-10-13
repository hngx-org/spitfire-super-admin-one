import inspect
import importlib

def collect_endpoints(blueprint):
    endpoints = []
    for rule in blueprint.url_map.iter_rules():
        if rule.endpoint != 'static':
            function_name = rule.endpoint.split('.')[-1]
            view_function = blueprint.view_functions[function_name]
            methods = ','.join(rule.methods)
            url = rule.rule
            endpoints.append((function_name, methods, url))
    return endpoints

# Import your blueprint dynamically
shop_blueprint = importlib.import_module('shop')

# Collect endpoints from the 'shop' blueprint with "/api/shop" prefix
shop_endpoints = collect_endpoints(shop_blueprint.shop)

# Now you have the endpoints in the shop_endpoints list
print(shop_endpoints)
