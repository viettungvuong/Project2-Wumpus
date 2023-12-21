def read_file(filename):
    # Read the content of the file
    with open(filename, "r") as file:
        content = file.readlines()

    # Extract size and map data
    size = int(content[0].strip())  # Extract size from the first line
    map_data = ''.join(content[1:])

    # Process map data
    # print(map_data)
    map_rows = map_data.strip().split('\n')
    # print(map_rows)

    merged_rows = []
    for row in map_rows:
        merged_row = row.strip().split('.')
        merged_rows.append(merged_row)

    return merged_rows

print(read_file("map2.txt"))