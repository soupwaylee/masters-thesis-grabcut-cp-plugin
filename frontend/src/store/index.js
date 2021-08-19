import { createStore } from 'vuex';
import canvasModule from '@/store/modules/canvas';
import interactionSessionModule from '@/store/modules/interactionSession'
import segmentationModule from '@/store/modules/segmentation';

export default createStore({
  modules: {
    canvasModule,
    interactionSessionModule,
    segmentationModule,
  }
});
