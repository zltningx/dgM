<template>
  <div class="app-container">
      <ticket-table :show="show"></ticket-table>
  </div>
</template>

<script>
  import TicketTable from './components/TicketTable'
  import getInfo from '@/api/user'

  export default {
    name: 'TicketListToDo',
    components: {
      TicketTable
    },
    data() {
      return {
        show: 'todo'
      }
    },
    created () {
      this.show = 'todo'
    }
  }
</script>
