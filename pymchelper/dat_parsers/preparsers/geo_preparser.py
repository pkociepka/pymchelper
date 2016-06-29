import re

def remove_comments(geo):
    return re.sub("\*.*\n", "\n", geo)

def remove_empty_lines(geo):
    return "\n".join([x for x in geo.split("\n") if x])

def split_into_parts(geo):
    [bodies, zones, materials] = geo.split("END")
    head = bodies.split("\n")[0]
    bodies = "\n".join(bodies.split("\n")[1:])
    return (head, bodies, zones, materials)

def convert_geo(geo):
    [head, bodies, zones, mats] =\
        split_into_parts(remove_empty_lines(remove_comments(geo)))
    return "\nEND\n".join([convert_head(head),
                           convert_bodies(bodies),
                           convert_zones(zones),
                           convert_materials(mats)])

#####################################################

def convert_head(head):
    flags = [int(head[0:5]), int(head[5:10])]
    title = head[20:].strip()
    return " ".join([str(flags[0]), str(flags[1]), title])

#####################################################

def is_body_continuation_line(line):
    return False if line[:11].strip() else True

def get_coords(line):
    coords = []
    while line.strip():
        coords.append(float(line[:10]))
        line = line[10:]
    return coords

def get_single_body(bodies):
    line = bodies[0]
    body_type = line[2:5]
    body_id = int(line[6:10])
    coords = get_coords(line[10:])
    bodies = bodies[1:]
    while bodies and is_body_continuation_line(bodies[0]):
        coords += get_coords(bodies[0][10:])
        bodies = bodies[1:]
    coords = [str(x) for x in coords]
    return "%s %s %s" % (body_type, body_id, " ".join(coords))

def remove_single_body(bodies):
    bodies = bodies[1:]
    while bodies and is_body_continuation_line(bodies[0]):
        bodies = bodies[1:]
    return bodies

def convert_bodies(bodies):
    bodies = bodies.split("\n")
    converted = []
    while bodies:
        converted.append(get_single_body(bodies))
        bodies = remove_single_body(bodies)
    return "\n".join(converted)

#####################################################

def is_zone_continuation_line(line):
    return False if line[:5].strip() else True

def get_operand(body):
    if "+" in body:
        return "+"
    elif "-" in body:
        return "-"
    elif "OR" in body:
        return "OR"

def get_body_id(body):
    return body.replace("+", "")\
               .replace("-", "")\
               .replace("OR", "")\
               .strip()

def get_op_list(line):
   ops = []
   while line.strip():
       ops.append(get_operand(line[:7]))
       ops.append(get_body_id(line[:7]))
       line = line[7:]
   return ops

def get_single_zone(zones, zone_counter):
    line = zones[0]
    zone_name = line[2:5]
    try:
        zone_id = int(line[5:10])
    except ValueError:
        zone_id = zone_counter
    ops = get_op_list(line[10:])

    zones = zones[1:]
    while zones and is_zone_continuation_line(zones[0]):
        ops += get_op_list(zones[0][5:])
        zones = zones[1:]
    print(ops)
    return "%s %s %s" % (zone_name, zone_id, " ".join(ops))

def remove_single_zone(zones):
    zones = zones[1:]
    while zones and is_zone_continuation_line(zones[0]):
        zones = zones[1:]
    return zones

def convert_zones(zones):
    zones = zones.split("\n")
    converted = []
    zones_count = 1
    while zones:
        converted.append(get_single_zone(zones, zones_count))
        zones_count += 1
        zones = remove_single_zone(zones)
    return "\n".join(converted)

#####################################################

def convert_materials(materials):
    tokens = materials.split()
    result = ""
    mat_count = int(len(tokens)/2)
    for i in range(mat_count):
        result += ("%s %s\n" % (tokens[i], tokens[i + mat_count]))
    return result
