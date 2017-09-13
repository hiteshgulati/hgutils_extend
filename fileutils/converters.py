from simpledbf import Dbf5


def dbf2csv(source_file_name, target_file_name = None):
    if target_file_name == None:
        target_file_name = source_file_name[:-4] + ".csv"
    dbf_file = Dbf5(source_file_name)
    dbf_file.to_csv(target_file_name)