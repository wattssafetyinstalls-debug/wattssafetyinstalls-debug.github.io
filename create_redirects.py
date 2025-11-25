redirects = [
    "/old-path /new-path 301",
    # Add redirects for merged services, e.g., "/lawn-care /property-maintenance 301"
]

with open('_redirects', 'w') as f:
    f.write('\n'.join(redirects))
print("Redirects file updated.")