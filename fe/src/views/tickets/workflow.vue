<template>
  <ticket-workflow :is-edit="true" />
</template>

<script>
import TicketWorkflow from './components/TicketWorkflow'

export default {
  name: 'Workflow',
  components: { TicketWorkflow }
}
</script>

