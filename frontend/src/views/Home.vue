<template>
  <meta charset=“UTF-8”>
  <ParticipantDataDialog></ParticipantDataDialog>
  <Dialog v-model:visible="displayThankYou" :style="{width: '50vw'}" :modal="true"
          :closable="false" :closeOnEscape="false">
    <p class="p-mb-3 p-text-center">Thank you for your participation!</p>
    <p class="p-mb-3 p-text-center">You may close the application tab now.</p>
  </Dialog>
  <Card class="noTotalWidth p-shadow-5">
    <template #title>
      <div class="title-wrapper">
        <span class="title"> &#x1F52C; &#x1F9A0; &#x1F58D; &#x1F3A8; &#x2705; &#x1F19A; &#x274E; &#x1F914; &#x1F4E4; </span>
      </div>
    </template>
    <template #content>
      <div class="tool-wrapper">
        <div class="p-d-flex p-jc-center">
          <div class="p-mx-2 p-my-2">
            <SelectButton v-model="brushType"
                          :options="brushOptions"
                          dataKey="value"
                          optionLabel="name"
                          optionValue="value"/>
          </div>
          <div class="p-mx-2 p-my-2">
            <Dropdown
              v-model="brushSize"
              :options="brushSizes"
              optionLabel="label"
              optionValue="size"
              placeholder="2px"/>
          </div>
          <div class="p-mx-2 p-my-2">
            <Button icon="pi pi-undo" label="Undo"
                    @click="undo()"
                    :disabled="isLoadingOrSubmitting || hasNoScribbles"/>
          </div>
<!--          <div class="p-mx-2 p-my-2">-->
<!--            <Button icon="pi pi-refresh" label="Redo" :disabled="true"/>-->
<!--          </div>-->
          <div class="p-mx-2 p-my-2">
            <Button icon="pi pi-trash" label="Clear All"
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
          <div class="p-d-flex p-flex-column p-jc-start p-mx-1 p-my-2">
            <p class="p-jc-start p-my-2">Mask Opacity: {{ `${maskOpacity} %` }}</p>
            <Slider class="p-my-2" id="maskOpacitySlider"
                    v-model="maskOpacity"
                    :step="5"
                    :min="0"
                    :max="100"
            />
          </div>
        </div>
      </div>
      <div class="progression-wrapper">
        <ConfirmPopup></ConfirmPopup>
        <div class="p-d-flex p-jc-center">
          <div class="p-mx-2 p-my-2">
            <Button icon="pi pi-cloud-upload" label="Segment" v-tooltip.bottom="'Submit scribbles to receive a segmentation'"
                    @click="segment()"
                    :loading="isLoadingSegmentation"
                    :disabled="!hasMadeNewEdits || hasNoScribbles || isSubmittingSegmentation || isImageLoading"/>
          </div>
          <div class="p-mx-2 p-my-2">
            <Button icon="pi pi-check" label="Finish" v-tooltip.bottom="'Submit mask and move on to next image'"
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
import {
  submissionWarnings,
  scribbleSubmissionSuccess,
  segmentationSubmission,
  fatalError
} from "@/helpers/toastMessages";
import {getTestImageSet} from "@/helpers/testImages";

export default {
  name: "App",
  components: {
    ParticipantDataDialog,
    InteractionCanvas
  },
  data() {
    return {
      displayThankYou: false,
      brushOptions: [
        {name: 'Cell', value: 'fg', icon: 'pi pi-circle-off'},
        {name: 'Background', value: 'bg', icon: 'pi pi-circle-on'}
      ],
    };
  },

  computed: {
    ...mapGetters({
      brushSizes: 'getBrushSizes',
      currentImageIndex: 'getCurrentImageIndex',
      numberOfTestImages: 'getNumberOfTestImages',
      isImageLoading: 'getIsImageLoading',
      isLoadingSegmentation: 'isLoadingSegmentation',
      isSubmittingSegmentation: 'isSubmittingSegmentation',
      hasNoScribbles: 'hasNoScribbles',
      hasMadeNewEdits: 'getHasMadeNewEdits',
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

    maskOpacity: {
      get() {
        return this.$store.getters.getMaskOpacity;
      },
      set(opacity) {
        this.$store.commit({
          type: 'SET_MASK_OPACITY',
          opacity: opacity
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
    window.addEventListener('beforeunload', this.preventNav,  { capture: true });

    let randId = [...Array(64)].map(() => Math.floor(Math.random()*36).toString(36)).join('');
    this.$store.dispatch('setSessionId', randId);

    let testImages = getTestImageSet();
    this.$store.dispatch('setTestImages', testImages);
  },

  beforeUnmount() {
    window.removeEventListener('beforeunload', this.preventNav, { capture: true });
  },

  beforeRouteLeave(to, from, next) {
    if (window.confirm('You will lose your current progress.')) {
      next();
    }
    else {
      next(false);
    }
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
        .then(() => {
          this.$toast.add(scribbleSubmissionSuccess(this.scribbleCounter));
        })
        .catch((error) => {
          // const errorString = e.toString();
          console.error(`SEGM FAILED for ${currentImageIndex} with ${error}`);
          // if (errorString.includes('Img') || errorString.includes('Timeout')) {
          this.$toast.add(fatalError);
          // }
          // else {
          //   this.$toast.add(segmentationSubmission.error);
          // }
        });
      this.setIsLoadingFlag(false);
    },

    finish(event) {
      this.$confirm.require({
        target: event.currentTarget,
        message: 'Have you picked your most accurate segmentation from the dropdown menu?',
        icon: 'pi pi-question-circle',
        acceptLabel: 'Proceed',
        rejectLabel: 'Cancel',
        accept: () => {
          this.handleSubmission();
        },
        reject: () => {},
      });
    },

    async handleSubmission() {
      this.setIsSubmittingFlag(true);
      try {
        await this.$store.dispatch('submitDisplayedMask');
      } catch(e) {
        console.error(`MASK SUBM FAILED with ${e}`);
        this.$toast.add(segmentationSubmission.error);
        this.setIsSubmittingFlag(false);
        return;
      }

      this.$toast.add(segmentationSubmission.success);
      this.incrementImageId();
      if (!this.isSessionFinished) {
        this.$refs.ic.resetForNextImage();
        await this.$refs.ic.loadImage();  //TODO possible error unhandled
      }
      else {
        window.removeEventListener('beforeunload', this.preventNav);
        this.displayThankYou = true;
      }
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
    width: 100%;
    margin-left: auto;
    margin-right: auto;
  }
</style>
