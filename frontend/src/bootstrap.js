import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import PrimeVue from 'primevue/config';

import Button from 'primevue/button';
import InputText from 'primevue/inputtext';
import Card from 'primevue/card';
import Dialog from 'primevue/dialog';
import RadioButton from 'primevue/radiobutton';
import Slider from 'primevue/slider';
import SelectButton from 'primevue/selectbutton';
import DataView from 'primevue/dataview';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import ColumnGroup from 'primevue/columngroup';     //optional for column grouping

import 'primevue/resources/themes/saga-blue/theme.css';
import 'primevue/resources/primevue.min.css';
import 'primeicons/primeicons.css';
import 'primeflex/primeflex.css' 

const app = createApp(App)

app.use(store)
app.use(router)
app.use(PrimeVue)

app.component('Button', Button)
app.component('InputText', InputText)
app.component('Card', Card)
app.component('Dialog', Dialog)
app.component('RadioButton', RadioButton)
app.component('Slider', Slider)
app.component('SelectButton', SelectButton)
app.component('DataView', DataView)
app.component('DataTable', DataTable)
app.component('Column', Column)
app.component('ColumnGroup', ColumnGroup)

app.mount('#app')
