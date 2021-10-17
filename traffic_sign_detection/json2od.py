import os
import tqdm
import json

# Constants
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

JSON_DIR = os.path.join(__location__,"ann")
json_list = os.listdir(JSON_DIR)


def json2od(json_name, base_dir):

    json_path = os.path.join(base_dir, json_name)
    
    # Read json file
    with open(json_path, 'r') as f:
        jsonfile = json.load(f)
        objects = jsonfile['objects']
        
        # If there is no object in the image, return NULL
        if len(objects) == 0:
            return NULL
        
        # Create empty list
        annotations = []
        for obj in objects:
            if obj['classTitle']=='Traffic Sign':
                obj_class_pts = obj['points']['exterior']
                obj_id = 0
                
                # Eliminate small ones 
                if (obj_class_pts[1][0] - obj_class_pts[0][0]) < 16 or (obj_class_pts[1][1] - obj_class_pts[0][1]) < 16:
                    continue
                
                # Add into list
                strlabel = str(obj_class_pts[0][0]) + ',' + str(obj_class_pts[0][1]) + ',' + str(obj_class_pts[1][0]) + ',' + str(obj_class_pts[1][1]) + ',' + str(obj_id)
                annotations.append(strlabel)
    
    # Modify list
    strlabel = ''
    for idx in range(len(annotations)):
        if idx != 0:
            strlabel += ' '

        strlabel += annotations[idx]

    return strlabel

# For 5 json files
for json_name in tqdm.tqdm(json_list[:5]):
    # Display the function output
    print(json2od(json_name, JSON_DIR))


IMAGE_DIR = os.path.join(__location__,"img")
OD_LABEL = os.path.join(__location__,"allLabel.txt")
# Open txt file
f = open(OD_LABEL, "w+")

# For every json file
for json_name in tqdm.tqdm(json_list):
    image_name = os.path.splitext(json_name)[0]
    # Change from png to jpg
    image_name = os.path.splitext(image_name)[0] + ".jpg"
    # Construct Line
    image_path = os.path.join(IMAGE_DIR, image_name)
    line = image_path+' '+json2od(json_name, JSON_DIR)+'\n'
    # Write down
    f.write(line)

# Close txt file
f.close()
