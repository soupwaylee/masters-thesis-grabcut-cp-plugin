<template>
  <ParticipantDataDialog></ParticipantDataDialog>
  <Card class="noTotalWidth p-shadow-5">
    <template #title>
      <div class="title-wrapper">
        <span class="title">GrabCut</span>
        <Button icon="pi pi-info-circle"
                @click="openGrabCutInfo"/>
        <Dialog v-model:visible="displayInfo"
                :closable="true"
                :closeOnEscape="true"
                :dismissableMask="true">
          <div class="dialog-header">
            <h3>GrabCut</h3>
          </div>

          This is GrabCut. Explanations will follow.
          <!-- Mark a subset of foreground and background pixels. -->
          <!-- Submit to check the segmentation output based on your provided input. -->
          <!-- Click Finish to move to the next image. -->
          <!-- Once you click Finish you can't go back to the previous image -->

        </Dialog>
      </div>
    </template>
    <template #content>
      <div class="tool-wrapper">
        <div class="p-d-flex p-flex-column p-jc-center">
          <label class="p-my-1">Brush Size: {{ brushSize }}</label>
          <Slider class="p-my-1" id="sizeSlider"
                  v-model="brushSize"
                  :max="brushSizeRange[1]"
                  :min="brushSizeRange[0]"
          />
        </div>
        <div class="p-d-flex p-jc-center">
          <div class="p-mx-2 p-my-2">
            <SelectButton v-model="brushType"
                          :options="brushOptions"
                          dataKey="value"
                          optionLabel="name"
                          optionValue="value"/>
          </div>
          <div class="p-mx-2 p-my-2">
            <Button icon="pi pi-undo" label="Undo"
                    @click="undo()"
                    :disabled="isLoadingOrSubmitting || hasNoScribbles"/>
          </div>
          <div class="p-mx-2 p-my-2">
            <Button icon="pi pi-refresh" label="Redo" :disabled="true"/>
          </div>
          <div class="p-mx-2 p-my-2">
            <Button icon="pi pi-trash" label="Clear"
                    @click="clear()"
                    :disabled="isLoadingOrSubmitting || hasNoScribbles"/>
          </div>
        </div>
      </div>
      <div class="p-d-flex p-jc-center">
        <div class="p-d-flex p-mx-1 p-my-2"><InteractionCanvas ref="ic"/></div>
        <div class="p-d-flex p-flex-column p-jc-start p-ml-2 p-my-2">
          <ToggleButton class="p-mx-1 p-my-2" v-model="isCanvasVisible" onLabel="Drawings" offLabel="Drawings" onIcon="pi pi-eye" offIcon="pi pi-eye-slash" />
          <ToggleButton class="p-mx-1 p-my-2" v-model="isMaskVisible" onLabel="Segmentation" offLabel="Segmentation" onIcon="pi pi-eye" offIcon="pi pi-eye-slash" />
        </div>
      </div>
      <div class="progression-wrapper">
        <ConfirmPopup></ConfirmPopup>
        <div class="p-d-flex p-jc-center">
          <div class="p-mx-2 p-my-2">
            <Button icon="pi pi-cloud-upload" label="Segment"
                    @click="segment()"
                    :loading="isLoadingSegmentation"
                    :disabled="hasNoScribbles || isSubmittingSegmentation || isImageLoading"/>
          </div>
          <div class="p-mx-2 p-my-2">
            <Button icon="pi pi-check" label="Finish"
                    @click="finish($event)"
                    :loading="isSubmittingSegmentation"
                    :disabled="(selectedSegmentation === null) || isLoadingSegmentation || isImageLoading"/>
          </div>
        </div>
      </div>
      <div v-if="hasSegmentations" class="p-mx-1 p-my-2">
        <Dropdown
          v-model="selectedSegmentation"
          :options="segmentationContexts"
          optionLabel="submissionTime"
          placeholder="Pick a Segmentation" />
      </div>
    </template>
  </Card>
</template>

<script>
import {mapGetters, mapActions} from 'vuex';
import InteractionCanvas from "@/components/InteractionCanvas";
import ParticipantDataDialog from "@/components/ParticipantDataDialog";
import {submissionWarnings, scribbleSubmissionSuccess, segmentationSubmission} from "@/helpers/toastMessages";
import {getTestImageSet} from "@/helpers/testImages";

