const state = {
  brushType: 'fg',
  brushSize: 1,
  currentlyDisplayedSegmentation: null,
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
  }
};

const getters = {
  getBrushType: state => state.brushType,
  getBrushSize: state => state.brushSize,
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