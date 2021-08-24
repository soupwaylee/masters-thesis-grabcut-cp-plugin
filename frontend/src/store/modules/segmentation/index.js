import {APIService as grabcutAPIService} from "@/api/grabcutAPI";
import {
  getScribbleMaskContext,
  getScribblePixelCount,
  booleanMaskArrayToIntImageDataArray,
  getImageDataURIFromDataArray
} from "@/helpers/canvas";

const grabcutService = new grabcutAPIService();

const state = {
  /**
   * @typedef {Object} SegmentationContext
   * @property {number} dataUri Data URI representation of the segmentation mask
   *                            given the colormap defined in the InteractionCanvas
   * @property {string} submissionTime Annotation submission timestamp
   */
  segmentationContexts: [],
};

const mutations = {
  ADD_SEGMENTATION_CONTEXT(state, payload) {
    state.segmentationContexts.push(payload.maskContext);
  },
};

const actions = {
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

    console.table(interactionRecord);

    await grabcutService
      .segmentImage(interactionRecord, {scribbleIndices, scribbleTypes})
      .then(response => {
        const submissionTime = response.interactionRecord.submissionTime;
        const maskIntDataArray = booleanMaskArrayToIntImageDataArray(response.maskDataArray);

        const segmentationMaskContext = {
          dataUri: getImageDataURIFromDataArray(maskIntDataArray, colors),
          submissionTime: submissionTime,
        };

        commit({
          type: 'ADD_SEGMENTATION_CONTEXT',
          maskContext: segmentationMaskContext
        });
      }, error => {
        console.error(error);
      });
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