export default {
  name: "App",
  components: {
    ParticipantDataDialog,
    InteractionCanvas
  },
  data() {
    return {
      displayInfo: false, //TODO this should be true for deployment (for the purpose of showing instructions etc.)
      brushOptions: [
        {name: 'Foreground', value: 'fg', icon: 'pi pi-circle-off'},
        {name: 'Background', value: 'bg', icon: 'pi pi-circle-on'}
      ],
      brushSizeRange: [1, 30],
    };
  },

  computed: {
    ...mapGetters({
      currentImageIndex: 'getCurrentImageIndex',
      numberOfTestImages: 'getNumberOfTestImages',
      isImageLoading: 'getIsImageLoading',
      isLoadingSegmentation: 'isLoadingSegmentation',
      isSubmittingSegmentation: 'isSubmittingSegmentation',
      hasNoScribbles: 'hasNoScribbles',
      hasSegmentations: 'hasSegmentations',
      segmentationContexts: 'getSegmentationContexts',
      scribbleCounter: 'getScribbleCounter',
      foregroundScribbleCounter: 'getForegroundScribbleCounter',
      backgroundScribbleCounter: 'getBackgroundScribbleCounter',
    }),

    isSessionFinished() {
      return this.currentImageIndex > (this.numberOfTestImages - 1);
    },

    isLoadingOrSubmitting() {
      return this.isImageLoading || this.isLoadingSegmentation || this.isSubmittingSegmentation;
    },

    hasNoForegroundScribbles() {
      return this.foregroundScribbleCounter === 0;
    },

    hasNoBackgroundScribbles() {
      return this.backgroundScribbleCounter === 0;
    },

    brushType: {
      get() {
        return this.$store.getters.getBrushType;
      },
      set(type) {
        this.$store.commit({
          type: 'SET_BRUSHTYPE',
          brushType: type
        });
      }
    },

    brushSize: {
      get() {
        return this.$store.getters.getBrushSize;
      },
      set(size) {
        this.$store.commit({
          type: 'SET_BRUSHSIZE',
          brushSize: size
        });
      }
    },

    isCanvasVisible: {
      get() {
        return this.$store.getters.getIsCanvasVisible;
      },
      set(isVisible) {
        this.$store.commit({
          type: 'SET_IS_CANVAS_VISIBLE',
          isCanvasVisible: isVisible,
        });
      }
    },

    isMaskVisible: {
      get() {
        return this.$store.getters.getIsMaskVisible;
      },
      set(isVisible) {
        this.$store.commit({
          type: 'SET_IS_MASK_VISIBLE',
          isMaskVisible: isVisible,
        });
      }
    },

    selectedSegmentation: {
      get() {
        return this.$store.getters.getDisplayedSegmentation;
      },
      set(segmentation) {
        this.$store.commit({
          type: 'SET_CURRENTLY_DISPLAYED_SEGMENTATION',
          segmentation: segmentation
        });
      },
    }
  },

  created() {
    let randId = [...Array(64)].map(() => Math.floor(Math.random()*36).toString(36)).join('');
    this.$store.dispatch('setSessionId', randId);

    let testImages = getTestImageSet();
    this.$store.dispatch('setTestImages', testImages);
  },

  beforeMount() {
    window.addEventListener('beforeunload', this.preventNav);
  },

  beforeDestroy() {
    window.removeEventListener('beforeunload', this.preventNav);
  },

  beforeRouteLeave(to, from, next) {
    if (!window.confirm('You will lose the current progress.')) {
      return;
    }
    next();
  },

  methods: {
    ...mapActions([
      'setIsLoadingFlag',
      'setIsSubmittingFlag',
      'incrementImageId',
    ]),

    preventNav(event) {
      event.preventDefault();
      event.returnValue = "";
    },

    openGrabCutInfo() {
      this.displayInfo = true;
    },

    undo() {
      this.$refs.ic.undoLastStroke();
    },

    clear() {
      this.$refs.ic.clearDrawings();
    },

    async segment() {
      if (this.hasNoForegroundScribbles) {
        this.$toast.add(submissionWarnings.noForegroundScribbles);
        return;
      }
      if (this.hasNoBackgroundScribbles) {
        this.$toast.add(submissionWarnings.noBackgroundScribbles);
        return;
      }
      this.setIsLoadingFlag(true);
      await this.$refs.ic.segment()
        .then(
          () => {
            this.$toast.add(scribbleSubmissionSuccess(this.scribbleCounter));
          }
        );
      this.setIsLoadingFlag(false);
    },

    finish(event) {
      this.$confirm.require({
        target: event.currentTarget,
        message: 'Are you sure you want to submit the displayed segmentation mask and move on to the next image?',
        icon: 'pi pi-exclamation-triangle',
        accept: () => {
          this.submit();
          this.incrementImageId();
          if (!this.isSessionFinished) {
            this.$refs.ic.loadImage();
          }
          else {
            // open popup
            console.log('Finished');
          }
        },
        reject: () => {},
      });
      //TODO increment image ID
    },

    async submit() {
      this.setIsSubmittingFlag(true);
      await this.$refs.ic.submitDisplayedMask()
        .then(
          () => {
            this.$toast.add(segmentationSubmission.success);
          },
          error => {
            console.error(error);
          }
        );
      this.setIsSubmittingFlag(false);
    },
  },
};
</script>

<style lang="scss">
  .noTotalWidth {
    width: 80%;
    margin: auto;
  }

  .p-slider-horizontal {
    width: 75%;
    margin-left: auto;
    margin-right: auto;
  }
</style>
