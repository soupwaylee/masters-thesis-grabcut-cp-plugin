import axios from 'axios';

import store from '../store';

const APIBaseURL = '/grabcut';

export class APIService {

    constructor() {
        // this.store = store;

        this.instance = axios.create({
            baseURL: APIBaseURL,
            timeout: 1000 * 5,
        });
    }

    getTodos() {
        return this.instance.get('todos/').then( response => response.data );
    }

    newTodo(task) {
        return this.instance.post('todos/', {'task': task}).then( response => response.data );
    }

    deleteTodo(id) {
        return this.instance.delete(`todos/${id}`)
    }

    getDHMImage(id) {
        return this.instance.get(`/dhmimages/${id}`).then( response => response.data );
    }
}