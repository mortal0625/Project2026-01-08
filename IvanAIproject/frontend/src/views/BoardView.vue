<template>
  <div class="board-view">
    <h1>看板</h1>

    <div class="add-task-section">
      <h2>任務新增</h2>
      <AddTaskForm @task-added="fetchBoardTasks" :initialCategory="'工作'" />
    </div>

    <div class="task-categories">
      <div class="task-category-row">
        <h3>今天要做</h3>
        <div class="tasks-container">
          <div v-for="task in boardTasks.today" :key="task.id" class="task-card">
            <TodoItem :task="task" @task-updated="fetchBoardTasks" @task-deleted="fetchBoardTasks" />
          </div>
        </div>
      </div>

      <div class="task-category-row">
        <h3>本週要做</h3>
        <div class="tasks-container">
          <div v-for="task in boardTasks.this_week" :key="task.id" class="task-card">
            <TodoItem :task="task" @task-updated="fetchBoardTasks" @task-deleted="fetchBoardTasks" />
          </div>
        </div>
      </div>

      <div class="task-category-row">
        <h3>未來規劃</h3>
        <div class="tasks-container">
          <div v-for="task in boardTasks.future" :key="task.id" class="task-card">
            <TodoItem :task="task" @task-updated="fetchBoardTasks" @task-deleted="fetchBoardTasks" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import AddTaskForm from '../components/AddTaskForm.vue';
import TodoItem from '../components/TodoItem.vue';

export default {
  name: 'BoardView',
  components: {
    AddTaskForm,
    TodoItem
  },
  data() {
    return {
      boardTasks: {
        today: [],
        this_week: [],
        future: []
      }
    };
  },
  created() {
    this.fetchBoardTasks();
  },
  methods: {
    async fetchBoardTasks() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/api/tasks/board', {
          headers: {
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
            'Expires': '0',
          }
        });
        this.boardTasks = response.data;
      } catch (error) {
        console.error('Error fetching board tasks:', error);
      }
    }
  }
};
</script>

<style scoped>
.board-view {
  padding: 20px;
}

.add-task-section {
  margin-bottom: 30px;
  background-color: #f0f0f0;
  padding: 20px;
  border-radius: 8px;
}

.add-task-section h2 {
  text-align: center;
  margin-bottom: 15px;
  color: #333;
}

.task-categories {
  display: flex;
  flex-direction: column; /* Stack categories vertically */
  gap: 20px;
}

.task-category-row {
  background-color: #f4f4f4;
  padding: 15px;
  border-radius: 8px;
}

.task-category-row h3 {
  text-align: center;
  margin-bottom: 15px;
  color: #333;
  font-size: 1.5em;
}

.tasks-container {
  display: flex; /* Tasks flow horizontally */
  overflow-x: auto; /* Enable horizontal scrolling if needed */
  gap: 15px;
  padding-bottom: 10px; /* Space for scrollbar */
}

.task-card {
  flex-shrink: 0; /* Prevent tasks from shrinking */
  width: 280px; /* Fixed width for task cards */
  background-color: white;
  border: 1px solid #ddd;
  border-radius: 5px;
  padding: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}
</style>
