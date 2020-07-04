<template>
  <ticket-detail :is-edit="true" />
</template>

<script>
import TicketDetail from './components/TicketDetail'

export default {
  name: 'EditTicket',
  components: { TicketDetail }
}
</script>

