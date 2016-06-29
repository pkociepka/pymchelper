import functools
from itertools import chain


body_types_names_mapping = {'cuboid': 'RPP',
                            'sphere': 'SPH',
                            'cylinder': 'RCC'}

def _geo_title_temp():
    return '*---><---><' + ('-' * 8) + '><' + ('-' * 58) + '>\n'


def _geo_title(json):
    JDBG1 = str(0)[-5:]
    JDBG2 = str(0)[-5:]
    unnused = 'test unused'[:10]
    title = 'example_title'[:60]

    title_line = ''
    title_line += '%5s' % JDBG1
    title_line += '%5s' % JDBG2
    title_line += '%10s' % unnused
    title_line += '%60s' %title
    title_line += '\n'
    return title_line


def _geo_body_temp():
    return '*.<->.<-->'+(6*'<-------->')+'\n'


def _parse_cuboid_coordinates(geometry):
    coordinates = [(x - (y/2), x + (y/2))for x, y in zip(geometry['center'], geometry['size'])]
    coordinates = chain(*coordinates)
    coordinates = map(lambda x: "%10f" % x, coordinates)
    return coordinates


def _parse_cylinder_coordinates(geometry):
    coordinates = geometry['start']
    coordinates += [y-x for x, y in zip(geometry['start'], geometry['end'])]
    coordinates = list(map(lambda x: "%10f" % x, coordinates))
    coordinates += ["\n", ' ' * 10, "%10f" % geometry['radius']]
    return coordinates


def _parse_sphere_coordinates(geometry):
    coordinates = geometry['center'] + [geometry['radius']]
    coordinates = map(lambda x: "%10f" % x, coordinates)
    return coordinates


def _geo_single_body(body):
    body_type = body_types_names_mapping[body['geometry']['type']]
    body_number = str('%4d' % body['id'])
    line = ['  ', body_type, ' ', body_number]
    if body_type == 'RPP':
        line += _parse_cuboid_coordinates(body['geometry'])
    elif body_type == 'RCC':
        line += _parse_cylinder_coordinates(body['geometry'])
    elif body_type == 'SPH':
        line += _parse_sphere_coordinates(body['geometry'])
    line.append("\n")
    return ''.join(line)


def _geo_body(bodies):
    bodies = [_geo_single_body(body) for body in bodies]
    bodies.append("  END\n\n")
    return "".join(bodies)


def _geo_zone_temp():
    return '*.<-><--->..<--->'+(8*'OR<--->')+'\n'


def _parse_single_zone_operation(operation):
    if operation['opcode'] == 'union':
        return ("OR%5d" % operation['bodyId'])
    elif operation['opcode'] == 'subtract':
        return "%+7d" % -operation['bodyId']
    elif operation['opcode'] == 'intersect':
        return "%+7d" % operation['bodyId']   # PLACE HOLDER
    else:
        return '  error'

def _geo_single_zone(zone):
    zone_name = "%03d" % zone['id']
    zone_number = "%5d" % zone['id']
    first_body = "%+5d" % zone['firstBodyId']
    line = ['  ', zone_name, zone_number, '  ', first_body]
    line += [_parse_single_zone_operation(x) for x in zone['operations']]
    line.append("\n")
    return "".join(line)


def _geo_zone(zones):
    zones = [_geo_single_zone(zone) for zone in zones]
    zones.append("  END\n\n")
    return "".join(zones)


def _geo_materials_temp():
    return ('<--->'*14) + '\n'


def _geo_materials(zones):
    list_of_zones = [zone['id'] for zone in zones]
    list_of_zones = list(map(lambda x: "%5d" % x, list_of_zones))
    list_of_materials = [zone['material'] for zone in zones]
    list_of_materials = list(map(lambda x: "%5d" % x, list_of_materials))
    materials = list_of_zones + ['\n'] + list_of_materials + ['\n']
    return "".join(materials)

def geo_to_dat(json):
    result = ''

    result += _geo_title(json)
    result += _geo_title_temp()

    result += _geo_body_temp()
    result += _geo_body(json['bodies'])

    result += _geo_zone_temp()
    result += _geo_zone(json['zones'])

    result += _geo_materials_temp()
    result += _geo_materials(json['zones'])
    return result

if __name__ == '__main__':
    json = {
        "bodies": [
            {
                "geometry": {
                    "center": [1, 1, 1],
                    "size": [1, 1, 1],
                    "type": "cuboid"
                },
                "name": "body1",
                "id": 1
            },
            {
                "geometry": {
                    "center": [1, 2, 3],
                    "size": [4,5, 6],
                    "type": "cuboid"
                },
                "name": "body2",
                "id": 2
            },
            {
                "geometry": {
                    "start": [1, 1, 1],
                    "end": [2, 2, 2],
                    "type": "cylinder",
                    "radius": 1
                },
                "name": "body3",
                "id": 3
            }
        ],
        "zones": [
            {
                "id": 1,
                "name": "zone1",
                "type": "type",
                "firstBodyId": 1,
                "material": 1,
                "operations": [
                    {
                        "opcode": "subtract",
                        "bodyId": 2
                    },
                    {
                        "opcode": "intersect",
                        "bodyId": 1
                    }
                ]
            },
            {
                "id": 2,
                "name": "zone2",
                "type": "type",
                "firstBodyId": 3,
                "material": 1,
                "operations": [
                    {
                        "opcode": "union",
                        "bodyId": 1
                    }
                ]
            }
        ]
    }
    print(geo_to_dat(json))
