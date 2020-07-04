import request from '@/utils/request'

// 安全测试工单 api
export function getTickets(params) {
  return request({
    url: '/penetration_ticket/',
    method: 'get',
    params
  })
}

export function newTicket(data) {
  return request({
    url: '/penetration_ticket/',
    method: 'post',
    data
  })
}

export function getTicket(id) {
  return request({
    url: `/penetration_ticket/${id}/`,
    method: 'get'
  })
}

export function editTicket(id, data) {
  return request({
    url: `/penetration_ticket/${id}/`,
    method: 'put',
    data
  })
}

export function deleteTicket(id) {
  return request({
    url: `/penetration_ticket/${id}/`,
    method: 'delete'
  })
}

export function createSubWorkflow(data) {
  return request({
    url: '/penetration_ticket_sub_workflow/',
    method: 'post',
    data
  })
}

export function getVulTypes() {
  return request({
    url: '/penetration_ticket_manager/get_types/',
    method: 'get'
  })
}

export function createTicketResult(data) {
  return request({
    url: '/penetration_ticket_result/',
    method: 'post',
    data
  })
}

// 漏洞生命周期管理 api

export function getVuls(params) {
  return request({
    url: '/vulnerability/',
    method: 'get',
    params
  })
}

export function getVul(id) {
  return request({
    url: `/vulnerability/${id}/`,
    method: 'get'
  })
}

export function editVul(id, data) {
  return request({
    url: `/vulnerability/${id}/`,
    method: 'put',
    data
  })
}

export function deleteVul(id) {
  return request({
    url: `/vulnerability/${id}/`,
    method: 'delete'
  })
}

export function getVulWorkflows(params) {
  return request({
    url: '/vul_workflow/',
    method: 'get',
    params
  })
}

export function getVulWorkflow(id) {
  return request({
    url: `/vul_workflow/${id}/`,
    method: 'get'
  })
}

export function newVulWorkflow(data) {
  return request({
    url: '/vul_workflow/',
    method: 'post',
    data
  })
}

export function editVulWorkflow(id, data) {
  return request({
    url: `/vul_workflow/${id}/`,
    method: 'put',
    data
  })
}

export function deleteVulWorkflow(id) {
  return request({
    url: `/vul_workflow/${id}/`,
    method: 'delete'
  })
}

export function createVulSubWorkflow(data) {
  return request({
    url: '/vul_sub_workflow/',
    method: 'post',
    data
  })
}

// 资产 Api

export function getAssets(params) {
  return request({
    url: '/asset/',
    method: 'get',
    params
  })
}

export function getAsset(id) {
  return request({
    url: `/asset/${id}`,
    method: 'get'
  })
}

export function newAsset(data) {
  return request({
    url: '/asset/',
    method: 'post',
    data
  })
}

export function editAsset(id, data) {
  return request({
    url: `/asset/${id}/`,
    method: 'put',
    data
  })
}

export function deleteAsset(id) {
  return request({
    url: `/asset/${id}/`,
    method: 'delete'
  })
}

export function deletePort(id) {
  return request({
    url: `/port/${id}/`,
    method: 'delete'
  })
}

export function editPort(id, data) {
  return request({
    url: `/port/${id}/`,
    method: 'put',
    data
  })
}

// SMTP Api
export function newSMTPConfig(data) {
  return request({
    url: '/smtp/',
    method: 'post',
    data
  })
}

export function getSMTPConfig(params) {
  return request({
    url: '/smtp/',
    method: 'get',
    params
  })
}

export function editSMTPConfig(id, data) {
  return request({
    url: `/smtp/${id}/`,
    method: 'put',
    data
  })
}

// notify Api
export function testSMTPConfig(data) {
  return request({
    url: '/notify/test/',
    method: 'post',
    data
  })
}

export function penTodoNotifiy(params) {
  return request({
    url: '/notify/pen/todo/',
    method: 'get',
    params
  })
}

export function vulTodoNotifiy(params) {
  return request({
    url: '/notify/vul/todo/',
    method: 'get',
    params
  })
}
