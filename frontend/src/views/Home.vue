<template>
	<Card class="noTotalWidth p-shadow-5">
		<template #title>
			Plugin grabcut → ToDo Example
		</template>
		<template #content>
			<form id="newTodoForm" @submit.prevent="addTodo()" class="p-formgroup-inline">
				<span class="p-float-label">
					<InputText
						id="newTodoInput"
						v-model="newTodo"
						name="newTodo"
						autocomplete="off"
					/>
					<label for="newTodoInput">New ToDo</label>
				</span>
				<Button type="submit" label="Add ToDo" />
			</form>
			<h2>ToDo List</h2>

			<DataTable :value="todos" :reorderableColumns="true" @rowReorder="onRowReorder" responsiveLayout="scroll">
				<Column :rowReorder="true" headerStyle="width: 3rem" :reorderableColumn="false" />
				<Column field="id" header="ID"></Column>
				<Column field="task" header="Task"></Column>
				<Column :exportable="false" :reorderableColumn="false" headerStyle="width: 3rem">
                    <template #body="slotProps">
                        <Button icon="pi pi-trash" class="p-button-rounded p-button-danger" @click="removeTodo(slotProps.data)" />
                    </template>
                </Column>
			</DataTable>

			<h4 v-if="todos.length === 0">Empty list.</h4>
		</template>
	</Card>
</template>

<script>
	//import { ref } from 'vue';
	import { APIService as grabcutAPIService } from '../api/grabcutAPI';
	const grabcutAS = new grabcutAPIService();
	export default {
		name: 'App',
		data() {
			return {
				todos: [],
				newTodo: ''
			}
		},
		methods: {
			getTodos() {
				grabcutAS.getTodos().then( (data) => {
					console.log(data)
					this.todos = data;
				});
			},
			addTodo() {
				console.log('new todo!')
				console.log(this.newTodo)
				if( this.newTodo ) {
					grabcutAS.newTodo(this.newTodo).then( (data) => {
						this.todos.push(data)
					});
					this.newTodo = '';
				}
			},
			removeTodo(data) {
				grabcutAS.deleteTodo(data.id);
				this.todos = this.todos.filter(element => data.id != element.id);
			},
			onRowReorder(event) {
				this.todos = event.value;
			}
		},
		mounted() {
			this.getTodos();
		},
	}
</script>

<style lang="scss">

.noTotalWidth {
	width: 80%;
	margin: auto;
}

#newTodoForm {
	justify-content: center;
}

</style>
