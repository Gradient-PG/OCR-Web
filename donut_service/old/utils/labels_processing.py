import json
import os

# Creates temporary representation of the image' labels
# WARNING: Handles only one level of labels nesting
def _get_temp_rows(single_json):
  elems = []
  raw_annotations = single_json['annotations'][0]['result']
  
  row = {
    "ID": None,
    "parentID": None,
    "label": None,
    "text": None,
    "children": [],
  }
  
  for i, el in enumerate(raw_annotations):
    

    if "labels" in el["value"].keys():
      row['label'] = el["value"]["labels"][0]
      row["ID"] = el["id"]
      
      if "parentID" in el.keys():
        row["parentID"] = el["parentID"]
        
    elif "text" in el["value"].keys():
      row['text'] = el["value"]["text"][0]
    
    if row['label'] is not None and row['text'] is not None:
      if row['text'] == '"' or row['text'] == "-'-" or row['text'] == '-"-':
        row['text'] = '-'
        
      elems.append(row)
      row = {
        "ID": None,
        "parentID": None,
        "label": None,
        "text": None,
        "children": [],
      }
  
  def get_parent(child):
    for el in elems:
      if el != None and el['ID'] == child['parentID']:
        return el
      
    return None
  
  for i, child in enumerate(elems):
    if child["parentID"] != None:
      parent = get_parent(child)
      child_copy = child.copy()
      
      elems[i] = None
      parent['children'].append(child_copy)
 
  result = []
  
  for i, el in enumerate(elems):
    if el != None:
      result.append(el)
    
  return result

# Transforms temporary representation of labels to 'ground truth'/json
def _temp_rows_to_gt(temp_rows):
  result = {}
  
  def process_one(elem):
    if len(elem['children']) > 0:
      children_c = {}
      for child in elem['children']:
        children_c.update(process_one(child))
      
      # We assume it only happens for 'st.': 'nr' pairs
      rank = elem['text']
      return {rank: children_c}
    else:
      return {elem['label']: elem['text']}
  
  for el in temp_rows:
    result.update(process_one(el))
  
  return result

def _process_json_single(single_json):
  temp_rows = _get_temp_rows(single_json)
  # print(temp_rows)
  return _temp_rows_to_gt(temp_rows)

# Extracts a filename of the image from the part of the json file describing that image assuming the structure: "<letter> (<number>).jpg"
def _get_image_code(single_json, aug):
  # img_path without augmentation
  if not aug:
    img_path = "".join(single_json['data']['ocr'].split('-')[-1:])  
    letter = img_path.split('_')[0]
    number = img_path.split('_')[1].split('.')[0]
  # img_path with augmentation
  else:
    img_path = single_json['data']['ocr'].split('_')
    letter = img_path[-2]
    number = img_path[-1].split('.')[0]
        
  code = f"{letter} ({number}).jpg"
  return code


def _process_json_bulk(bulk_raw,aug):
  result = []
  
  for single_json in bulk_raw:
    image_code = _get_image_code(single_json,aug)
    single_gt = _process_json_single(single_json)
    
    single_output = {
      "image_code": image_code,
      "gt_parse": single_gt,
      "meta": {},
      "valid_line": {},
      "roi": {},
      "repeating_symbol": [],
      "dontcare": []
    }
    result.append(single_output)
  
  return result

# Frocesses single JSON file given a path
def get_processed_content(filepath,aug=False):
  file = open(filepath)
  raw_json = json.load(file)
  
  return _process_json_bulk(raw_json,aug)

# Processes all raw JSON files from the directory following the structure:
# raw:
# - A:
# - - <A-files>
# - B:
# - - <B-files>
# ...

def get_processed_all(jsons_raw_dirpath, aug=False):
    
  cwd = os.getcwd()

  # gets parent directory and absolute path to it
  cwd = os.path.abspath(os.path.join(cwd, os.pardir))

  # a complete path to JSON files
  # path = os.path.join(cwd, jsons_raw_dirpath)
  path = jsons_raw_dirpath
  dir_list = os.listdir(path)

  result = []
  if not aug:
    for subdir_name in dir_list:
      # Path to subdirectory (ex. .../A, .../B)
      subdir_path = path + subdir_name
      dir_content = os.listdir(subdir_path)
      
      for filename in dir_content:
        # Path to json file (ex. .../A/A_1-50.json)
        filepath = subdir_path + '/' + filename
        ext = filename.split('.')[-1]
        if ext == 'json':
          proc_json = get_processed_content(filepath)
          for any in proc_json:
            result.append(any)
  # for augmented data
  else:
    for file in dir_list:
      
      filepath = os.path.join(path,file)
      proc_json = get_processed_content(filepath,aug)
      for any in proc_json:
        result.append(any)

  return result