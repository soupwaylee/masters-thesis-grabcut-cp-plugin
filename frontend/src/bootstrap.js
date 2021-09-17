import {createApp} from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import PrimeVue from 'primevue/config';

import ConfirmationService from 'primevue/confirmationservice';
import ToastService from 'primevue/toastservice';

import Button from 'primevue/button';
import InputText from 'primevue/inputtext';
import Card from 'primevue/card';
import ConfirmPopup from 'primevue/confirmpopup';
import Dialog from 'primevue/dialog';
import Dropdown from 'primevue/dropdown';
import Slider from 'primevue/slider';
import SelectButton from 'primevue/selectbutton';
import Skeleton from 'primevue/skeleton';
import Toast from 'primevue/toast';
import ToggleButton from 'primevue/togglebutton';
import Tooltip from 'primevue/tooltip';
import DataView from 'primevue/dataview';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import ColumnGroup from 'primevue/columngroup'; //optional for column grouping
import 'primevue/resources/themes/saga-blue/theme.css';
import 'primevue/resources/primevue.min.css';
import 'primeicons/primeicons.css';
import 'primeflex/primeflex.css'

const app = createApp(App)

app.use(store)
app.use(router)
app.use(PrimeVue)
app.use(ConfirmationService)
app.use(ToastService);

app.directive('tooltip', Tooltip);

app.component('Button', Button)
app.component('InputText', InputText)
app.component('Card', Card)
app.component('ConfirmPopup', ConfirmPopup)
app.component('Dialog', Dialog)
app.component('Slider', Slider)
app.component('SelectButton', SelectButton)
app.component('Skeleton', Skeleton)
app.component('Toast', Toast)
app.component('ToggleButton', ToggleButton)
app.component('DataView', DataView)
app.component('DataTable', DataTable)
app.component('Column', Column)
app.component('ColumnGroup', ColumnGroup)
app.component('Dropdown', Dropdown)

app.mount('#app')
