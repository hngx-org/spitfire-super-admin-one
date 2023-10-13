from routes import shop

def collect_endpoints():
    endpoints = []
    for rule in shop.url_map.iter_rules():
        if rule.endpoint != 'static':
            function_name = rule.endpoint.split('.')[-1]
            methods = ','.join(rule.methods)
            url = rule.rule
            endpoints.append((function_name, methods, url))
    return endpoints

# Collect endpoints from the 'shop' blueprint in the routes.py file
shop_endpoints = collect_endpoints()

# Now you have the endpoints in the shop_endpoints list
print(shop_endpoints)


