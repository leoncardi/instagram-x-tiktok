import os
import hashlib
from datetime import datetime
from tzlocal import get_localzone
import pickle
import pandas as pd


class DFVC:
    def __init__(self, df: pd.DataFrame, df_name: str = None):
        self.df = df
        self.df_name = df_name if df_name else 'Untitled DataFrame'
        self.creation_date = self.get_current_gmt_timestamp()
        self.version = self.generate_version_hash()
        self.shape = self.df.shape


    def _repr_html_(self):
        """
        Generates an HTML representation of the DFVC object for rendering in Jupyter notebooks
        with a muted dark turquoise theme.
        """
        unique_id = f"dfvc_{id(self)}" 
        html = f"""
        <div style='border:1px solid #1b2b30; padding:10px; border-radius:10px; width:max-content; 
                    font-family:Arial, sans-serif; background-color:#0a0e12; color:#8fa3a6; font-size:0.9em;'>
            <div style='display: flex; align-items: center;'>
                <button onclick="var info = document.getElementById('{unique_id}_info');
                                if (info.style.display === 'none') {{
                                    info.style.display = 'block';
                                    this.textContent = '-';
                                }} else {{
                                    info.style.display = 'none';
                                    this.textContent = '+';
                                }}"
                        style='background-color:#202c31; color:#b5c9cb; border:none; padding:4px 12px; 
                            border-radius:5px; cursor:pointer; font-size:0.8em; margin-right:10px;'>
                    +
                </button>
                <span style='font-weight: bold; color:#2d6f6b;'>DFVC Object</span>
            </div>
            <div id='{unique_id}_info' style='display:none; margin-top:10px;'>
                <strong style='color:#2d6f6b;'>df_name==</strong>{self.df_name}<br>
                <strong style='color:#2d6f6b;'>version==</strong>{self.version}<br>
                <strong style='color:#2d6f6b;'>creation_date==</strong>{self.creation_date}<br>
                <strong style='color:#2d6f6b;'>shape==</strong>{self.shape}<br>
            </div>
        </div>
        """
        return html


    def get_current_gmt_timestamp(self):
        """
        Returns the current timestamp in the format 'YYYY:MM:DD HH:MM:SS GMT±X'.

        Returns:
            str: A string containing the formatted timestamp.
        """
        # Get local timezone and current time
        local_tz = get_localzone()
        local_time = datetime.now(local_tz)

        # Calculate UTC offset in hours
        offset_seconds = local_time.utcoffset().total_seconds()
        offset_hours = int(offset_seconds // 3600)
        offset_sign = "+" if offset_hours >= 0 else "-"
        offset_hours = abs(offset_hours)

        # Format the timestamp
        formatted_time = local_time.strftime(f"%Y:%m:%d %H:%M:%S GMT{offset_sign}{offset_hours:02}")
        return formatted_time


    def generate_version_hash(self):
            """
            Generates a compact and unique hash based solely on the dataframe content.

            Returns:
                str: A SHA-256 hash representing the version.
            """
            # Ensure the dataframe is not empty or None
            if self.df is None or self.df.empty:
                raise ValueError("The dataframe is either None or empty. Cannot generate a version hash.")

            # Generate a hash directly from the dataframe content
            version_hash = hashlib.sha256(
                pd.util.hash_pandas_object(self.df, index=True).values.tobytes()
            ).hexdigest()

            return version_hash


    def get_dataframe(self):
        """
        Returns the original dataframe.

        Returns:
            pandas.DataFrame: The original dataframe stored in the object.
        
        Raises:
            AttributeError: If the dataframe is not initialized or is None.
        """
        if not hasattr(self, 'df') or self.df is None:
            raise AttributeError('The dataframe is not initialized or is set to None.')
        return self.df


    def compare_dfvc_objects(self, other):
        """
        Validates the integrity of another DFVC object by comparing key attributes.

        Args:
            other (DFVC): The other DFVC object to compare against.

        Raises:
            ValueError: If any attribute does not match the expected values.
        """
        # Validate version
        if self.version != other.version:
            raise ValueError(f"Version mismatch: self.version={self.version}, other.version={other.version}")

        # Validate shape
        if self.shape != other.shape:
            raise ValueError(f"Shape mismatch: self.shape={self.shape}, other.shape={other.shape}")

        # Validate creation date
        if self.creation_date != other.creation_date:
            raise ValueError(
                f"Creation date mismatch: self.creation_date={self.creation_date}, other.creation_date={other.creation_date}"
            )

        # Validate dataframe equality
        if not self.df.equals(other.df.sort_index(axis=0).sort_index(axis=1)):
            raise ValueError("Dataframe contents do not match after normalization.")

        # Validate original dataframe equality
        if not self.df.equals(other.original_df.sort_index(axis=0).sort_index(axis=1)):
            raise ValueError("Original dataframe contents do not match after normalization.")

        print('Version integrity verified successfully.')


    def compare_versions(self, expected_version):
        """
        Compares the current object version with the expected version to ensure integrity.

        Args:
            expected_version (str): The version to compare against.

        Raises:
            ValueError: If the current version does not match the expected version.
        """
        if self.version != expected_version:
            raise ValueError(f'Version mismatch: expected "{expected_version}", found "{self.version}".')
        
        print('Version integrity verified successfully.')


    def export_as_dfvc_file(self, file_path):
        """
        Saves the current object as a .dfvc file.

        Args:
            file_path (str): The path where the .dfvc file will be saved.

        Raises:
            ValueError: If the file_path is invalid.
            IOError: If there is an issue during the file writing process.
        """
        # Ensure the file extension is .dfvc
        if not file_path.endswith('.dfvc'):
            file_path += '.dfvc'

        # Validate and create the directory if it does not exist
        directory = os.path.dirname(file_path) or "."
        if not os.path.exists(directory):
            try:
                os.makedirs(directory)
                print(f"Directory {directory} created.")
            except Exception as e:
                raise ValueError(f"Cannot create directory {directory}: {e}")

        try:
            # Save the object as a .dfvc file
            with open(file_path, 'wb') as file:
                pickle.dump(self, file)
        except Exception as e:
            raise IOError(f"Failed to export DFVC file to {file_path}: {e}")

        print(f"DFVC object successfully saved to {file_path}.")


    @staticmethod
    def load_dfvc_file(file_path):
        """
        Loads a DFVC object from a .dfvc file.

        Args:
            file_path (str): The path to the .dfvc file to be loaded.

        Returns:
            DFVC: The loaded DFVC object.

        Raises:
            ValueError: If the file does not have a .dfvc extension.
            FileNotFoundError: If the specified file does not exist.
            IOError: If there is an issue during file reading.
            pickle.UnpicklingError: If the file content is not a valid serialized DFVC object.
        """
        # Check file extension
        if not file_path.endswith('.dfvc'):
            raise ValueError("The file must have a .dfvc extension.")

        # Check if the file exists
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"The file '{file_path}' does not exist.")

        try:
            # Load the object from the file
            with open(file_path, 'rb') as file:
                return pickle.load(file)
        except pickle.UnpicklingError as e:
            raise pickle.UnpicklingError(f"Failed to deserialize the DFVC object: {e}")
        except Exception as e:
            raise IOError(f"An error occurred while reading the file '{file_path}': {e}")
