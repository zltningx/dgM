<template>
  <ticket-detail :is-edit="false" />
</template>

<script>
import TicketDetail from './components/TicketDetail'

export default {
  name: 'CreateTicket',
  components: { TicketDetail }
}
</script>

