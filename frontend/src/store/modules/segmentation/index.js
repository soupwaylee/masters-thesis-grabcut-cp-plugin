import {APIService as grabcutAPIService} from "@/api/grabcutAPI";
import {
  getScribbleMaskContext,
  getScribblePixelCount,
  booleanMaskArrayToIntImageDataArray,
  booleanMaskArrayToReducedMaskNumberArray,
  getImageDataURIFromDataArray
} from "@/helpers/canvas";

const grabcutService = new grabcutAPIService();

const state = {
  /**
   * @typedef {Object} SegmentationContext
   * @property {number} dataUri Data URI representation of the segmentation mask
   *                            given the colormap defined in the InteractionCanvas
   * @property {number[]} reducedMask Array containing the foreground indices of a segmentation mask
   * @property {string} submissionTime Annotation submission timestamp
   * @property {string} interactionRecordId Interaction record UUID
   */
  segmentationContexts: [],
};

const mutations = {
  SET_SEGMENTATION_CONTEXTS(state, payload) {
    state.segmentationContexts = payload.contexts;
  },
  ADD_SEGMENTATION_CONTEXT(state, payload) {
    state.segmentationContexts.push(payload.maskContext);
  },
};

const actions = {
  clearSegmentations({commit}) {
    commit({
      type: 'SET_SEGMENTATION_CONTEXTS',
      contexts: []
    });
  },

  async getSegmentation({commit, rootState}, {imageData, colors}) {
    const interactionSessionState = rootState.interactionSessionModule;

    let {scribbleIndices, scribbleTypes} = getScribbleMaskContext(imageData);
    let {pixelCount, fgPixelCount, bgPixelCount} = getScribblePixelCount(scribbleIndices, scribbleTypes);
    let imageId = interactionSessionState.testImages[interactionSessionState.currentImageIndex];

    let interactionRecord = {
      'sessionId': interactionSessionState.sessionId,
      'imageId': imageId,
      "scribbles": interactionSessionState.scribbles,
      "foregroundScribbles": interactionSessionState.foregroundScribbles,
      "backgroundScribbles": interactionSessionState.backgroundScribbles,
      "annotatedPixels": pixelCount,
      "foregroundPixels": fgPixelCount,
      "backgroundPixels": bgPixelCount,
      "submissionIndex": interactionSessionState.submissionCounter,
      "firstInteractionTime": interactionSessionState.currentImageInteractionStartingTime,
      "submissionTime": interactionSessionState.segmentationRequestTime,
    }
    
    await grabcutService
      .segmentImage(interactionRecord, {scribbleIndices, scribbleTypes})
      .then(response => {
        const submissionTime = new Date(response.interactionRecord.submissionTime);
        const gmtIdx = submissionTime.toString().indexOf('GMT');

        const submissionTimeFormatted = submissionTime.toString().slice(0, gmtIdx - 1);
        const interactionRecordId = response.interactionRecord.id;
        const maskIntDataArray = booleanMaskArrayToIntImageDataArray(response.maskDataArray);

        const segmentationMaskContext = {
          dataUri: getImageDataURIFromDataArray(maskIntDataArray, colors),
          reducedMask: booleanMaskArrayToReducedMaskNumberArray(response.maskDataArray),
          interactionRecordId: interactionRecordId,
          submissionTime: submissionTimeFormatted,
        };

        commit({
          type: 'ADD_SEGMENTATION_CONTEXT',
          maskContext: segmentationMaskContext
        });
      }, error => {
        console.error(error);
      });
  },

  async submitDisplayedMask({rootState}) {
    const interactionState = rootState.interactionSessionModule;
    const canvasState = rootState.canvasModule;

    const sessionId = interactionState.sessionId;
    const imageId = interactionState.testImages[interactionState.currentImageIndex];
    const interactionRecordId = canvasState.currentlyDisplayedSegmentation.interactionRecordId;
    const currentReducedMask = canvasState.currentlyDisplayedSegmentation.reducedMask.toString();

    await grabcutService.submitSegmentation(sessionId, imageId, interactionRecordId, currentReducedMask);
  },

};

const getters = {
  getSegmentationContexts: state => state.segmentationContexts,
  hasSegmentations: state => state.segmentationContexts.length !== 0,
  getSegmentationCounter: state => state.segmentationContexts.length,
  getLatestSegmentation: state => state.segmentationContexts[state.segmentationContexts.length - 1],
};

const segmentationModule = {
  state,
  mutations,
  actions,
  getters,
}

export default segmentationModule;