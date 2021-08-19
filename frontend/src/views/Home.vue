<template>
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
        <label for="sizeSlider">Size: {{ brushSize }}</label>
        <Slider id="sizeSlider"
                v-model="brushSize"
                :max="brushSizeRange[1]"
                :min="brushSizeRange[0]"
        />
        <span class="p-buttonset">
          <SelectButton v-model="brushType" :options="brushOptions" dataKey="value" optionLabel="name"
                        optionValue="value"/>
          <Button icon="pi pi-undo" label="Undo" @click="undo()"/>
          <Button icon="pi pi-refresh" label="Redo"/>
          <Button icon="pi pi-trash" label="Clear" @click="clear()"/>
        </span>
      </div>
      <InteractionCanvas ref="ic"/>
      <div class="progression-wrapper">
        <Button icon="pi pi-cloud-upload" label="Segment" @click="segment()"/>
        <Button icon="pi pi-check" label="Finish"/>
      </div>
    </template>
  </Card>
</template>

<script>
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
      brushSizeRange: [1, 30],
    };
  },
  computed: {
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
  },
  created() {
    let randId = [...Array(64)].map(() => Math.floor(Math.random()*36).toString(36)).join('');
    this.$store.dispatch('setSessionId', randId);
  },
  methods: {
    openGrabCutInfo() {
      this.displayInfo = true;
    },
    undo() {
      this.$refs.ic.undoLastStroke();
    },
    clear() {
      this.$refs.ic.clearDrawings();
    },
    segment() {
      this.$refs.ic.segment();
    }
  },
};
</script>

<style lang="scss">
.noTotalWidth {
  width: 80%;
  margin: auto;
}
</style>
