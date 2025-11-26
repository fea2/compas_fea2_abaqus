"""
Note
----
to debug run from terminal:
abaqus python path_to_\compas_fea2_abaqus\results\odb_extract.py None path_to_odb odb_file_name
"""

from sqlite3 import Error
import sqlite3

try:
    # from ..job import *
    import odbAccess
except Exception as e:
    print("Error importing odbAccess. Make sure you run this script from Abaqus.")
    print(e)
    pass

import os
import sys

# from collections.abc import Iterable

# conversion between Field Value names and FieldValue attribute names
invariants_dict = {
    "MISES": "mises",
    "MAX_PRINCIPAL": "maxPrincipal",
    "MID_PRINCIPAL": "midPrincipal",
    "MIN_PRINCIPAL": "minPrincipal",
    "MAX_INPLANE_PRINCIPAL": "maxInPlanePrincipal",
    "MIN_INPLANE_PRINCIPAL": "minInPlanePrincipal",
    "OUTOFPLANE_PRINCIPAL": "outOfPlanePrincipal",
    "TRESCA": "tresca",
    "PRESS": "press",
    "INV3": "inv3",
    "MAGNITUDE": "magnitude",
}

# convert = {
#     'CF1':   'cfx',  'CF2':  'cfy',  'CF3':  'cfz', 'CFM': 'cfm',
#     'CM1':   'cmx',  'CM2':  'cmy',  'CM3':  'cmz', 'CMM': 'cmm',
#     'U1':    'ux',   'U2':   'uy',   'U3':   'uz',  'UM':  'um',
#     'UR1':   'urx',  'UR2':  'ury',  'UR3':  'urz', 'URM': 'urm',
#     'RF1':   'rfx',  'RF2':  'rfy',  'RF3':  'rfz', 'RFM': 'rfm',
#     'RM1':   'rmx',  'RM2':  'rmy',  'RM3':  'rmz', 'RMM': 'rmm',
#     'S11':   'sxx',  'S22':  'syy',  'S33':  'szz',  'S12':  'sxy',  'S13':  'sxz',  'S23':  'sxz',
#     'E11':   'exx',  'E22':  'eyy',  'E33':  'ezz',  'E12':  'exy',  'E13':  'exz',  'E23':  'exz',
#     'LE11':  'exx',  'LE22': 'eyy',  'LE33': 'ezz',  'LE12': 'exy',  'LE13': 'exz',  'LE23': 'exz',
#     'PE11':  'pexx', 'PE22': 'peyy', 'PE33': 'pezz', 'PE12': 'pexy', 'PE13': 'pexz', 'PE23': 'pexz',
#     'SF1':   'sf1',  'SF2':  'sf2',  'SF3':  'sf3',  'SF4':  'sf4',  'SF5':  'sf5',  'SF6':  'sf6',
#     'SM1':   'sm1',  'SM2':  'sm2',  'SM3':  'sm3',
#     'SK1':   'skx',  'SK2':  'sky',  'SK3':  'skz',
#     'SE1':   'se1',  'SE2':  'se2',  'SE3':  'se3',
#     'CTF1':  'spfx', 'CTF2': 'spfy', 'CTF3': 'spfz',
#     'TF1':   'tfx',  'TF2':  'tfy',  'TF3':  'tfz',
#     'NFORCSO1': 'nfx', 'NFORCSO2': 'nfy', 'NFORCSO3': 'nfz', 'NFORCSO4': 'nmx',  'NFORCSO5':  'nmy',  'NFORCSO6':  'nmz',


#     'VALUE':  'rbfor',
#     'AXES':   'axes',
#     'SMISES': 'smises', 'SMAXP': 'smaxp', 'SMINP': 'sminp',
# }

# TODO Extend with:https://abaqus-docs.mit.edu/2017/English/SIMACAEOUTRefMap/simaout-c-std-nodalvariables.htm


