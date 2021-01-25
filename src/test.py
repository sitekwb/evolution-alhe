from sndlibparser import nodes, links, link_keys, link_array, demand_array, demand_keys, demands

# for key, data in zip(link_keys, link_array):
#     print(key, data)

for key, data in zip(demand_keys, demand_array):
    print(key, data)

