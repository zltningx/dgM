<template>
  <div class="app-container">
      <ticket-table></ticket-table>
  </div>
</template>

<script>
  import TicketTable from './components/TicketTable'
  import getInfo from '@/api/user'

  export default {
    name: 'TicketListAll',
    components: {
      TicketTable
    }
  }
</script>
