import cv2 as cv
import mediapipe as mp

from src.utils import timestamp


class Gesture:
    def __init__(self, model_path, do_on_gesture, do_on_nothing):
        self.model_path = model_path

        self.do_on_gesture = do_on_gesture
        self.do_on_nothing = do_on_nothing

        self.base_options = mp.tasks.BaseOptions
        self.GestureRecognizer = mp.tasks.vision.GestureRecognizer
        self.GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
        self.GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
        self.VisionRunningMode = mp.tasks.vision.RunningMode

    def _print_result(self, result: mp.tasks.vision.GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
        if result.gestures.__len__() > 0:
            self.do_on_gesture(result)
        else:
            self.do_on_nothing()

    def recognition(self):
        vid = cv.VideoCapture(0)

        options = self.GestureRecognizerOptions(
            base_options=self.base_options(model_asset_path=self.model_path),
            running_mode=self.VisionRunningMode.LIVE_STREAM,
            result_callback=self._print_result)
        with self.GestureRecognizer.create_from_options(options) as recognizer:
            while cv.waitKey(1) & 0xFF != ord('a'):
                ret, frame = vid.read()

                mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
                recognizer.recognize_async(mp_image, timestamp())

        vid.release()
        cv.destroyAllWindows()
