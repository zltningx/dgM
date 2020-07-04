import request from '@/utils/request'

export function login(data) {
  return request({
    url: '/token/obtain/',
    method: 'post',
    data
  })
}

export function getInfo(token) {
  return request({
    url: '/user/info/',
    method: 'post',
    data: token
  })
}

// export function logout() {
//   return request({
//     url: '/user/logout/',
//     method: 'post'
//   })
// }

export function getTransactors() {
  return request({
    url: '/user/get_transactors/',
    method: 'get'
  })
}

export function getSecGroup() {
  return request({
    url: '/user/get_sec_group/',
    method: 'get'
  })
}

// read user
export function getUsers(params) {
  return request({
    url: '/read_user/',
    method: 'get',
    params
  })
}

export function getUserInfo(id) {
  return request({
    url: `/read_user/${id}/`,
    method: 'get'
  })
}
