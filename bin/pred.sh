#python -m convert yolov3.cfg model/pretrain/yolov3.weights model/pretrain/yolo.h5
python -m yolo_pred --model model/pretrain/yolo.h5 --image \
  --model_path model/jd/jd.h5 \
  --classes_path model_data/jd_classes.txt \
  --anchors_path model_data/tiny_yolo_anchors.txt