<template>
  <form @submit.prevent="addTask" class="add-task-form">
    <input
      type="text"
      v-model="newTask.title"
      placeholder="新增任務標題"
      required
    />
    <input
      type="text"
      v-model="newTask.description"
      placeholder="任務描述 (選填)"
    />
    <input
      type="datetime-local"
      v-model="newTask.due_date"
    />
    <select v-model="newTask.category">
      <option value="工作">工作</option>
      <option value="會議">會議</option>
      <option value="個人">個人</option>
    </select>
    <input
      type="text"
      v-if="newTask.category === '會議'"
      v-model="newTask.client_name"
      placeholder="客戶名稱"
    />
    <input
      type="text"
      v-if="newTask.category === '會議'"
      v-model="newTask.location"
      placeholder="會議地點"
    />
    <button type="submit">新增任務</button>
  </form>
</template>

<script>
import axios from 'axios';

export default {
  name: 'AddTaskForm',
  props: {
    initialCategory: {
      type: String,
      default: '工作'
    }
  },
  data() {
    return {
      newTask: {
        title: '',
        description: '',
        due_date: '',
        category: this.initialCategory,
        client_name: '',
        location: ''
      }
    };
  },
  methods: {
    async addTask() {
      console.log('addTask method called');
      try {
        const taskPayload = { ...this.newTask };
        // Remove empty strings for optional fields to avoid sending them as empty
        for (const key in taskPayload) {
          if (taskPayload[key] === '') {
            taskPayload[key] = null;
          }
        }
        console.log('Sending taskPayload:', taskPayload);
        
        await axios.post('http://127.0.0.1:5000/api/tasks', taskPayload);
        console.log('Task added successfully!');
        this.resetForm();
        this.$emit('task-added');
      } catch (error) {
        console.error('Error adding task:', error);
      }
    },
    resetForm() {
      this.newTask = {
        title: '',
        description: '',
        due_date: '',
        category: this.initialCategory,
        client_name: '',
        location: ''
      };
    }
  }
};
</script>

<style scoped>
.add-task-form {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 15px;
  background-color: #e9ecef;
  border-radius: 8px;
  margin-bottom: 20px;
}

.add-task-form input[type="text"],
.add-task-form input[type="datetime-local"],
.add-task-form select {
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 1em;
}

.add-task-form button {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 10px 15px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1em;
}

.add-task-form button:hover {
  background-color: #0056b3;
}
</style>