def create_connection(db_file=None):
    """Create a database connection to the SQLite database specified by db_file.

    Parameters
    ----------
    db_file : str, optional
        Path to the .db file, by default 'None'. If not provided, the database
        is run in memory.

    Return
    ------
    :class:`sqlite3.Connection` | None
        Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file or ":memory:")
    except Error as e:
        print(e)
    return conn


def _create_table(conn, sql):
    """Create a table from the create_table_sql statement.

    Parameters
    ----------
    conn : :class:`sqlite3.Connection`
        Connection to the database.
    create_table_sql : str
        A CREATE TABLE statement

    """
    try:
        c = conn.cursor()
        c.execute(sql)
    except Error as e:
        print(e)


def _insert_entry(conn, sql):
    try:
        c = conn.cursor()
        c.execute(sql)
    except Error as e:
        print(e)
        print(sql)
        exit()
    return c.lastrowid


def create_info_table(conn):
    with conn:
        sql = """CREATE TABLE IF NOT EXISTS info (property text, description text, UNIQUE(property) );"""
        _create_table(conn, sql)


def create_field_description_table(conn):
    with conn:
        sql = """CREATE TABLE IF NOT EXISTS fields (field text, description text, components text, invariants text, UNIQUE(field) );"""
        _create_table(conn, sql)


def insert_field_description(conn, field, description, components_names, invariants_names):
    sql = """ INSERT OR IGNORE INTO fields VALUES ('{}', '{}', '{}', '{}')""".format(
        field,
        description,
        components_names,
        invariants_names,
    )

    return _insert_entry(conn, sql)


def create_field_table(conn, field, components_names, invariants_names):
    """Create the results table for the given field.

    Parameters
    ----------
    conn : obj
        Connection to the databse.
    field : str
        Name of the output field.
    components_names : Iterable
        Output field components names.
    invariants_names : Iterable
        Output field invariants names.
    """
    # FOREIGN KEY (step) REFERENCES analysis_results (step_name),
    with conn:
        sql = """CREATE TABLE IF NOT EXISTS {} (step text, part text, type text, position text, key integer, {});""".format(
            field,
            ", ".join(["{} float".format(c) for c in components_names + invariants_names]),
        )
        _create_table(conn, sql)


def insert_field_results(conn, field, components_data, invariants_data, step, part, key_type, position, key):
    """Insert the results of the analysis at a node.

    Parameters
    ----------
    conn : obj
        Connection to the databse.
    field : str
        Name of the output field.
    components_data : Iterable
        Output field components values.
    invariants_data : Iterable
        Output field invariants values.
    step : str
        Name of the analysis step.
    part : str
        Name of the part.
    key_type : str
        'node' or 'element'.
    position : str
        'NODAL' or 'INTERGRATION POINT'
    key : int
        Key of the node/element.

    Return
    ------
    int
        Index of the inserted item.
    """

    sql = """ INSERT INTO {} VALUES ('{}', '{}', '{}', '{}', {}, {})""".format(
        field,
        step,
        part,
        key_type,
        position,
        int(key),
        ", ".join([str(c) for c in components_data + invariants_data]),
    )
    return _insert_entry(conn, sql)


def extract_odb_data(database_path, database_name, field):
    """Extracts data from the .odb file for the requested steps and fields.

    Parameters
    ----------
    database_path : str
        Folder path containing the analysis .odb file.
    database_name : str
        Name of the database.
    requested_fields : list
        Data field requests.
    file_format : str
        'db', 'json' or 'pkl'

    Returns
    -------
    None

    Note
    ----
    Developers should consult the official guidelines on how to speed up the
    script: http://130.149.89.49:2080/v2016/books/cmd/default.htm?startat=pt05ch09s05.html

    """

    # create from the field argument, the correspondence table between abaqus results fields and requested compas results fields
    field_name_comp_abaq = {}
    field_component_abaq_comp = {}
    if field:
        for field_data in field.split("."):
            field_name_data = field_data.split("-")[0]
            field_component_data = field_data.split("-")[1]
            field_name_comp_abaq[field_name_data.split("/")[0]] = field_name_data.split("/")[1].split(",")
            field_component_abaq_comp[field_name_data.split("/")[0]] = {
                field_component.split("/")[0]: field_component.split("/")[1]
                for field_component in field_component_data.split(",")
            }

    # open the odb file
    odb = odbAccess.openOdb(os.path.join(database_path, "{}.odb".format(database_name)))
    steps = odb.steps
    database = os.path.join(database_path, "{}-results.db".format(database_name))
    if os.path.exists(database):
        os.remove(database)

    with create_connection(database) as conn:
        create_field_description_table(conn)
        for step_name, step in steps.items():
            frame = step.frames[-1]  # TODO maybe loop through the frames
            default_fields = frame.fieldOutputs

            # loop through all the requested compas field
            for compas_field_name, abaqus_fields_names in field_name_comp_abaq.items():
                invariants_names = []  # invariants are, for now, not integrated in the table

                # initialization of sql table of compas field
                insert_field_description(
                    conn,
                    compas_field_name,
                    "",
                    " ".join(field_component_abaq_comp[compas_field_name].values()),
                    " ".join(invariants_names),
                )
                create_field_table(
                    conn,
                    compas_field_name,
                    list(field_component_abaq_comp[compas_field_name].values()),
                    invariants_names,
                )

                # the data from the different abaqus fields composing the compas field
                # are assembled in a dictionnary
                component_data_dict = {}
                for abaqus_field in abaqus_fields_names:
                    field_data = default_fields[abaqus_field]
                    abaqus_components_names = list(field_data.componentLabels)
                    field_data_values = field_data.values
                    for value in field_data_values:
                        if getattr(value, "nodeLabel"):
                            key = value.nodeLabel
                            key_type = "node"
                        elif getattr(value, "elementLabel"):
                            key = value.elementLabel
                            key_type = "element"
                        else:
                            raise AttributeError()
                        position = value.position.name
                        part = value.instance.name[:-2]
                        if part not in component_data_dict.keys():
                            component_data_dict[part] = {}
                        if key not in component_data_dict[part].keys():
                            component_data_dict[part][key] = {
                                component: 0 for component in field_component_abaq_comp[compas_field_name].values()
                            }
                        component_data_dict[part][key]["key_type"] = key_type
                        for i in range(len(abaqus_components_names)):
                            abaqus_component_name = abaqus_components_names[i]
                            compas_component_name = field_component_abaq_comp[compas_field_name][abaqus_component_name]
                            component_value = value.data[i]
                            component_data_dict[part][key][compas_component_name] = component_value

                # results are inserted in the sql table
                for part, key_data in component_data_dict.items():
                    for key, component_data in key_data.items():
                        insert_field_results(
                            conn,
                            compas_field_name,
                            [
                                component_data_dict[part][key][component]
                                for component in field_component_abaq_comp[compas_field_name].values()
                            ],
                            [],
                            step_name,
                            part,
                            component_data["key_type"],
                            position,
                            key,
                        )
        conn.commit()


# ============================================================================
# Main
# ============================================================================
# NOTE: this is used while calling the module through abaqus -> !!!DO NOT DELETE!!!
# NOTE: must be compatible with python 2+.
if __name__ == "__main__":
    # NOTE: the arguments are in the order they are passed
    database_path = sys.argv[-2]
    database_name = sys.argv[-1]
    if len(sys.argv) > 3:
        field_input = sys.argv[-3]
    else:
        field_input = None

    extract_odb_data(database_path=database_path, database_name=database_name, field=field_input)
