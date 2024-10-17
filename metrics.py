import random 


def calculate_containment_ratio(box1, box2):
    # Compute the (x, y)-coordinates of the intersection rectangle
    xA = max(box1[0], box2[0])
    yA = max(box1[1], box2[1])
    xB = min(box1[2], box2[2])
    yB = min(box1[3], box2[3])

    interWidth = max(0, xB - xA)
    interHeight = max(0, yB - yA)
    interArea = interWidth * interHeight

    box1Area = (box1[2] - box1[0]) * (box1[3] - box1[1])

    containment_ratio = interArea / float(box1Area)
    return containment_ratio > 0.7


def is_bbox_similar(bbox1, bbox2, threshold=0.7):
    # Calculate the (x, y)-coordinates of the intersection rectangle
    xA = max(bbox1[0], bbox2[0])
    yA = max(bbox1[1], bbox2[1])
    xB = min(bbox1[2], bbox2[2])
    yB = min(bbox1[3], bbox2[3])

  
    interArea = max(0, xB - xA) * max(0, yB - yA)

    box1Area = (bbox1[2] - bbox1[0]) * (bbox1[3] - bbox1[1])
    box2Area = (bbox2[2] - bbox2[0]) * (bbox2[3] - bbox2[1])

    iou = interArea / float(box1Area + box2Area - interArea)
    return iou > threshold

def generate_color():
    """Generate a random BGR color that is not red."""
    while True:
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        # Check if the color is red
        if color != (0, 0, 255):
            return color