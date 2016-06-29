from itertools import chain


def _detector_temp():
    return '*'+ ('-'*8) + '>' + (('<' + ('-'*8) +'>')*6) + "\n"

_particle_type_mapping = {
    'all': -1,
    'neutrons': 1,
    'protons': 2,
    'pion_pi_minus': 3,
    'pion_pi_plus': 4,
    'pion_pi_zero': 5,
    'heavyions': 25
}


def _mesh_detector_geometry_line(detector):
    detector_name = "%10s" % 'MSH'
    detector_geometry = detector['geometry']['start'] + detector['geometry']['end']
    detector_geometry = list(map(lambda x: "%10f" % x, detector_geometry))
    return "".join([detector_name] + detector_geometry + ["\n"])


def _cylinder_detector_geometry_line(detector):
    detector_name = "%10s" % 'CYL'
    inner_radius = "%10f" % detector['geometry']['radius'][0]
    min_angle = "%10f" % detector['geometry']['angle'][0]
    min_Z = "%10f" % detector['geometry']['zrange'][0]
    outer_radius = "%10f" % detector['geometry']['radius'][1]
    max_angle = "%10f" % detector['geometry']['angle'][1]
    max_Z = "%10f" % detector['geometry']['zrange'][1]
    return "".join([detector_name, inner_radius, min_angle, min_Z, outer_radius, max_angle, max_Z, '\n'])


def _3dim_detector_slicing_line(detector):
    detector_slices = detector['bins']
    detector_slices = list(map(lambda x: "%10f" % x, detector_slices))
    particle_type = "%10d" % _particle_type_mapping[detector['particle']]
    scored_quantity = ("%10s" % detector['quantity']).upper()
    file_name = "%10s" % ('det' + str(detector['id']))
    line = [" " * 10] + detector_slices + [particle_type, scored_quantity, file_name, "\n"]
    return "".join(line)


def _additional_heavy_ion_parameters(detector):
    if _particle_type_mapping[detector['particle']] != 25 and \
                    detector['quantity'] != 'letflu':
        return ""

    atomic_number = "%10d" % detector['particle_data']["A"]
    atomic_mass = "%10d" % detector['particle_data']["Z"]
    medium = "%10d" % detector['particle_data']['medium'] \
        if 'medium' in detector['particle_data'].keys() else ''
    return "".join([' '*10, atomic_number, atomic_number, medium, '\n'])


def _parse_mesh_detector(detector):
    geometry_line = _mesh_detector_geometry_line(detector)
    slicing_line = _3dim_detector_slicing_line(detector)

    detector_line = [geometry_line, slicing_line]
    return "".join(detector_line)


def _parse_cylinder_detector(detector):
    first_line = _cylinder_detector_geometry_line(detector)
    second_line = _3dim_detector_slicing_line(detector)
    third_line = _additional_heavy_ion_parameters(detector)
    return "".join(first_line + second_line + third_line)

_detector_parser_mapping = {
    'mesh': _parse_mesh_detector,
    'cylinder': _parse_cylinder_detector
}


def _parse_single_detector(detector):
    return _detector_parser_mapping[detector['geometry']['type']](detector)


def detect_to_dat(json):
    detectors = [_detector_temp()]
    detectors += [_parse_single_detector(detector) for detector in json['detectors']]
    detectors.append("\n")
    return "".join(detectors)
