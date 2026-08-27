import os
from pathlib import Path
import base64
import cv2
import face_recognition
import numpy as np

DEFAULT_TOLERANCE = 0.48

def available():
    return cv2 is not None and face_recognition is not None

def decode_data_url(data_url: str):
    if not available() or not data_url or ',' not in data_url:
        raise ValueError('Face-recognition dependencies or image data are missing')
    raw = base64.b64decode(data_url.split(',',1)[1], validate=True)
    arr = np.frombuffer(raw, np.uint8)
    frame = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if frame is None:
        raise ValueError('Unable to decode image')
    return frame

def _face_locations(rgb_image, upsample=1):
    return face_recognition.face_locations(rgb_image, model='hog', number_of_times_to_upsample=upsample)

def image_quality(frame, location):
    top, right, bottom, left = location
    h, w = frame.shape[:2]
    width, height = right-left, bottom-top
    if width < max(110, int(w*0.20)) or height < max(110, int(h*0.20)):
        return False, 'Move closer so the face fills more of the frame'
    gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    brightness=float(np.mean(gray))
    if brightness < 50: return False, 'Image is too dark'
    if brightness > 220: return False, 'Image is too bright'
    blur_score=float(cv2.Laplacian(gray, cv2.CV_64F).var())
    if blur_score < 45: return False, 'Image is too blurry; hold still'
    if left < 3 or top < 3 or right > w-3 or bottom > h-3:
        return False, 'Keep the whole face inside the camera frame'
    return True, 'OK'

def encode_frame(data_url: str):
    frame=decode_data_url(data_url)
    rgb=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    locations=_face_locations(rgb, upsample=1)
    if len(locations)!=1:
        raise ValueError('Exactly one face must be visible')
    ok,msg=image_quality(frame, locations[0])
    if not ok:
        raise ValueError(msg)
    encs=face_recognition.face_encodings(rgb, locations, num_jitters=4, model='small')
    if not encs:
        raise ValueError('Could not create a face encoding')
    return encs[0].tolist()

def get_face_encodings(user_folder):
    encodings=[]
    folder=Path(user_folder)
    if not folder.is_dir(): return encodings
    for path in sorted(folder.glob('*.jpg')):
        try:
            bgr=cv2.imread(str(path))
            if bgr is None: continue
            rgb=cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
            locations=_face_locations(rgb,upsample=1)
            if len(locations)!=1: continue
            ok,_=image_quality(bgr,locations[0])
            if not ok: continue
            found=face_recognition.face_encodings(rgb,locations,num_jitters=4,model='small')
            if found: encodings.append(found[0])
        except Exception:
            continue
    return encodings

def recognize_faces(frame, upsample=1):
    rgb=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    locations=_face_locations(rgb,upsample=upsample)
    encodings=face_recognition.face_encodings(rgb,locations,num_jitters=2,model='small')
    return locations,encodings

def _user_score(known_encodings,test_encoding):
    distances=face_recognition.face_distance(known_encodings,test_encoding)
    if len(distances)==0: return None
    ordered=np.sort(distances)
    top=ordered[:min(5,len(ordered))]
    return float(top[0]*0.45+np.mean(top)*0.35+np.median(top)*0.20)

def match_distance(probe, encodings):
    if not encodings or not available(): return None
    known=np.asarray(encodings,dtype=float)
    if known.size==0: return None
    if known.ndim==1: known=np.expand_dims(known,0)
    distances=face_recognition.face_distance(known,np.asarray(probe,dtype=float))
    return float(np.min(distances)) if len(distances) else None

def best_match(probe, encodings, tolerance=DEFAULT_TOLERANCE):
    d=match_distance(probe,encodings)
    return d is not None and d<=tolerance

def best_match_for_encoding(test_encoding, known_users, tolerance=DEFAULT_TOLERANCE):
    candidates=[]
    for user,path_or_enc in known_users:
        try:
            if isinstance(path_or_enc,(str,os.PathLike)):
                if not os.path.exists(path_or_enc): continue
                enc=np.load(path_or_enc,allow_pickle=False)
            else:
                enc=np.asarray(path_or_enc,dtype=float)
            if enc.size==0: continue
            if enc.ndim==1: enc=np.expand_dims(enc,0)
            score=_user_score(enc,test_encoding)
            if score is not None: candidates.append((score,user))
        except Exception:
            continue
    if not candidates: return None,None,None
    candidates.sort(key=lambda item:item[0])
    best_user=candidates[0][1]
    best_score=candidates[0][0]
    second_score=candidates[1][0] if len(candidates)>1 else None
    if best_score>tolerance: return None,best_score,second_score
    return best_user,best_score,second_score
