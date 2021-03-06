<template>
  <Toast position="bottom-right" group="br"/>
  <Dialog v-model:visible="displayForm" :style="{width: '50vw'}"
          :modal="true" :closable="false" :closeOnEscape="false">
    <template #header>
      <h3>Please tell us a bit about yourself.</h3>
    </template>
    <div>
      <div>
        <h4>How old are you?</h4>
        <Dropdown v-model="selectedAgeGroup" :options="ageGroupOptions" optionLabel="range" optionValue="range"
                  placeholder="- Select -"/>
        <p :style="missingAgeGroupStyle">* Please make a selection</p>
      </div>
      <div>
        <h4>Which academic background do you identify with?</h4>
        <p>If you're in an interdisciplinary area,
          pick the higher level field which you most strongly identify with.</p>
        <Dropdown v-model="selectedAcademicField" :options="academicFieldOptions" optionLabel="field"
                  optionValue="field" placeholder="- Select -"/>
        <p :style="missingAcademicFieldStyle">* Please make a selection</p>
      </div>
    </div>
    <template #footer>
      <Button label="Submit" icon="pi pi-check" @click="submit()" autofocus/>
    </template>
  </Dialog>
</template>

<script>
import {mapActions, mapGetters} from 'vuex';
import {participantDataSubmission} from "@/helpers/toastMessages";

export default {
  name: 'ParticipantDataDialog',

  data() {
    return {
      displayForm: true,
      displayAgeGroupWarning: false,
      displayMissingAcademicFieldWarning: false,

      ageGroupOptions: [
        {range: 'Under 18', rangeId: 0},
        {range: '18-24', rangeId: 1},
        {range: '25-34', rangeId: 2},
        {range: '35-44', rangeId: 3},
        {range: '45-54', rangeId: 4},
        {range: '55-64', rangeId: 5},
        {range: 'Above 64', rangeId: 6}
      ],
      academicFieldOptions: [
        {field: 'Medicine and Health Science', fieldId: 0},
        {field: 'Electrical and Computer Engineering', fieldId: 1},
        {field: 'Computer Science', fieldId: 2},
        {field: 'Mathematics', fieldId: 3},
        {field: 'Physics', fieldId: 4},
        {field: 'Management and Business Studies', fieldId: 5},
        {field: 'Biology', fieldId: 6},
        {field: '(Bio-)chemistry', fieldId: 7},
        {field: 'Chemical Engineering and Material Science', fieldId: 8},
        {field: 'Mechanical Engineering', fieldId: 9},
        {field: 'Humanities (e.g. Philosphy, Languages, Arts, Law)', fieldId: 10},
        {field: 'Social Science (e.g. Political Sciences, Psychology)', fieldId: 11},
        {field: 'Education Science', fieldId: 12},
        {field: 'Civil-, Geo- and Environmental Engineering', fieldId: 13}
      ],
    };
  },

  computed: {
    ...mapGetters({
      sessionId: 'getSessionId',
    }),
    selectedAgeGroup: {
      get() {
        return this.$store.getters.getSelectedAgeGroup;
      },
      set(ageGroup) {
        this.setAgeGroup(ageGroup);
      },
    },
    selectedAcademicField: {
      get() {
        return this.$store.getters.getSelectedAcademicField;
      },
      set(field) {
        this.setAcademicField(field);
      },
    },
    isDemographicsDataFilled() {
      return this.selectedAgeGroup !== null
        && this.selectedAcademicField !== null;
    },
    missingAgeGroupStyle() {
      return {
        color: 'red',
        visibility: this.displayAgeGroupWarning ? 'visible' : 'hidden',
      };
    },
    missingAcademicFieldStyle() {
      return {
        color: 'red',
        visibility: this.displayMissingAcademicFieldWarning ? 'visible' : 'hidden',
      };
    },
  },

  methods: {
    ...mapActions([
      'setAgeGroup',
      'setAcademicField',
      'submitParticipantData'
    ]),

    async submit() {
      this.displayAgeGroupWarning = this.selectedAgeGroup === null;
      this.displayMissingAcademicFieldWarning = this.selectedAcademicField === null;

      if (this.isDemographicsDataFilled) {
        await this.submitParticipantData()
          .then(
            () => {
              this.$toast.add(participantDataSubmission.success);
              this.displayForm = false;
            },
            error => {
              console.error(error);
            }
          );
      }
    },
  },
}
</script>