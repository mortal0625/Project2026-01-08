<template>
  <div class="calendar-view">
    <h1>日曆</h1>
    
    <v-calendar
      class="custom-calendar"
      :attributes="attributes"
      is-expanded
      title-position="left"
    ></v-calendar>

  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'CalendarView',
  data() {
    return {
      events: [],
    };
  },
  computed: {
    attributes() {
      return this.events.map(event => ({
        key: event.id,
        highlight: true,
        dates: new Date(event.start),
        popover: {
          label: event.title,
        },
      }));
    }
  },
  created() {
    this.fetchCalendarEvents();
  },
  methods: {
    async fetchCalendarEvents() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/api/tasks/calendar', {
          headers: {
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
            'Expires': '0',
          }
        });
        this.events = response.data;
      } catch (error) {
        console.error('Error fetching calendar events:', error);
      }
    },
  }
};
</script>

<style>
.custom-calendar.vc-container {
  --day-border: 1px solid #b8c2cc;
  --day-border-highlight: 1px solid #b8c2cc;
  --day-width: 90px;
  --day-height: 90px;
  --weekday-bg: #f8fafc;
  --weekday-border: 1px solid #eaeaea;
  border-radius: 0;
  width: 100%;
}
</style>
