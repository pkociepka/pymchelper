import os
from bdo2txt import parse_to_txt

__author__ = 'Mateusz'


# It is assumed that parser receives path from if-shieldide/ to the processed file as an argument
# Parser returns processed data as a dictionary with the following keys:
# -axes: contains marks of interesting axes
# -data: contains calculated values
# -bounds: contains bounds for relevant axes


def parse_output(file_path):
    """ Args:
            file_path: Path to the processed file from if-shieldide/ directory
        Returns:
            Output data in dictionary format
    """
    parse_to_txt(file_path)
    txt_file = open(os.path.splitext(file_path)[0] + '.txt')
    return txt_to_dict(txt_file.read())


def txt_to_dict(bdo_data: str) -> dict:
    """ Args:
            bdo_data: txt data extracted from original .bdo file using bdo2txt built-in shieldhit parser
    """
    # lines containing data from detector
    data_lines = get_data_lines(bdo_data)
    # lines with metadata
    info_lines = get_info_lines(bdo_data)
    # line which describe detector parameters
    det_type_line = get_det_line(info_lines)
    if det_type_line[0] == 'ZONE':
        # parse zone-type detector
        res = parse_zone_type_det(data_lines, det_type_line)
    else:
        # parse msh-type detector
        res = parse_msh_type_det(data_lines, det_type_line)
    return res


def parse_zone_type_det(data_lines, det_type_line):
        zone_first = int(det_type_line[2])
        zone_last = int(det_type_line[5])
        res = {}
        i = 0
        for x in range(zone_first, zone_last + 1):
            res[x] = float(data_lines[i][3])
            i += 1
        return res


def parse_msh_type_det(data_lines, det_type_line):
    bin_line = [x for x in det_type_line if not x.startswith("BIN")]
    # create list[(dimension, index, bins)]
    bins = []
    i = 0
    while i < len(bin_line):
        bins.append((bin_line[i], len(bins), int(bin_line[i + 1])))
        # bins[bin_line[i]] = int(bin_line[i+1])
        i += 2

    # indices of dimensions that vary (these columns contain data)
    data_indices = []
    for (dim, index, bin_count) in bins:
        if bin_count != 1:
            data_indices.append((dim, index, bin_count))

    dimensions = len(data_indices)

    res = {"axes": []}
    for (dim, index, _) in data_indices:
        res["axes"].append(dim)

    if dimensions == 1:
        args = []
        values = []
        d_i = data_indices[0][1]
        # number of vertical lines - empty last line
        v_i = len(data_lines[0]) - 1
        for line in data_lines:
            args.append(float(line[d_i]))
            values.append(float(line[v_i]))
        res["data"] = values
        res["bounds"] = {data_indices[0][0]: [min(args), max(args)]}
    if dimensions == 2:
        values = []
        # indices of specific axes
        x_i = data_indices[0][1]
        y_i = data_indices[1][1]
        v_i = len(data_lines[0]) - 1
        i = 0
        for m in range(data_indices[1][2]):
            values.append([])
            for n in range(data_indices[0][2]):
                line = data_lines[i]
                values[-1].append(float(line[v_i]))
                i += 1
        res["data"] = values
        res["bounds"] = {data_indices[0][0]: [float(data_lines[0][x_i]), float(data_lines[-1][x_i])],
                         data_indices[1][0]: [float(data_lines[0][y_i]), float(data_lines[-1][y_i])]}
    if dimensions == 3:
        values = []
        x_i = data_indices[0][1]
        y_i = data_indices[1][1]
        z_i = data_indices[2][1]
        v_i = len(data_lines[0]) - 1
        i = 0
        for m in range(data_indices[2][2]):
            values.append([])
            for n in range(data_indices[1][2]):
                values[-1].append([])
                for o in range(data_indices[0][2]):
                    line = data_lines[i]
                    values[-1][-1].append(float(line[v_i]))
                    i += 1
        res["data"] = values
        res["bounds"] = {data_indices[0][0]: [float(data_lines[0][x_i]), float(data_lines[-1][x_i])],
                         data_indices[1][0]: [float(data_lines[0][y_i]), float(data_lines[-1][y_i])],
                         data_indices[2][0]: [float(data_lines[0][z_i]), float(data_lines[-1][z_i])]}
    return res


def get_data_lines(bdo_data):
    # lines containing data from detector
    data_lines = [x for x in bdo_data.split("\n") if not x.startswith('#')]
    # remove empty lines
    data_lines = [x for x in data_lines if x]
    # split each line into four-element list [x, y, z, value]
    data_lines = [x.split() for x in data_lines]
    return data_lines


def get_info_lines(bdo_data):
    info_lines = [x for x in bdo_data.split("\n") if x.startswith('#')]
    return info_lines


def get_det_line(info_lines):
    det_type_line = info_lines[1].split()
    # remove '#' symbol
    det_type_line = det_type_line[1:]
    return det_type_line
