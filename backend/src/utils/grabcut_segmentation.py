import cv2 as cv
import numpy as np
from datetime import datetime
import logging
import app


log = logging.getLogger('app.sub')

"""
```
cv::GrabCutClasses {
  cv::GC_BGD = 0,
  cv::GC_FGD = 1,
  cv::GC_PR_BGD = 2,
  cv::GC_PR_FGD = 3
}
```
"""

class GrabCutSegmenter:
    img_shape = (384, 512)

    # TODO allow for further refinement with cv.GC_EVAL or cv.GC_EVAL_FREEZE_MODEL

    @staticmethod
    def pixels_to_gc_classes_array(target_idx, target_type, foreground=1, log_gc_classes=False):
        if len(target_idx) != len(target_type):
            app.logger.warning('Index-value mismatch')
            return
        elif len(target_idx) == 0:
            app.logger.warning('Empty lists')
            return
        else:
            gc_classes_array = np.empty(GrabCutSegmenter.img_shape, dtype=np.uint8).ravel()
            gc_classes_array.fill(cv.GC_PR_BGD)

            target_gc_classes = np.empty(len(target_type), dtype=np.uint8)
            target_gc_classes.fill(cv.GC_BGD)
            target_gc_classes[target_type] = cv.GC_FGD

            np.put(gc_classes_array, target_idx, target_gc_classes)

            if log_gc_classes:
                now = datetime.now()
                dt_str = now.strftime('%m-%d-%Y-%H%M%S')
                np.savez(f'scribbles/{dt_str}.npz', gc_classes_array)

            return gc_classes_array.reshape(GrabCutSegmenter.img_shape)

    @staticmethod
    def gc_segment(target_img, target_idx, target_type, iter_count=5, foreground=1):
        target_img_3c = cv.cvtColor(target_img, cv.COLOR_GRAY2RGB)
        manual_mask = GrabCutSegmenter.pixels_to_gc_classes_array(target_idx, target_type)
        if manual_mask is None:
            app.logger.info('Scribble mask is missing.')
            return
        try:
            bgd_model = np.zeros((1, 65), np.float64)
            fgd_model = np.zeros((1, 65), np.float64)
            grabcut_result, bgd_model, bgd_model = cv.grabCut(
                target_img_3c,
                manual_mask,
                None,
                bgd_model,
                fgd_model,
                iter_count,
                cv.GC_INIT_WITH_MASK
            )
            # mask_contrast_8bit = np.where((grabcut_result == 2) | (grabcut_result == 0), 0, 255).astype('uint8')
            mask_boolean = np.where((grabcut_result == 2) | (grabcut_result == 0), False, True).astype('bool')
            return np.ravel(mask_boolean).tolist()
        except Exception as exc:
            app.logger.error('Error during GrabCut segmentation', exc_info=True)
            raise RuntimeError('Failed to perform GrabCut') from exc
