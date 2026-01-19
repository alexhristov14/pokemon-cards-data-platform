def helper_set_name(set_name):
    set_name = set_name.replace('&', 'and')
    return "-".join(set_name.lower().split())

def get_common_id_from_raw_table(row):
    data = row.card_name.split('-')
    pokemon_name = data[0] if data[0] != 'mega' else data[1]
    # extra_data = data[1:-1] if data[0] != 'mega' else [data[0], *data[2:-1]],
    num_in_set = data[-1]
    set_name = helper_set_name(row.set_name)

    return "-".join([pokemon_name, num_in_set, set_name])

def get_common_id_from_metadata_table(row):
    card_name = row.card_name.split()
    pokemon_name = card_name[0].lower()
    # extra_data = card_name[1:]
    num_in_set = str(row.num_in_set)
    set_name = helper_set_name(row.set_name)


    return "-".join([pokemon_name, num_in_set, set_name])

