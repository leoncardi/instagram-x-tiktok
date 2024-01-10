def get_raw_db_path(root_dir):
    """Assists sqlite connections by providing the absolute directory for 'raw.db'"""
    return f'{root_dir}/database/01_raw.db'

def get_transf_db_path(root_dir):
    """Assists sqlite connections by providing the absolute directory for 'transformed.db'"""
    return f'{root_dir}/database/02_transformed.db'