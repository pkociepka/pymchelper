
def mat_to_dat(materials):

    dat_result = [__mat_to_dat(material) for material in materials['materials']]
    string_result = ""
    for material in dat_result:
        string_result += material
    return string_result


def __mat_to_dat(material):
    result = ""
    result += "* " + material['name'] + "\n" if 'name' in material.keys() and material['name'] else ""
    result += "MEDIUM " + str(material['medium']) + "\n"
    result += "STATE " + str(material['state']) + "\n" if 'state' in material.keys() else ""

    if 'icru' in material.keys():
        result += "ICRU " + str(material['icru']) + "\n"
        result += "RHO " + str(material['density']) + "\n" if 'density' in material.keys() else ""

        loaddedx = " " + str(material['loaddedx']) if 'loaddedx' in material.keys() else None
        loaddedx = "" if loaddedx == " 0" else loaddedx

        result += "LOADDEDX" + loaddedx + "\n" if loaddedx is not None else ""
    elif 'nuclids' in material.keys():
        result += "RHO " + str(material['density']) + "\n"
        for nuclide in material['nuclids']:
            # nuclide
            result += "NUCLID " + str(nuclide['nuclid_numbers'][0]) + " " + \
                      str(nuclide['nuclid_numbers'][1]) + "\n"
            # amass
            result += "AMASS " + str(nuclide['atomic_mass']) + "\n" if 'atomic_mass' in nuclide.keys() else ""
            # ivalue
            result += "IVALUE " + str(nuclide['excitation']) + "\n" if 'excitation' in nuclide.keys() else ""

        result += "LOADDEDX " + str(material['loaddedx']) + "\n" if 'loaddedx' in material.keys() else ""

    result += "END\n\n"

    return result