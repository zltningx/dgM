<template>
  <div class="app-container">
      <ticket-table :show="show"></ticket-table>
  </div>
</template>

<script>
  import TicketTable from './components/TicketTable'
  import getInfo from '@/api/user'

  export default {
    name: 'TicketListAll',
    components: {
      TicketTable
    },
    data() {
      return {
        show: 'own'
      }
    },
    created () {
      this.show = 'own'
    }
  }
</script>
