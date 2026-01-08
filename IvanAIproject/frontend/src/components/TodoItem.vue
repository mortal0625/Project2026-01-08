<template>
  <div :class="['todo-item', { completed: task.completed }]">
    <input type="checkbox" v-model="task.completed" @change="toggleCompleted" />
    <div class="task-content">
      <h3>{{ task.title }}</h3>
      <p v-if="task.description">{{ task.description }}</p>
      <p v-if="task.due_date">Due: {{ formattedDueDate }}</p>
      <p v-if="task.category">Category: {{ task.category }}</p>
      <p v-if="task.client_name">Client: {{ task.client_name }}</p>
      <p v-if="task.location">Location: {{ task.location }}</p>
    </div>
    <button @click="deleteTask" class="delete-btn">X</button>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'TodoItem',
  props: {
    task: {
      type: Object,
      required: true
    }
  },
  computed: {
    formattedDueDate() {
      if (this.task.due_date) {
        const date = new Date(this.task.due_date);
        return date.toLocaleDateString();
      }
      return '';
    }
  },
  methods: {
    async toggleCompleted() {
      try {
        await axios.put(`http://127.0.0.1:5000/api/tasks/${this.task.id}`, {
          ...this.task,
          completed: this.task.completed
        });
        this.$emit('task-updated');
      } catch (error) {
        console.error('Error updating task:', error);
      }
    },
    async deleteTask() {
      try {
        await axios.delete(`http://127.0.0.1:5000/api/tasks/${this.task.id}`);
        this.$emit('task-deleted');
      } catch (error) {
        console.error('Error deleting task:', error);
      }
    }
  }
};
</script>

<style scoped>
.todo-item {
  display: flex;
  align-items: center;
  padding: 10px;
  border-bottom: 1px solid #eee;
  background-color: #fff;
}

.todo-item.completed {
  text-decoration: line-through;
  color: #aaa;
}

.todo-item input[type="checkbox"] {
  margin-right: 10px;
}

.task-content {
  flex-grow: 1;
}

.delete-btn {
  background-color: #ff4d4d;
  color: white;
  border: none;
  padding: 5px 10px;
  border-radius: 4px;
  cursor: pointer;
  margin-left: 10px;
}
</style>
