import os
import json
import re

def is_leaf_directory(path):
    for entry in os.scandir(path):
        if entry.is_dir():
            return False
    return True

def extract_dose_theta(file_path):
    """Extract the dose_theta value from the .md file"""
    dose_section = False
    try:
        with open(file_path, 'r') as file:
            for line in file:
                if line.strip().startswith('# DRµG type:'):
                    dose_section = True
                if dose_section and 'dose_theta' in line:
                    return float(line.split('=')[1].strip())
                # Exit the section upon reaching another header or end of section
                if dose_section and line.strip().startswith('#') and not line.strip().startswith('# DRµG type:'):
                    dose_section = False
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
    return None

def directory_to_json(path, san_length):
    """Recursively build a JSON object representing the directory structure"""
    dir_dict = {}
    for entry in os.scandir(path):
        if entry.is_dir():
            # Continue building the structure only if it's a leaf directory
            if entry.name == '__pycache__':
                continue
            elif is_leaf_directory(entry.path):
                files_info = []
                for f in os.scandir(entry.path):
                    if f.is_file() and f.name.endswith('.md'):
                        dose_theta = extract_dose_theta(f.path)
                        files_info.append({
                            'filename': f.name,
                            'dose_theta': dose_theta,
                            'filepath' : f.path[san_length:]
                        })
                dir_dict[entry.name] = files_info
            else:
                dir_dict[entry.name] = directory_to_json(entry.path, san_length)
    return dir_dict

script_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.join(script_dir, '.')

dir_json = directory_to_json(root_dir, len(root_dir))

output_file_path = os.path.join(script_dir, 'directory_structure.json')

with open(output_file_path, 'w') as outfile:
    json.dump(dir_json, outfile, indent=4)

print(f"Directory structure written to {output_file_path}")
