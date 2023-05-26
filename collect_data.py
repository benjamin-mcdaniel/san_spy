import os
import json
import configparser

def get_folder_size(path, depth):
    total_size = 0

    for dirpath, dirnames, filenames in os.walk(path):
        if dirpath != path and dirpath.count(os.sep) - path.count(os.sep) >= depth:
            # Reached the desired depth, only calculate file sizes
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                total_size += os.path.getsize(filepath)
        else:
            # Calculate the size of all contents in the directory
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                total_size += os.path.getsize(filepath)
    
    return total_size

def collect_folder_sizes(root_dirs, depth):
    result = {}

    for root_dir in root_dirs:
        folder_data = {}
        folder_data[root_dir] = {}

        for dirpath, dirnames, _ in os.walk(root_dir):
            folder_size = get_folder_size(dirpath, depth)
            folder_data[root_dir][dirpath] = folder_size
        
        result.update(folder_data)

    return result

def save_to_json(data, output_path):
    with open(output_path, 'w') as file:
        json.dump(data, file, indent=4)

def main():
    config = configparser.ConfigParser()
    config.read('conf.ini')

    dirs = config['DEFAULT']['dirs'].split(',')
    depth = int(config['DEFAULT']['depth'])
    save_dir = config['DEFAULT']['save_dir']
    
    folder_sizes = collect_folder_sizes(dirs, depth)

    for root_dir, data in folder_sizes.items():
        output_file = os.path.join(save_dir, f'{root_dir}_sizes.json')
        save_to_json(data, output_file)

    print("Folder sizes collected and saved to JSON.")

if __name__ == '__main__':
    main()
