import { createStore } from 'vuex';
import canvasModule from '@/store/modules/canvas';
import interactionSessionModule from '@/store/modules/interactionSession'
import segmentationModule from '@/store/modules/segmentation';
import participantDataModule from '@/store/modules/participantData';

export default createStore({
  modules: {
    participantDataModule,
    canvasModule,
    interactionSessionModule,
    segmentationModule,
  }
});
