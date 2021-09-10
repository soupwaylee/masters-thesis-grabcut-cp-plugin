const state = {
  brushType: 'fg',
  brushSize: 1,
  isCanvasEmpty: true,
  isImageLoading: false,
  currentlyDisplayedSegmentation: null,
  isCanvasVisible: true,
  isMaskVisible: true,
  visibilityToggleCategories: [
    {name: 'Canvas', key: 'C'},
    {name: 'Mask', key: 'M'},
  ],
  selectedVisibilities: [
    {name: 'Canvas', key: 'C'},
    {name: 'Mask', key: 'M'},
  ],
};

const mutations = {
  SET_BRUSHTYPE (state, payload) {
    state.brushType = payload.brushType;
  },
  SET_BRUSHSIZE (state, payload) {
    state.brushSize = payload.brushSize;
  },
  SET_IS_CANVAS_EMPTY (state, payload) {
    state.isCanvasEmpty = payload.isEmpty;
  },
  SET_IS_IMAGE_LOADING (state, payload) {
    state.isImageLoading = payload.isLoading;
  },
  SET_IS_CANVAS_VISIBLE (state, payload) {
    state.isCanvasVisible = payload.isCanvasVisible;
  },
  SET_IS_MASK_VISIBLE (state, payload) {
    state.isMaskVisible = payload.isMaskVisible;
  },
  SET_CURRENTLY_DISPLAYED_SEGMENTATION (state, payload) {
    state.currentlyDisplayedSegmentation = payload.segmentation;
  },
  SET_SELECTED_VISIBILITIES (state, payload) {
    state.selectedVisibilities = payload.selection;
  },
};

const actions = {
  setBrushType ({ commit }, payload) {
    commit('SET_BRUSHTYPE', payload);
  },
  setBrushSize ({ commit }, payload) {
    commit('SET_BRUSHSIZE', payload);
  },
  setIsCanvasEmptyFlag({ commit }, payload) {
    commit('SET_IS_CANVAS_EMPTY', payload);
  },
  setIsImageLoadingFlag({ commit }, isLoading) {
    commit({type: 'SET_IS_IMAGE_LOADING', isLoading: isLoading});
  },
  setSegmentationForDisplay ({ commit }, segmentation) {
    commit({
      type: 'SET_CURRENTLY_DISPLAYED_SEGMENTATION',
      segmentation: segmentation
    });
  },
  setVisibilitySelection ({ commit }, selection) {
    commit({
      type: 'SET_SELECTED_VISIBILITIES',
      selection: selection,
    });
  },
  resetCanvasState({ commit }) {
    commit({
      type: 'SET_BRUSHTYPE',
      brushType: 'fg'
    });
    commit({
      type: 'SET_BRUSHSIZE',
      brushSize: 1
    });
    commit({
      type: 'SET_CURRENTLY_DISPLAYED_SEGMENTATION',
      segmentation: null
    });
  }
};

const getters = {
  getBrushType: state => state.brushType,
  getBrushSize: state => state.brushSize,
  getIsCanvasEmpty: state => state.brushSize,
  getIsImageLoading: state => state.isImageLoading,
  getIsCanvasVisible: state => state.isCanvasVisible,
  getIsMaskVisible: state => state.isMaskVisible,
  getDisplayedSegmentation: state => state.currentlyDisplayedSegmentation,
  getVisibilityToggleCategories: state => state.visibilityToggleCategories,
  getSelectedVisibilities: state => state.selectedVisibilities,
  isCanvasDisplaySelected: state => state.selectedVisibilities.some(selection => selection.key === 'C'),
  isMaskDisplaySelected: state => state.selectedVisibilities.some(selection => selection.key === 'M'),
};

const canvasModule = {
  state,
  mutations,
  actions,
  getters,
}

export default canvasModule;