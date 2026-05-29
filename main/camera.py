import cv2 as cv
from ultralytics import YOLO

model = YOLO("yolov8n")

class camera:
    def __init__(self,source = 0):
        self.cm = cv.VideoCapture(source)
        while True:
            ret,frame = self.cm.read()
            if not ret:
                break
            results = model(frame)
            for result in results:
                for box in result.boxes:
                    cls_id = int(box.cls[0])        
                    label = model.names[cls_id]     

                    if label == "person":          
                        conf = float(box.conf[0])   
                        x1, y1, x2, y2 = map(int, box.xyxy[0])

                        # Draw rectangle
                        cv.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

                        # Draw label + confidence
                        text = f"Person {conf:.2f}"
                        cv.putText(frame, text, (x1, y1 - 10),
                                   cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            # Show person count on frame
            person_count = sum(
                1 for r in results
                for box in r.boxes
                if model.names[int(box.cls[0])] == "person"
            )
            cv.putText(frame, f"Persons: {person_count}", (20, 40),
                       cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv.imshow("window",frame)
            if cv.waitKey(18) & 0xFF == ord('q'):
                break
        
        self.cm.release()
        cv.destroyAllWindows()

            # for box in result:
            #     boxes = box

obj = camera("a.mp4")


