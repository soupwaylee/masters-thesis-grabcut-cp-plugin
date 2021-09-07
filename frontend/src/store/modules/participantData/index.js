import {APIService as grabcutAPIService} from "@/api/grabcutAPI";
import {root} from "../../../../.eslintrc";

const grabcutService = new grabcutAPIService();

const state = {
  ageGroup: null,
  academicField: null,
};

const mutations = {
  SET_AGE_GROUP (state, payload) {
    state.ageGroup = payload.ageGroup;
  },
  SET_ACADEMIC_FIELD (state, payload) {
    state.academicField = payload.academicField;
  }
};

const actions = {
  setAgeGroup ({ commit }, payload) {
    commit({type: 'SET_AGE_GROUP', ageGroup: payload});
  },

  setAcademicField ({ commit }, payload) {
    commit({type: 'SET_ACADEMIC_FIELD', academicField: payload});
  },

  async submitParticipantData ({state, rootState}) {
    return grabcutService.submitParticipantData(
      rootState.interactionSessionModule.sessionId,
      state.ageGroup,
      state.academicField
    )
  }
};

const getters = {
  getSelectedAgeGroup: state => state.ageGroup,
  getSelectedAcademicField: state => state.academicField,
};

const participantDataModule = {
  state,
  mutations,
  actions,
  getters,
}

export default participantDataModule;