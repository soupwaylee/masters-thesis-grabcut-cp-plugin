<template>
  <Card class="noTotalWidth p-shadow-5">
    <template #title>
      <div class="title-wrapper">
        <span class="title">GrabCut</span>
        <Button icon="pi pi-info-circle"
          @click="openGrabCutInfo"/>
        <Dialog v-model:visible="displayInfo"
          :closeOnEscape="true"
          :dismissableMask="true"
          :closable="true">
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
        <label for="sizeSlider">Size: {{ brushSize }}</label>
        <Slider id="sizeSlider"
                v-model="brushSize"
                :min="brushSizeRange[0]"
                :max="brushSizeRange[1]"
        />
        <span class="p-buttonset">
          <SelectButton v-model="brushType" :options="brushOptions" optionLabel="name" optionValue="value" dataKey="value"/>
          <Button label="Undo" icon="pi pi-undo" @click="$refs.ic.undoLastStroke()"/>
          <Button label="Redo" icon="pi pi-refresh" />
          <Button label="Clear" icon="pi pi-trash" @click="$refs.ic.clearDrawings()"/>
        </span>
      </div>
      <InteractionCanvas ref="ic"/>
      <div class="progression-wrapper">
        <Button label="Segment" icon="pi pi-cloud-upload" />
        <Button label="Finish" icon="pi pi-check" />
      </div>
    </template>
  </Card>
</template>

<script>
// import { ref } from 'vue';
// import { APIService as grabcutAPIService } from "../api/grabcutAPI";
// const grabcutAS = new grabcutAPIService();
import InteractionCanvas from "@/components/InteractionCanvas";

export default {
  name: "App",
  components: {
    InteractionCanvas
  },
  data() {
    return {
      displayInfo: false, //TODO this should be true for deployment (for the purpose of showing instructions etc.)
      brushOptions: [
        {name: 'Foreground', value: 'fg', icon: 'pi pi-circle-off'},
        {name: 'Background', value: 'bg', icon: 'pi pi-circle-on'}
      ],
			brushSizeRange: [1,30],
    };
  },
  computed: {
    brushType: {
      get () {
        return this.$store.getters.getBrushType;
      },
      set (type) {
        this.$store.commit({
          type: 'SET_BRUSHTYPE',
          brushType: type
        });
      }
    },
    brushSize: {
      get () {
        return this.$store.getters.getBrushSize;
      },
      set (size) {
        this.$store.commit({
          type: 'SET_BRUSHSIZE',
          brushSize: size
        });
      }
    },
  },
  methods: {
		openGrabCutInfo() {
			this.displayInfo = true;
		},
  },
};
</script>

<style lang="scss">
.noTotalWidth {
  width: 80%;
  margin: auto;
}
</style>
