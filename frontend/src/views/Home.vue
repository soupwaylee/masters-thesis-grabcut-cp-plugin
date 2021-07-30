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

        </Dialog>
      </div>
    </template>
    <template #content>
      <div class="tool-wrapper">
        <label for="sizeSlider">Size</label>
        <Slider id="sizeSlider"
                v-model="brushSize"
                :min="brushSizeRange[0]"
                :max="brushSizeRange[1]"
        />
        <span class="p-buttonset">
          <SelectButton v-model="brushType" :options="brushOptions" optionLabel="name" optionValue="value"/>
          <Button label="Undo" icon="pi pi-undo" />
          <Button label="Redo" icon="pi pi-refresh" />
          <Button label="Clear" icon="pi pi-trash" />
        </span>
      </div>
      <InteractionCanvas/>
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
      displayInfo: false,
      brushOptions: [
        {name: 'Foreground', value: 'fg'},
        {name: 'Background', value: 'bg'}
      ],
			brushSizeRange: [0,30],
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
